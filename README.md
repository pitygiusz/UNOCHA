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

This repository contains solution for the UN OCHA challange, developed by the QuattroFormaggi team during the **2026 Datathon** organised by **Analytics Club** at ETH Zurich. It is Switzerland's largest hackathon with over 200 participants from 24 universities. Learn more [here](https://www.datathon.ai/).

We created an interactive briefing note generator that helps humanitarian coordinators quickly understand the funding landscape of crises around the world. By asking natural language questions, users can get professional reports with key insights, funding gaps, and contextual analysis based on historical data and recent news. 

## Motivation

As conflicts, famine, natural disasters and other crises emerge, the question of distributing funding also arises. Organizations like UN OCHA take on this task, analyzing vast amounts of data to make sure that the money is given to those in need. However, working with humanitarian data is not easy for a few reasons. Firstly and most importantly, it represents real people, often in vulnerable situations, and they should not be treated as just data points. Secondly, crises are complex mechanisms that just cannot be condensed into a table or a plot.

Coordinators at organizations such as OCHA need tools that provide them with holistic, descriptive, and expert-level information. That's why we created **Geo-Insight Assistant** — an interactive briefing note generator. It focuses on providing a range of information regarding the queried topic in a one-sheet, ready-to-print text format. The data used is a conjunction of [historical data provided by OCHA](https://data.humdata.org/) as well as [recent humanitarian-oriented news](https://reliefweb.int/). Importantly, it analyses figures, but doesn't discriminate because of them. When data is uncertain, missing, or otherwise suspicious, it informs the user about this fact so that no rushed decisions are being made.

## Key Features

- **Natural Language Queries** - Ask questions like "Show underfunded food crises in the Sahel" or "Current humanitarian needs in Middle East"
- **Intelligent Data Filtering** - AI-powered query interpretation to extract relevant data from large datasets
- **Professional Briefing Notes** - AI-generated reports with key insights, funding gaps, and contextual analysis
- **Cloud Deployment** - Runs on Hugging Face Spaces with OpenRouter API

## How to Run

Deploy your own instance in minutes:

1. Create a new Space on Hugging Face: https://huggingface.co/spaces/new
2. Choose "Gradio" as the SDK
3. Connect this repository
4. Add your OpenRouter API key as a secret
5. Space will deploy automatically


## System Architecture

```
User Query (Natural Language)
    |
    v
Query Interpreter (OpenRouter API)
    |
    v (Structured Query JSON with regions, sectors, date ranges)
Data Filtering (CSV-based pandas operations)
    |
    v (Relevant humanitarian data subset)
Briefing Note Writer (OpenRouter API)
    |
    v
Professional Briefing Note + PDF Export
```


## Data Sources

The application uses humanitarian data from multiple authoritative sources:

- UN OCHA HPC: Global humanitarian needs and response data
- World Bank: Population statistics for context
- ReliefWeb: Latest crisis news and articles
- FTS Global: Requirements and funding data

The data was manually cleaned and preprocessed to ensure quality and relevance. The final datasets include over 7,600 crisis records and almost 1000 news articles, covering a wide range of regions, sectors, and time periods.



## Example Queries

The system accepts natural language questions like:

- "Show underfunded food crises in the Sahel since 2022"
- "Current humanitarian needs in Middle East"
- "Countries with highest severity but lowest funding."


Each query generates a professional briefing note with:
- Executive summary
- Contextual analysis
- Key funding gaps
- Regional trends
- Recommendations for resource allocation


## Project Structure

```
UNOCHA/
├── data/
│   ├── unocha_dataset.csv          
│   └── reliefweb_dataset.csv       
├── geo-insight/
│   ├── app.py                      # Main Gradio application entry point
│   ├── .env.example                               
│   └── src/
│       ├── QueryInterpreter.py     # Query parsing logic
│       ├── BriefingNoteWriter.py   # Report generation
│       ├── QueryInterpreter.md     # System prompt for query parsing
│       ├── BriefingNoteWriter.md   # System prompt for report writing
│       ├── query_to_sql.py         # Data filtering logic
│       ├── query_to_articles.py    # Article retrieval logic
│       ├── QuerySpec.py            # Data schema and validation
│       └── __init__.py             
├── documentation/
│   └── (Architecture and technical documentation)
├── requirements.txt                # Python dependencies
├── Dockerfile                      
└── README.md                       
```

## Note
This project was orginally designed to run on **Databricks** Platform, from data processing to the final application. It was later adapted to run on Hugging Face Spaces for easy demonstration. The main changes include:
- Data loading and processing layer was simplified to use CSV files and pandas instead of SQL database queries.
- Claude API calls were replaced with OpenRouter API calls, and the system prompts were adapted accordingly. 