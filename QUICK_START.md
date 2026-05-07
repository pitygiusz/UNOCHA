# 🚀 Quick Start Guide

Rozpocznij pracę z UNOCHA Geo-Insight w 5 minut!

## Option 1: Local Development (Fastest)

### Step 1: Clone & Setup
```bash
# Navigate to project directory
cd UNOCHA

# Run setup script
./setup.sh

# Follow prompts to add OpenRouter API key to .env
```

### Step 2: Run
```bash
# Activate venv
source venv/bin/activate

# Start the app
python geo-insight/src/app.py
```

### Step 3: Use
- Open browser to http://localhost:7860
- Try a query: `"Show underfunded food crises in the Sahel"`
- Results appear in 30-40 seconds
- Click "Save as PDF" to export

## Option 2: Docker (Recommended for Production)

```bash
# Build image
docker build -t geo-insight .

# Run container
docker run -p 7860:7860 \
  -e OPENROUTER_API_KEY="sk-or-v1-your-key" \
  -v $(pwd)/data:/app/data \
  geo-insight
```

Visit: http://localhost:7860

## Option 3: Hugging Face Spaces (Cloud Deployment)

See [HF_SPACES_README.md](./geo-insight/HF_SPACES_README.md) for full guide.

Quick summary:
1. Create Space at https://huggingface.co/spaces
2. Add `OPENROUTER_API_KEY` secret
3. Push code to HF Space repo
4. App auto-deploys in 5-10 minutes

---

## 🔑 Get Your API Key

1. Go to https://openrouter.ai/
2. Sign up (free account)
3. Create API key
4. Add to `.env`: `OPENROUTER_API_KEY=sk-or-v1-...`

**Cost**: ~$0.003 per request (~$10/month for typical usage)

---

## 📊 Test Your Setup

```bash
# Validate installation
python test_setup.py
```

All tests should pass with ✓ marks.

---

## 🎯 Example Queries

Copy & paste into the app:

```
"Show underfunded food crises in the Sahel since 2022"
```

```
"Current humanitarian needs in Middle East"
```

```
"Countries with highest severity but lowest funding"
```

```
"Protection sector crises in Africa"
```

```
"Recent emergencies with critical funding gaps"
```

---

## ⚡ What Happens

1. **Query** → Natural language question
2. **Interpret** → Claude AI parses your query (3-5 sec)
3. **Filter** → Data from CSV matching your criteria
4. **Generate** → AI writes professional briefing note (10-20 sec)
5. **Export** → Display results + PDF export option

**Total time**: ~30-40 seconds per request

---

## 🔧 Troubleshooting

### "OPENROUTER_API_KEY not set"
```bash
# Make sure .env exists and has your key
cat .env | grep OPENROUTER_API_KEY

# If missing, edit .env:
nano .env
# Add: OPENROUTER_API_KEY=sk-or-v1-...
```

### "CSV file not found"
```bash
# Check file exists
ls -lh data/unocha_dataset.csv

# Should show: 7,610 records humanitarian data
```

### "No results from query"
- Try simpler query with fewer filters
- Check CSV contains matching data
- Try: `"Show all humanitarian data for Afghanistan"`

### "API error / timeout"
- Check internet connection
- Verify API key is valid at https://openrouter.ai/
- Check OpenRouter status page
- May need to wait 30-60 seconds between requests

---

## 📚 Learn More

- **Full deployment**: [HF_SPACES_README.md](./geo-insight/HF_SPACES_README.md)
- **Technical details**: [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md)
- **Deployment steps**: [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)
- **What changed**: [REFACTORING_SUMMARY.md](./REFACTORING_SUMMARY.md)

---

## 💾 Project Structure

```
UNOCHA/
├── data/
│   └── unocha_dataset.csv          ← 7,600+ records
├── geo-insight/
│   ├── src/
│   │   ├── app.py                  ← Main app (run this!)
│   │   └── requirements.txt
│   └── .env.example                ← Copy to .env
├── .env                            ← Your secrets (don't commit!)
├── setup.sh                        ← Run this first
├── Dockerfile                      ← For Docker/HF
└── README.md                       ← Full documentation
```

---

## ✅ Checklist

- [ ] Clone repository
- [ ] Run `./setup.sh`
- [ ] Add OPENROUTER_API_KEY to `.env`
- [ ] Run `python test_setup.py` (all green ✓)
- [ ] Start app: `python geo-insight/src/app.py`
- [ ] Open browser: http://localhost:7860
- [ ] Try example query
- [ ] See briefing note appear!

---

## 🚀 Next Steps

### Local Testing
1. Test with different queries
2. Check PDF export works
3. Review debug output in terminal

### Deploy to Cloud
1. Follow [HF_SPACES_README.md](./geo-insight/HF_SPACES_README.md)
2. Set up Space on Hugging Face
3. Share URL with team

### Customize
1. Edit prompts in `geo-insight/src/prompts/`
2. Update CSV data in `data/unocha_dataset.csv`
3. Adjust styling in `app.py` CSS section

---

## 🆘 Need Help?

### Quick Links
- **API Help**: https://openrouter.ai/docs
- **HF Spaces**: https://huggingface.co/docs/hub/spaces
- **Gradio**: https://www.gradio.app/docs

### Check These Docs
1. `README.md` - Overview
2. `HF_SPACES_README.md` - Cloud deployment
3. `MIGRATION_GUIDE.md` - Technical details
4. `DEPLOYMENT_CHECKLIST.md` - Step-by-step guide

### Run Tests
```bash
python test_setup.py
```

---

**Ready?** Run `./setup.sh` and start querying!

Updated: May 2026  
Quick Start v1.0
