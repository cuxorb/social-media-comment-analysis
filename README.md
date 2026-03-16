# Social Media Comment Section Analysis

Group project for **AIE1902** — CUHK-Shenzhen

## Overview

This project analyzes differences in comment section behavior between popular and unpopular animal-related videos on social media. It compares engagement, sentiment, and humor patterns using statistical analysis and LLM interpretation.

**Research Question:** What differences exist in the characteristics of comment sections under popular versus unpopular animal-related videos?

## Key Findings

| Metric | Popular Videos | Unpopular Videos |
|---|---|---|
| Mean Likes per Comment | 845 | 13 |
| Positive Sentiment | 30% | 16% |
| Humor Ratio | 35% | 31% |
| Neutral Ratio | 15% | 25% |

Popular videos attract significantly more positive and humorous comments, while unpopular videos generate more neutral, less engaged commentary.

## Project Structure

```
├── analyze.py              # Main analysis script
├── dataset.json            # Raw comment dataset
├── dataset_1_batch.json    # Batch 1 data
├── dataset_2_batch.json    # Batch 2 data
├── analysis_report.md      # Generated report
├── photos/                 # Post screenshots (post_1 to post_20)
├── images/                 # Campaign images
└── requirements.txt        # Python dependencies
```

## How to Run

1. Clone the repository:
```bash
git clone https://github.com/cuxorb/social-media-comment-analysis.git
cd social-media-comment-analysis
```

2. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Add your OpenAI API key:
```bash
echo "OPENAI_API_KEY=your_key_here" > .env
```

4. Run the analysis:
```bash
python analyze.py
```

The report will be saved to `analysis_report.md`.

## Tech Stack

- **Python** — data processing
- **pandas** — statistical analysis
- **OpenAI GPT-4.1-mini** — LLM interpretation
- **tabulate** — report formatting
