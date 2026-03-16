import json
import os
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from tabulate import tabulate

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------
# LOAD DATA
# -------------------------

with open("dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)["data"]

df = pd.DataFrame(dataset)

# normalize missing fields
df["likes"] = pd.to_numeric(df.get("likes", 0), errors="coerce").fillna(0)
df["sentiment"] = df.get("raw_sentiment", "unknown")
df["type"] = df.get("comment_type", "unknown")

# -------------------------
# BASIC GROUP STATISTICS
# -------------------------

stats = []

for group, g in df.groupby("group"):

    total = len(g)
    mean_likes = g["likes"].mean()

    sentiment_ratio = (
        g["sentiment"]
        .value_counts(normalize=True)
        .to_dict()
    )

    stats.append({
        "group": group,
        "comments": total,
        "mean_likes": round(mean_likes, 2),
        "humor_ratio": sentiment_ratio.get("humor", 0),
        "positive_ratio": sentiment_ratio.get("positive", 0),
        "neutral_ratio": sentiment_ratio.get("neutral", 0)
    })

stats_df = pd.DataFrame(stats)

# -------------------------
# DIFFERENCE TABLE
# -------------------------

if len(stats_df) >= 2:

    base = stats_df.iloc[0]
    comp = stats_df.iloc[1]

    diff = {
        "metric": [],
        "difference": []
    }

    for col in ["mean_likes", "humor_ratio", "positive_ratio", "neutral_ratio"]:

        diff["metric"].append(col)
        diff["difference"].append(round(comp[col] - base[col], 4))

    diff_df = pd.DataFrame(diff)

else:
    diff_df = pd.DataFrame()

# -------------------------
# PRINT TABLES
# -------------------------

print("\nSTATISTICS\n")
print(tabulate(stats_df, headers="keys", tablefmt="github"))

print("\nDIFFERENCE TABLE\n")
print(tabulate(diff_df, headers="keys", tablefmt="github"))

# -------------------------
# PREPARE SMALL PAYLOAD
# -------------------------

payload = {
    "statistics": stats_df.to_dict(orient="records"),
    "differences": diff_df.to_dict(orient="records")
}

prompt = f"""
You are analyzing social media comment sections.

Research question:
What differences exist in the characteristics of comment sections
under popular versus unpopular animal-related videos?

Dataset summary:

{json.dumps(payload, indent=2)}

Explain:

1. engagement differences
2. sentiment differences
3. humor vs neutral patterns
4. behavioral interpretation
"""

# -------------------------
# LLM ANALYSIS
# -------------------------

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    temperature=0.2,
    messages=[
        {"role": "system", "content": "You are a computational social science researcher."},
        {"role": "user", "content": prompt}
    ]
)

analysis = response.choices[0].message.content

# -------------------------
# SAVE REPORT
# -------------------------

with open("analysis_report.md", "w", encoding="utf-8") as f:

    f.write("# Comment Section Analysis\n\n")

    f.write("## Statistics\n\n")
    f.write(tabulate(stats_df, headers="keys", tablefmt="github"))

    f.write("\n\n## Differences\n\n")
    f.write(tabulate(diff_df, headers="keys", tablefmt="github"))

    f.write("\n\n## LLM Interpretation\n\n")
    f.write(analysis)

print("\nReport saved to analysis_report.md\n")