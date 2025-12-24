# Deployment Checklist for shinyapps.io

Use this checklist before deploying your app.

## Pre-Deployment Checklist

- [ ] App runs locally without errors
- [ ] `app.py` has `app = App(app_ui, server)` at the bottom
- [ ] `requirements.txt` includes all dependencies
- [ ] All file paths are relative (not absolute)
- [ ] No hardcoded local file paths
- [ ] Tested with sample data

## Files Needed for Deployment

- [x] `app.py` - Main application file
- [x] `requirements.txt` - All Python dependencies
- [ ] `.gitignore` - Optional but recommended

## Deployment Steps

1. [ ] Create shinyapps.io account
2. [ ] Install `rsconnect-python`: `pip install rsconnect-python`
3. [ ] Get deployment token from shinyapps.io
4. [ ] Run: `rsconnect add --account YOUR_ACCOUNT --name NAME --token TOKEN --secret SECRET`
5. [ ] Deploy: `rsconnect deploy shiny . --name baseball-dashboard --title "Baseball Stats Dashboard"`
6. [ ] Test the deployed app
7. [ ] Share the URL!

## Common Issues

### Issue: "Module not found"
**Solution**: Add missing package to `requirements.txt`

### Issue: Deployment fails
**Solution**: 
- Check that `app = App(app_ui, server)` is at the bottom of `app.py`
- Verify all imports work
- Check deployment logs on shinyapps.io

### Issue: App is slow
**Solution**: 
- Data fetching takes time on first load
- Consider adding loading indicators
- Use caching effectively

## After Deployment

- [ ] Test all features work online
- [ ] Share URL in your article
- [ ] Add to GitHub README
- [ ] Update if you make changes

---

**Ready to deploy?** Follow the steps in `DEPLOYMENT.md`!

