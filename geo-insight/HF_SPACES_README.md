# UNOCHA Geo-Insight

A Gradio-based application that analyzes humanitarian crises data and generates briefing notes using natural language queries. Now running on Hugging Face Spaces with OpenRouter API integration.

## Features

- 🔍 Natural language query interpretation for humanitarian data
- 📊 CSV-based data processing (no database required)
- 📝 AI-powered briefing note generation
- 💾 Export results as PDF
- 🚀 Deployed on Hugging Face Spaces

## Setup for Hugging Face Spaces

### 1. Create a Space
- Go to https://huggingface.co/spaces
- Create a new Space with Gradio runtime
- Choose Docker container option if you want more control

### 2. Set Environment Variables
Add the following secret variable in your Space settings:

```
OPENROUTER_API_KEY=your_api_key_here
```

Get your OpenRouter API key from: https://openrouter.ai/

### 3. Data File
Place the CSV file at: `data/unocha_dataset.csv`

The CSV should have these columns:
- `country_code` - ISO3 country code
- `cluster_code` - Humanitarian sector code
- `sector` - Sector description
- `population` - Country population
- `in_need` - Number of people in need
- `targeted` - Number of people targeted
- `year` - Year of data
- `total_required_funds` - Funds requested
- `total_granted_funds` - Funds granted
- `total_granted_percentage` - Percentage of granted vs required
- `severity_index` - Crisis severity measure

### 4. Deploy

Clone your repository and push to Hugging Face:

```bash
git clone https://huggingface.co/spaces/USERNAME/geo-insight
cd geo-insight
git add .
git commit -m "Initial commit"
git push
```

## Local Development

### Requirements
```bash
pip install -r geo-insight/src/requirements.txt
```

### Setup
1. Copy `.env.example` to `.env` and add your OpenRouter API key
2. Ensure `data/unocha_dataset.csv` exists in the root directory

### Run
```bash
cd geo-insight/src
python app.py
```

## Project Structure

```
.
├── data/
│   └── unocha_dataset.csv          # Humanitarian data (CSV format)
├── geo-insight/
│   ├── src/
│   │   ├── app.py                  # Main Gradio application
│   │   ├── requirements.txt         # Python dependencies
│   │   ├── models/
│   │   │   └── QuerySpec.py         # Data schema for query interpretation
│   │   ├── prompts/
│   │   │   ├── QueryInterpreter.md  # System prompt for query parsing
│   │   │   └── BriefingNoteWriter.md # System prompt for report generation
│   │   └── quattroformaggi/
│   │       ├── QueryInterpreter.py  # NLP query interpretation (OpenRouter)
│   │       ├── BriefingNoteWriter.py # Report generation (OpenRouter)
│   │       ├── query_to_sql.py       # CSV data filtering
│   │       └── query_to_articles.py  # Articles data filtering
│   └── .env.example                 # Environment variables template
└── README.md
```

## Query Examples

Try these natural language queries:

- "Show underfunded food crises in the Sahel since 2022"
- "Current state of humanitarian needs in Middle East"
- "Countries with highest severity but lowest funding"
- "Protection sector crises in Africa"
- "Recent humanitarian emergencies with critical funding gaps"

## API Models Used

- **Query Interpretation**: Claude 3.5 Sonnet via OpenRouter
- **Report Generation**: Claude 3.5 Sonnet via OpenRouter

## Troubleshooting

### "OPENROUTER_API_KEY not set"
- Add the variable to your Space secrets
- For local dev, create `.env` file with `OPENROUTER_API_KEY=your_key`

### "CSV file not found"
- Ensure `data/unocha_dataset.csv` exists relative to project root
- Check file permissions

### No query results
- Try a simpler query with fewer filters
- Check that the CSV file contains data matching your criteria
- Review the debug output in the terminal

## Performance Notes

- Query interpretation: ~3-5 seconds
- Report generation: ~10-20 seconds
- Total request time: ~30-40 seconds

For faster responses, consider:
- Using simpler queries
- Filtering by specific years/regions upfront
- Reducing CSV dataset size if it's very large

## License

[Your License Here]

## Contact

For issues or suggestions, please open an issue in the repository.
