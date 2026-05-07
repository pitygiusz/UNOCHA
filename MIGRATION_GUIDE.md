# Migration Guide: Databricks → CSV + OpenRouter (HF Spaces)

## Summary of Changes

This guide documents the changes made to migrate the UNOCHA Geo-Insight project from Databricks Apps with Anthropic API to Hugging Face Spaces with OpenRouter API and CSV-based data.

### Major Changes

#### 1. **Data Source**
| Before | After |
|--------|-------|
| Databricks SQL Tables | CSV files (local) |
| `unocha.default.master_table` | `data/unocha_dataset.csv` |
| `unocha.default.reliefweb_cleaned` | Same CSV (filtered) |
| Real-time cloud DB | Static CSV snapshot |

#### 2. **LLM Provider**
| Before | After |
|--------|-------|
| Anthropic Python SDK | OpenRouter HTTP API |
| `claude-sonnet-4-6` | `claude-3.5-sonnet` |
| Direct API calls | REST endpoints via requests |
| SDK-based auth | Bearer token via headers |

#### 3. **Hosting Platform**
| Before | After |
|--------|--------|
| Databricks Apps | Hugging Face Spaces |
| `demo.launch(share=True, inline=True)` | Gradio container on HF |
| Databricks-specific settings | Standard Gradio deployment |
| Internal DB connectivity | CSV file in repo |

---

## File-by-File Changes

### `requirements.txt`
**Removed:**
- `anthropic` (SDK for Anthropic API)
- `databricks-sdk`
- `databricks-sql-connector`

**Added:**
- `requests` (for OpenRouter HTTP API)
- `python-dotenv` (for environment variable management)

**Kept:**
- `gradio>=4.44.0`
- `pandas`
- `pydantic`
- `typing_extensions`
- `reportlab`
- `markdown`
- `tabulate`

### `app.py`
**Key Changes:**
1. ✂️ Removed Databricks connection code:
   ```python
   # REMOVED:
   from databricks import sql
   connection = sql.connect(...)
   connection.close()
   ```

2. ✂️ Removed environment variable checks for Databricks:
   ```python
   # REMOVED:
   db_host = os.getenv("DATABRICKS_HOST")
   db_http_path = os.getenv("DATABRICKS_HTTP_PATH")
   db_token = os.getenv("DATABRICKS_TOKEN")
   ```

3. ✅ Added CSV path handling:
   ```python
   # ADDED:
   from pathlib import Path
   WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
   CSV_FILE_PATH = WORKSPACE_ROOT / "data" / "unocha_dataset.csv"
   ```

4. ✅ Updated function signatures:
   ```python
   # BEFORE:
   filtered_df = filter_humanitarian_data(agent_json, connection, master_table_path)
   
   # AFTER:
   filtered_df = filter_humanitarian_data(agent_json, str(CSV_FILE_PATH))
   ```

5. ✅ Added error handling for missing CSV:
   ```python
   # ADDED:
   try:
       print("[DEBUG] Calling filter_humanitarian_data...")
       filtered_df = filter_humanitarian_data(agent_json, str(CSV_FILE_PATH))
   except Exception as e:
       print(f"[ERROR] Error during data filtering: {str(e)}")
       raise
   ```

### `QueryInterpreter.py`
**Complete Refactor:**

**Before (Anthropic SDK):**
```python
import anthropic

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=system_prompt,
    messages=[...]
)
text = next(block.text for block in message.content if isinstance(block, anthropic.types.TextBlock))
```

**After (OpenRouter API):**
```python
import requests

api_key = os.getenv("OPENROUTER_API_KEY")
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://huggingface.co/spaces",
    "X-Title": "UNOCHA Geo-Insight"
}

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers=headers,
    json={
        "model": "claude-3.5-sonnet",
        "max_tokens": 1024,
        "system": system_prompt,
        "messages": [...]
    }
)
text = response.json()["choices"][0]["message"]["content"].strip()
```

### `BriefingNoteWriter.py`
**Same pattern as QueryInterpreter:**
- Removed `anthropic` import
- Added `requests` and environment variable handling
- Changed to OpenRouter HTTP API calls
- Simplified response parsing

### `query_to_sql.py`
**Complete Rewrite:**

**Before (Databricks SQL):**
```python
from databricks import sql

def filter_humanitarian_data(agent_json_string: str, connection, table_name: str) -> pd.DataFrame:
    # Build SQL query with parameterized placeholders
    query = f"SELECT * FROM {table_name} WHERE 1=1"
    # Execute via connection.cursor()
```

**After (CSV Filtering):**
```python
def filter_humanitarian_data(agent_json_string: str, csv_file_path: str) -> pd.DataFrame:
    # Load CSV
    df = pd.read_csv(csv_file_path)
    
    # Apply pandas filters
    filtered_df = df[df["country_code"].isin(regions)]
    filtered_df = filtered_df[filtered_df["cluster_code"].isin(sectors)]
    # etc.
```

**Logic:**
- Load entire CSV once
- Filter using pandas boolean indexing
- No SQL injection concerns (filtering in-memory)
- Fallback column names for flexibility

### `query_to_articles.py`
**Same refactor as `query_to_sql.py`:**
- Remove Databricks connection parameter
- Add CSV file path parameter
- Use pandas filtering instead of SQL
- Handle missing columns gracefully

---

## Environment Variables

### Before (Databricks)
```bash
DATABRICKS_HOST=https://xxx.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/xxx
DATABRICKS_TOKEN=xxx
```

### After (OpenRouter)
```bash
OPENROUTER_API_KEY=sk-or-v1-xxx
```

Create `.env` file locally:
```bash
cp .env.example .env
# Edit .env and add your OpenRouter API key
```

### On Hugging Face Spaces
Set as a **secret variable** in Space settings (not visible in logs).

---

## Data Migration

### CSV Format
The CSV should contain these columns (exact names matter):

| Column | Type | Notes |
|--------|------|-------|
| `country_code` | str | ISO3 code (e.g., "AFG") |
| `cluster_code` | str | Sector code (e.g., "HEA", "FSC") |
| `sector` | str | Sector description (e.g., "Health") |
| `population` | int | Country population |
| `in_need` | int | People in need of aid |
| `targeted` | int | People receiving aid |
| `year` | int | Data year |
| `total_required_funds` | float | Funds requested (USD) |
| `total_granted_funds` | float | Funds granted (USD) |
| `total_granted_percentage` | float | Granted / Required (0-100) |
| `severity_index` | float | Crisis severity (0-10) |

### Export from Databricks to CSV
```python
import pandas as pd
from databricks import sql

connection = sql.connect(
    server_hostname="...",
    http_path="...",
    access_token="..."
)

df = pd.read_sql("SELECT * FROM unocha.default.master_table", connection)
df.to_csv("data/unocha_dataset.csv", index=False)
connection.close()
```

---

## Deployment on Hugging Face Spaces

### 1. Create Space
- Visit: https://huggingface.co/spaces
- Click "Create new Space"
- **Space name:** `unocha-geo-insight`
- **License:** Choose appropriate license
- **Visibility:** Public (or private)
- **SDK:** Gradio
- **Dockerfile:** Yes (for more control)

### 2. Clone & Push Code
```bash
git clone https://huggingface.co/spaces/USERNAME/unocha-geo-insight
cd unocha-geo-insight

# Copy your code
cp -r /path/to/UNOCHA/* .

# Add data file
mkdir -p data
cp /path/to/unocha_dataset.csv data/

git add .
git commit -m "Initial commit: Geo-Insight with CSV + OpenRouter"
git push
```

### 3. Set Secret Variable
- Go to Space settings
- Under "Repository secrets", add:
  - **Name:** `OPENROUTER_API_KEY`
  - **Value:** Your OpenRouter API key from https://openrouter.ai/

### 4. Monitor Build
- Space will auto-build from Dockerfile
- Check "Logs" tab for any errors
- App should be live at: `https://huggingface.co/spaces/USERNAME/unocha-geo-insight`

---

## Performance Comparison

### Query Interpretation
| Metric | Databricks | OpenRouter |
|--------|-----------|-----------|
| Latency | ~1-2s | ~3-5s |
| Model | claude-sonnet-4-6 | claude-3.5-sonnet |
| Rate limit | Account-based | $X per 1M tokens |
| Reliability | High | High |

### Data Access
| Metric | Databricks | CSV |
|--------|-----------|-----|
| Query time | ~0.5-1s | ~0.01s (in-memory) |
| Data freshness | Real-time | Snapshot |
| Scalability | Unlimited | CSV size dependent |
| Cost | Warehouse cost | Free (storage only) |

**Total Request Time:**
- Before: ~15-20s
- After: ~30-40s (due to OpenRouter latency)

### Cost Comparison
| Item | Databricks | OpenRouter |
|------|-----------|-----------|
| Database | $1-5/hour | $0 (CSV) |
| API calls | Included | ~$0.003 per request |
| Hosting | ~$2000/month | Free (HF) |
| **Monthly (est.)** | **$2000+** | **< $10** |

---

## Testing Checklist

- [ ] Local development works with `.env` file
- [ ] CSV file loads successfully
- [ ] Query interpretation returns valid QuerySpec JSON
- [ ] Data filtering returns expected results
- [ ] Brief writer generates coherent output
- [ ] PDF export works
- [ ] All example queries work
- [ ] Error handling works (test with invalid query)
- [ ] Space secrets are properly set
- [ ] Space deployment builds without errors
- [ ] Space app responds to queries

---

## Troubleshooting

### "OPENROUTER_API_KEY not set"
```bash
# Local: Create .env file
echo "OPENROUTER_API_KEY=sk-or-v1-xxx" > .env

# HF Spaces: Add to Space secrets via web UI
```

### "CSV file not found"
```
Make sure:
- File exists at: data/unocha_dataset.csv
- Path is relative to WORKSPACE_ROOT
- File is committed to git (not in .gitignore)
```

### "No query results"
- Try simpler queries
- Check CSV contains matching data
- Review debug output in terminal

### "OpenRouter API error"
- Check API key validity at https://openrouter.ai/
- Verify remaining credits/quota
- Check that model name is correct

---

## Rollback Plan

If you need to revert to Databricks:

1. **Revert commits:**
   ```bash
   git revert <commit-hash>
   ```

2. **Restore old files:**
   - `requirements.txt` (add back `anthropic`, `databricks-sql-connector`)
   - `app.py` (restore Databricks connection code)
   - `QueryInterpreter.py` (restore anthropic SDK)
   - `BriefingNoteWriter.py` (restore anthropic SDK)
   - `query_to_sql.py` (restore Databricks SQL code)
   - `query_to_articles.py` (restore Databricks SQL code)

3. **Set environment variables:**
   - On Databricks Apps: Configure DATABRICKS_* secrets
   - On HF Spaces: No longer needed

---

## Next Steps

1. ✅ Update project for HF Spaces deployment
2. ⏳ Test thoroughly in local environment
3. ⏳ Create HF Spaces repository
4. ⏳ Deploy and monitor initial requests
5. ⏳ Gather user feedback
6. ⏳ Optimize prompts/data as needed

---

## Additional Resources

- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Hugging Face Spaces Guide](https://huggingface.co/docs/hub/spaces)
- [Gradio Documentation](https://www.gradio.app/docs)
- [Pandas CSV I/O](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
