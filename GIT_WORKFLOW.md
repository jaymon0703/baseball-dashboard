# Git Workflow for Article Deployment

## Recommended Approach: Feature Branch

Yes, you should create a feature branch! Here's why and how:

---

## Why Use a Feature Branch?

1. **Keep main branch stable** - Your main branch stays clean and working
2. **Test before merging** - Deploy and test from the feature branch first
3. **Easy rollback** - If something breaks, just switch back to main
4. **Clean history** - Better commit history and organization
5. **Collaboration** - Easier to review changes before merging

---

## Recommended Workflow

### Step 1: Create Feature Branch

```bash
# Make sure you're on main and it's up to date
git checkout main
git pull origin main

# Create and switch to feature branch
git checkout -b feature/article-deployment

# Or with a more descriptive name:
git checkout -b feature/wordpress-article-tutorial
```

### Step 2: Make Your Changes

Add all the article-related files:
- `WORDPRESS_ARTICLE.md`
- `DEPLOYMENT.md`
- `DEPLOYMENT_CHECKLIST.md`
- `ENHANCEMENT_SUGGESTIONS.md`
- Updated `README.md`
- `.gitignore`

```bash
# Stage your changes
git add .

# Commit with descriptive message
git commit -m "Add WordPress article and deployment documentation"
```

### Step 3: Test Locally

```bash
# Make sure app still works
shiny run app.py

# Test that everything is correct
```

### Step 4: Deploy from Feature Branch (Optional)

You can deploy from the feature branch to test:

```bash
# Deploy from current branch
rsconnect deploy shiny . --name baseball-dashboard --title "Baseball Stats Dashboard"
```

**Note**: shinyapps.io deploys from your local directory, not from Git. So the branch doesn't affect deployment directly, but it's good practice to deploy from the feature branch first to test.

### Step 5: Push Feature Branch

```bash
# Push feature branch to GitHub
git push origin feature/article-deployment
```

### Step 6: Merge to Main (After Testing)

Once you've tested the deployment and everything works:

```bash
# Switch back to main
git checkout main

# Merge feature branch
git merge feature/article-deployment

# Push to GitHub
git push origin main
```

### Step 7: Deploy from Main (Final)

```bash
# Now deploy from main branch (your stable version)
rsconnect deploy shiny . --name baseball-dashboard --title "Baseball Stats Dashboard"
```

---

## Alternative: Deploy Directly from Feature Branch

If you want to keep the article version separate for now:

```bash
# Stay on feature branch
git checkout feature/article-deployment

# Deploy from feature branch
rsconnect deploy shiny . --name baseball-dashboard --title "Baseball Stats Dashboard"
```

This way, your deployed app matches your article exactly, and you can merge to main later when ready.

---

## Branch Naming Suggestions

Good branch names:
- `feature/article-deployment`
- `feature/wordpress-tutorial`
- `feature/add-deployment-docs`
- `docs/article-and-deployment`

Avoid:
- `test` (too generic)
- `new-stuff` (not descriptive)
- `fix` (not a fix)

---

## Best Practice Workflow

```
main (stable)
  │
  ├─→ feature/article-deployment (work in progress)
  │     │
  │     ├─→ Test locally
  │     ├─→ Deploy to shinyapps.io (test)
  │     ├─→ Verify everything works
  │     │
  │     └─→ Merge back to main
  │
  └─→ Deploy from main (production)
```

---

## Quick Commands Reference

```bash
# Create feature branch
git checkout -b feature/article-deployment

# Work on changes, commit
git add .
git commit -m "Your message"

# Deploy (from any branch)
rsconnect deploy shiny . --name baseball-dashboard

# Push branch
git push origin feature/article-deployment

# Merge to main (when ready)
git checkout main
git merge feature/article-deployment
git push origin main
```

---

## My Recommendation

**For your situation:**

1. ✅ Create feature branch: `feature/article-deployment`
2. ✅ Commit all article/documentation files
3. ✅ Deploy from feature branch to test
4. ✅ Once verified, merge to main
5. ✅ Deploy from main for "production"

This gives you:
- Clean separation of article work
- Ability to test before merging
- Stable main branch
- Easy to update article version later

---

## Important Note

**shinyapps.io deployment is from your local directory**, not from Git. So:
- The branch you're on doesn't directly affect deployment
- But using a feature branch is still good practice for organization
- You can deploy from any branch - it just uses your local files

The feature branch is more about **code organization** and **testing** than deployment mechanics.

---

Ready to create your feature branch? Run:

```bash
git checkout -b feature/article-deployment
```

Then commit your changes and deploy! 🚀

