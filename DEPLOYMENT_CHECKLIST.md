# Deployment Checklist for Hugging Face Spaces

Użyj tej listy kontrolnej aby wdrożyć projekt na Hugging Face Spaces.

## Pre-Deployment Checklist

### 1. Local Testing
- [ ] Clone repository locally
- [ ] Run `./setup.sh`
- [ ] Run `python test_setup.py`
- [ ] CSV file loads successfully
- [ ] Test query: `python geo-insight/src/app.py`
- [ ] Can make sample queries
- [ ] Results generate without errors
- [ ] PDF export works

### 2. Code Review
- [ ] No hardcoded API keys in code
- [ ] No Databricks imports remain
- [ ] All imports are available in `requirements.txt`
- [ ] `query_to_sql.py` uses CSV instead of SQL
- [ ] `query_to_articles.py` uses CSV instead of SQL
- [ ] `QueryInterpreter.py` uses OpenRouter
- [ ] `BriefingNoteWriter.py` uses OpenRouter
- [ ] All paths are relative (not absolute)
- [ ] `.env` is in `.gitignore`
- [ ] Debug prints are acceptable (good for monitoring)

### 3. Data Preparation
- [ ] CSV file has been validated
- [ ] CSV has all required columns
- [ ] CSV is not corrupted
- [ ] CSV is not too large (check Hugging Face file limits)
- [ ] Column names match code expectations
- [ ] No sensitive data in CSV

### 4. Documentation
- [ ] README.md is updated
- [ ] HF_SPACES_README.md is complete
- [ ] MIGRATION_GUIDE.md documents changes
- [ ] Example queries in README
- [ ] Setup instructions are clear
- [ ] Troubleshooting section exists

## Hugging Face Spaces Setup

### 5. Create Space
- [ ] Go to https://huggingface.co/spaces
- [ ] Click "Create new Space"
- [ ] Enter Space name: `unocha-geo-insight`
- [ ] Select License (choose appropriate one)
- [ ] Set Visibility: Public (or Private)
- [ ] Select SDK: Gradio
- [ ] Select Space SDK version: 4.44.0
- [ ] Check "Use Dockerfile" checkbox
- [ ] Click "Create Space"

### 6. Upload Files
```bash
# Clone Space
git clone https://huggingface.co/spaces/USERNAME/unocha-geo-insight
cd unocha-geo-insight

# Copy files (do this from parent UNOCHA directory)
cp -r ../geo-insight/* .
cp ../data/unocha_dataset.csv data/
cp ../Dockerfile .
cp ../.gitignore .
```

### 7. Configure Space Settings
- [ ] Go to Space Settings (⚙️ icon)
- [ ] Add Secret: `OPENROUTER_API_KEY=sk-or-v1-...`
- [ ] Verify the secret is marked as hidden
- [ ] Keep visibility settings as desired
- [ ] Optional: Add custom README

### 8. Deploy
```bash
# From your local Space clone
git add .
git commit -m "Initial deployment: Geo-Insight with CSV + OpenRouter"
git push
```

- [ ] Monitor build progress (check "Logs" tab)
- [ ] Wait for "Building" status to complete
- [ ] Check for build errors in logs
- [ ] Verify Space is now "Running"

## Post-Deployment Testing

### 9. Initial Testing
- [ ] Space loads successfully (no 500 errors)
- [ ] Interface is visible
- [ ] Text input field is responsive
- [ ] "Send" button works
- [ ] Loading animation appears
- [ ] Results load within 40 seconds
- [ ] Results display correctly
- [ ] No error messages shown

### 10. Functionality Testing
- [ ] Test with example query: "Show underfunded food crises in the Sahel since 2022"
- [ ] Results contain meaningful data
- [ ] Briefing note is well-formatted
- [ ] Data table appears at bottom
- [ ] Test with another query
- [ ] PDF export button works
- [ ] Try invalid query (should handle gracefully)
- [ ] Check debug output in Space logs

### 11. Performance Testing
- [ ] Typical query time: 30-40 seconds ✓
- [ ] No timeouts (usually 10 minutes per request on HF)
- [ ] Memory usage is stable
- [ ] No memory leaks after multiple requests
- [ ] Can handle concurrent users

### 12. Error Handling
- [ ] Test with empty query
- [ ] Test with query that returns no results
- [ ] Test with special characters
- [ ] Test with very long query
- [ ] Check error messages are helpful
- [ ] No stack traces shown to users
- [ ] Error logs appear in Space logs

## Monitoring & Maintenance

### 13. Set Up Monitoring
- [ ] Check Space logs regularly (first week)
- [ ] Monitor API usage on OpenRouter
- [ ] Set up alerts for high usage
- [ ] Document any errors in Space logs
- [ ] Plan for data updates

### 14. Documentation Updates
- [ ] Add Space URL to README
- [ ] Update "Live Demo" link
- [ ] Add troubleshooting based on actual usage
- [ ] Document any known issues
- [ ] Create usage analytics if needed

### 15. Optimization (Optional)
- [ ] Profile slow queries in logs
- [ ] Consider caching if same queries are common
- [ ] Optimize CSV for faster filtering if needed
- [ ] Monitor OpenRouter costs
- [ ] Evaluate if cheaper models work

## Rollback Procedure

### If Something Goes Wrong
1. [ ] Identify the issue in Space logs
2. [ ] Check OpenRouter API status
3. [ ] Test CSV file integrity
4. [ ] Verify secret is set correctly
5. [ ] Delete Space and start over OR
6. [ ] Revert to previous git commit:
   ```bash
   git revert HEAD
   git push
   ```

## Team Communication

- [ ] Notify stakeholders of live deployment
- [ ] Provide Space URL to users
- [ ] Share example queries
- [ ] Explain any limitations
- [ ] Set expectations on performance
- [ ] Provide feedback channel for issues

## Final Verification

- [ ] Space URL works publicly
- [ ] Different browsers tested (Chrome, Firefox, Safari)
- [ ] Mobile view is usable
- [ ] Share with stakeholders for feedback
- [ ] Document any user feedback
- [ ] Plan for future improvements

## Additional Resources

- OpenRouter API: https://openrouter.ai/
- Hugging Face Spaces: https://huggingface.co/spaces
- Gradio Docs: https://www.gradio.app/docs
- Project README: [./README.md](./README.md)
- Migration Guide: [./MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md)

## Notes

Use this section to track deployment-specific notes:

```
Date: ___________
Deployed by: ___________
Workspace URL: ___________
Issues encountered: ___________
Resolution: ___________
Follow-up items: ___________
```

---

**Status**: [ ] Ready for Deployment

**Last Updated**: May 2026

**Verified by**: ___________

Date: ___________
