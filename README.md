---
title: UNOCHA Geo-Insight
emoji: "💻"
colorFrom: blue
colorTo: gray
sdk: gradio
sdk_version: "6.14.0"
python_version: "3.13"
app_file: geo-insight/src/app.py
pinned: false
---

# Geo-Insight: Which Crises Are Most Overlooked?

## Datathon 2026 Solution by QuattroFormaggi

As conflicts, famine, natural disasters and other crises emerge, the question of distributing funding also arises. Organizations like UN OCHA take on this task, analyzing vast amounts of data to make sure that the money is given to those in need. However, working with humanitarian data is not easy for a few reasons. Firstly and most importantly, it represents real people, often in vulnerable situations, and they should not be treated as just data points. Secondly, crises are complex mechanisms that just cannot be condensed into a table or a plot.

Coordinators at organizations such as OCHA need tools that provide them with holistic, descriptive, and expert-level information. That's why we created **Geo-Insight Assistant** — an interactive briefing note generator. It focuses on providing a range of information regarding the queried topic in a one-sheet, ready-to-print text format.

### 🎯 Key Features

- 🔍 **Natural Language Queries** - Ask questions like "Show underfunded food crises in the Sahel"
- 📊 **Intelligent Data Filtering** - Powered by Claude AI for query interpretation
- 📝 **Professional Briefing Notes** - AI-generated reports with key insights and funding gaps
- 💾 **Export Capabilities** - Save results as PDF for sharing
- 🚀 **Cloud-Ready** - Deployed on Hugging Face Spaces with OpenRouter API

### ⚡ Quick Start (Local Development)

```bash
# 1. Clone and setup
./setup.sh

# 2. Add your OpenRouter API key to .env
# Get key from https://openrouter.ai/

# 3. Run the app
python geo-insight/app.py

# 4. Open in browser
# http://localhost:7860
```

### 📖 Full Documentation

- **[Setup & Deployment Guide](./geo-insight/HF_SPACES_README.md)** - Deploy on Hugging Face Spaces
- **[Migration Guide](./MIGRATION_GUIDE.md)** - Technical details of Databricks → CSV + OpenRouter changes
- **[Local Setup](./geo-insight/README.md)** - Detailed local development guide

### 🏗 Architecture

```
User Query (Natural Language)
    ↓
Query Interpreter (Claude 3.5 Sonnet via OpenRouter)
    ↓ [Structured Query JSON]
Data Filtering (CSV-based pandas operations)
    ↓ [Filtered Dataset]
Briefing Note Writer (Claude 3.5 Sonnet via OpenRouter)
    ↓ [Professional Report]
User (with PDF export option)
```

### 📊 Data Source


1. Download appropriate datasets from the following links:
   - https://data.humdata.org/dataset/global-hpc-hno (make sure to add the year column in order to distinguish between records in provided CSV files),
   - https://data.humdata.org/dataset/global-requirements-and-funding-data &ndash; specifically, `fts_requirements_funding_global.csv` and `fts_incoming_funding_global.csv`,
   - https://data.worldbank.org/indicator/SP.POP.TOTL?end=2023&start=2001 &ndash; in this case, the resulting CSV file should be flattened so that it has 3 columns - `Country Code`, `year` and `population`,
   - https://www.acaps.org/en/data (optional) &ndash; contains monthly severity indices per crisis; requires some preprocessing before ingesting


- **Format**: CSV (local file: `data/unocha_dataset.csv`)
- **Records**: 7,610+ humanitarian crisis data points
- **Columns**: Country code, sector, population, funding gaps, severity metrics
- **No external database required** - Simple CSV-based filtering

### 🔑 API Provider

- **Provider**: OpenRouter (https://openrouter.ai/)
- **Model**: Claude 3.5 Sonnet
- **Cost**: ~$0.003 per request (~$10/month for typical usage)
- **Benefits**: Cost-effective, reliable, no lock-in to single provider

### 📋 Query Examples

Try these natural language queries:

```
"Show underfunded food crises in the Sahel since 2022"
"Current humanitarian needs in Middle East"
"Countries with critical funding gaps despite high severity"
"Protection sector emergencies in East Africa"
"Recent crises receiving less than 20% of required funds"
```

### 🚀 Deployment

#### Option 1: Hugging Face Spaces (Recommended)
- Zero infrastructure cost
- Automatic scaling
- Easy secrets management
- Custom domain optional

See: [HF_SPACES_README.md](./geo-insight/HF_SPACES_README.md)

#### Option 2: Local/Docker
- Full control
- Development testing
- Private deployment

### 📁 Project Structure

```
UNOCHA/
├── data/
│   └── unocha_dataset.csv          # Humanitarian data (7,600+ rows)
├── geo-insight/
│   ├── src/
│   │   ├── app.py                  # Main Gradio application
│   │   ├── requirements.txt         # Python dependencies
│   │   ├── models/
│   │   │   └── QuerySpec.py         # Data schema
│   │   ├── prompts/
│   │   │   ├── QueryInterpreter.md  # System prompts
│   │   │   └── BriefingNoteWriter.md
│   │   └── quattroformaggi/         # Core modules
│   │       ├── QueryInterpreter.py
│   │       ├── BriefingNoteWriter.py
│   │       ├── query_to_sql.py
│   │       └── query_to_articles.py
│   ├── .env.example                 # Environment template
│   ├── HF_SPACES_README.md          # Deployment guide
│   └── app.yaml                     # Gradio Space config
├── MIGRATION_GUIDE.md               # Databricks → CSV migration
├── setup.sh                         # Setup script
├── test_setup.py                    # Validation tests
├── Dockerfile                       # Container definition
└── README.md                        # This file
```

### 💡 Recent Changes

**Version 2.0 (May 2026):**
- ✅ Migrated from Databricks SQL to CSV-based data
- ✅ Switched from Anthropic SDK to OpenRouter API
- ✅ Optimized for Hugging Face Spaces deployment
- ✅ Reduced infrastructure costs by 99%
- ✅ Maintained all functionality and performance

See [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md) for technical details.

### 🧪 Testing

```bash
# Validate setup
python test_setup.py

# Run local dev server
python geo-insight/src/app.py

# Run Gradio tests (if implemented)
# pytest tests/
```

### 📞 Support

- **API Issues**: Check [OpenRouter docs](https://openrouter.ai/docs)
- **Deployment**: See [HF Spaces guide](./geo-insight/HF_SPACES_README.md)
- **Data Issues**: Check CSV format in [Migration Guide](./MIGRATION_GUIDE.md)

### 📄 License

[Your License Here]

### 👥 Credits

Built by **QuattroFormaggi** for UNOCHA Datathon 2026

---

**Live Demo**: [Coming soon - Deploy your own Space!](https://huggingface.co/spaces/new)

Need help? Check the [documentation](./geo-insight/HF_SPACES_README.md) or run `python test_setup.py` to validate your setup.


Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
emoji: 💻
