---
title: UNOCHA Geo-Insight
colorFrom: blue
colorTo: gray
sdk: gradio
sdk_version: "6.14.0"
python_version: "3.13"
app_file: geo-insight/app.py
pinned: false
---

# Geo-Insight: Which Crises Are Most Overlooked?

## Datathon 2026 Solution by QuattroFormaggi

As conflicts, famine, natural disasters and other crises emerge, the question of distributing funding also arises. Organizations like UN OCHA take on this task, analyzing vast amounts of data to make sure that the money is given to those in need. However, working with humanitarian data is not easy for a few reasons. Firstly and most importantly, it represents real people, often in vulnerable situations, and they should not be treated as just data points. Secondly, crises are complex mechanisms that just cannot be condensed into a table or a plot.

Coordinators at organizations such as OCHA need tools that provide them with holistic, descriptive, and expert-level information. That's why we created **Geo-Insight Assistant** — an interactive briefing note generator. It focuses on providing a range of information regarding the queried topic in a one-sheet, ready-to-print text format.

## Key Features

- **Natural Language Queries** - Ask questions like "Show underfunded food crises in the Sahel" or "Current humanitarian needs in Middle East"
- **Intelligent Data Filtering** - Powered by Claude AI for accurate query interpretation into structured database filters
- **Professional Briefing Notes** - AI-generated reports with key insights, funding gaps, and contextual analysis
- **PDF Export** - Save results for sharing with stakeholders and decision-makers
- **Cloud Deployment** - Runs on Hugging Face Spaces with OpenRouter API (zero infrastructure costs)

## Quick Start on Hugging Face Spaces

Deploy your own instance in minutes:

1. Create a new Space on Hugging Face: https://huggingface.co/spaces/new
2. Choose "Gradio" as the SDK
3. Connect this repository
4. Add your OpenRouter API key as a secret (get one free at https://openrouter.ai/)
5. Space will deploy automatically

No Docker, no server management, no DevOps experience needed.

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Add your OpenRouter API key
cp geo-insight/.env.example geo-insight/.env
# Edit .env with your API key

# Run locally
python geo-insight/app.py

# Open browser to http://localhost:7860
```

## Architecture

```
User Query (Natural Language)
    |
    v
Query Interpreter (Claude 3.5 Sonnet via OpenRouter API)
    |
    v (Structured Query JSON with regions, sectors, date ranges)
Data Filtering (CSV-based pandas operations)
    |
    v (Relevant humanitarian data subset)
Briefing Note Writer (Claude 3.5 Sonnet via OpenRouter API)
    |
    v
Professional Briefing Note + PDF Export
```

The system is built on a clean separation of concerns:
- **Query Interpretation**: Converts natural language questions into structured database queries
- **Data Layer**: CSV-based filtering with pandas (no external databases required)
- **Report Generation**: AI-powered briefing notes with context and insights

## Data Sources

The application uses humanitarian data from multiple authoritative sources:

- UN OCHA HPC: Global humanitarian needs and response data
- World Bank: Population statistics for context
- ReliefWeb: Latest crisis news and articles
- FTS Global: Requirements and funding data

All data is stored locally as CSV files (7,600+ crisis records) for fast access and cost efficiency.

## Technology Stack

- **Frontend**: Gradio (Python-based web UI)
- **Backend**: Python with pandas for data processing
- **AI Models**: Claude 3.5 Sonnet via OpenRouter API
- **Hosting**: Hugging Face Spaces
- **Data Format**: CSV (no database dependencies)

## Example Queries

The system accepts natural language questions like:

- "Show underfunded food crises in the Sahel since 2022"
- "Current humanitarian needs in Middle East"
- "Countries with critical funding gaps despite high severity"
- "Protection sector emergencies in East Africa"
- "Recent crises receiving less than 20% of required funds"

Each query generates a professional briefing note with:
- Executive summary
- Contextual analysis
- Key funding gaps
- Regional trends
- Recommendations for resource allocation

## Cost Efficiency

- **Infrastructure**: $0 (Hugging Face Spaces free tier)
- **API Costs**: ~$0.003 per request (~$10/month for typical usage)
- **Total Monthly Cost**: ~$10 for production use
- **Previous Solution**: $500+/month with Databricks + proprietary APIs

This project demonstrates how modern open-source tools and cost-effective APIs can build production-grade humanitarian applications without expensive infrastructure.

## Development Notes

This was built during the UNOCHA Datathon 2026 as a solution to help humanitarian coordinators make better allocation decisions through accessible, intelligent tools. The focus has been on:

1. **Usability**: Natural language queries instead of database knowledge
2. **Cost**: Minimal operational expenses for NGOs
3. **Reliability**: Simple architecture with no external dependencies beyond APIs
4. **Professionalism**: Polished reports suitable for decision-making

## Further Reading

- OpenRouter API Documentation: https://openrouter.ai/docs
- Hugging Face Spaces: https://huggingface.co/spaces
- Gradio Documentation: https://gradio.app
- UN OCHA Data: https://data.humdata.org

## Project Structure

```
UNOCHA/
├── data/
│   ├── unocha_dataset.csv          # Humanitarian crisis data (7,600+ records)
│   └── reliefweb_dataset.csv       # News and articles data
├── geo-insight/
│   ├── app.py                      # Main Gradio application entry point
│   ├── .env.example                # Environment variables template
│   ├── README.md                   # Detailed setup guide
│   └── src/
│       ├── QueryInterpreter.py     # Query parsing logic
│       ├── BriefingNoteWriter.py   # Report generation
│       ├── QueryInterpreter.md     # System prompt for query parsing
│       ├── BriefingNoteWriter.md   # System prompt for report writing
│       ├── query_to_sql.py         # Data filtering logic
│       ├── query_to_articles.py    # Article retrieval logic
│       ├── QuerySpec.py            # Data schema and validation
│       └── __init__.py             # Package initialization
├── notebooks/
│   └── (Data exploration and analysis notebooks)
├── documentation/
│   └── (Architecture and technical documentation)
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container configuration
└── README.md                       # This file
```
