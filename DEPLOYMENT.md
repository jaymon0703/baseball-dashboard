# Deploying Your Baseball Dashboard to shinyapps.io

This guide will walk you through deploying your Shiny for Python dashboard to shinyapps.io so you can share it with the world!

---

## Prerequisites

- Your dashboard is working locally
- A GitHub account (optional but recommended)
- A shinyapps.io account (free tier available)

---

## Step 1: Create a shinyapps.io Account

1. Go to [shinyapps.io](https://www.shinyapps.io/)
2. Click "Sign Up" (it's free!)
3. Choose an account name (this will be part of your app URL)
4. Verify your email

---

## Step 2: Install rsconnect-python

The `rsconnect-python` package is needed to deploy Shiny apps. Install it:

```bash
pip install rsconnect-python
```

Or add it to your requirements.txt (though it's only needed for deployment, not running the app).

---

## Step 3: Get Your Deployment Token

1. Log in to [shinyapps.io](https://www.shinyapps.io/)
2. Go to **Account** → **Tokens**
3. Click **Add Token**
4. Give it a name (e.g., "My Computer")
5. Copy the command that looks like:

```bash
rsconnect add --account YOUR_ACCOUNT_NAME --name YOUR_TOKEN_NAME --token YOUR_TOKEN --secret YOUR_SECRET
```

---

## Step 4: Configure rsconnect

Run the command you copied in your terminal:

```bash
rsconnect add --account YOUR_ACCOUNT_NAME --name YOUR_TOKEN_NAME --token YOUR_TOKEN --secret YOUR_SECRET
```

This links your computer to your shinyapps.io account.

---

## Step 5: Prepare Your App for Deployment

Make sure your project has:

1. **app.py** - Your main application file
2. **requirements.txt** - All dependencies listed

Your `requirements.txt` should look like:

```txt
shiny>=0.9.0
shinywidgets>=0.1.0
pybaseball>=2.2.0
pandas>=2.0.0
plotly>=5.0.0
numpy>=1.24.0
requests>=2.30.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
```

**Important**: Make sure your `app.py` has this at the bottom:

```python
app = App(app_ui, server)
```

This is required for deployment!

---

## Step 6: Deploy Your App

Navigate to your project directory and run:

```bash
rsconnect deploy shiny . --name baseball-dashboard --title "Baseball Stats Dashboard"
```

Replace:
- `baseball-dashboard` with your desired app name (lowercase, no spaces)
- `"Baseball Stats Dashboard"` with your desired title

The `.` means "current directory"

---

## Step 7: Access Your Deployed App

Once deployment completes, your app will be available at:

```
https://YOUR_ACCOUNT_NAME.shinyapps.io/baseball-dashboard/
```

Share this URL with anyone!

---

## Updating Your App

To update your deployed app, just run the deploy command again:

```bash
rsconnect deploy shiny . --name baseball-dashboard --title "Baseball Stats Dashboard"
```

It will update the existing app with your latest changes.

---

## Troubleshooting

### "Module not found" errors
- Make sure all dependencies are in `requirements.txt`
- Check that package versions are compatible

### Deployment fails
- Check that `app.py` has `app = App(app_ui, server)` at the bottom
- Ensure all file paths are relative (not absolute)
- Check the shinyapps.io dashboard for error logs

### App runs locally but not online
- Some packages may not be available on shinyapps.io
- Check the deployment logs for specific errors
- Test with a minimal version first

### Slow loading
- Data fetching can be slow on first load
- Consider pre-loading common data
- Use caching effectively

---

## Free Tier Limits

The free shinyapps.io tier includes:
- 5 applications
- 25 hours of usage per month
- Shared resources

This is perfect for learning and sharing your projects!

---

## Next Steps

Once deployed:
1. Share the URL on social media
2. Add it to your GitHub README
3. Include it in your blog post
4. Show it off to friends and family!

---

## Alternative: Deploy to Other Platforms

You can also deploy to:
- **Streamlit Cloud** (if you switch to Streamlit)
- **Heroku** (more complex setup)
- **DigitalOcean** (requires server management)
- **Your own server** (full control)

But shinyapps.io is the easiest for Shiny apps!

---

Happy deploying! 🚀

