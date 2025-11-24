# CareerViet Auto Apply - GitHub Actions Setup

## 🎯 Overview

This workflow automatically applies to management jobs on CareerViet every day using GitHub Actions.

## 🚀 Setup Instructions

### 1. Set GitHub Secrets

Go to your repository → Settings → Secrets and variables → Actions → New repository secret

Add the following secret:
- **Name:** `GOOGLE_API_KEY`
- **Value:** Your Google Gemini API key

Get a free API key at: https://aistudio.google.com/app/apikey

### 2. Enable GitHub Actions

1. Go to the **Actions** tab in your repository
2. Click **"I understand my workflows, go ahead and enable them"**
3. Find the **"CareerViet Auto Apply"** workflow

### 3. Test the Workflow

**Manual Test:**
1. Go to Actions → CareerViet Auto Apply
2. Click **"Run workflow"** → **"Run workflow"**
3. Wait for completion (~10-15 minutes)
4. Check the results in **Artifacts**

**Automatic Schedule:**
- Runs every day at **9 AM Vietnam time** (2 AM UTC)
- You can modify the schedule in `.github/workflows/careerviet-auto-apply.yml`

## 📊 How It Works

### Workflow Steps

1. **Checkout code** - Gets your repository code
2. **Set up Python 3.11** - Installs Python
3. **Install uv** - Fast Python package installer
4. **Install dependencies** - Installs browser-use, Playwright, etc.
5. **Install Playwright browsers** - Installs Chromium for headless browsing
6. **Run automation** - Executes the job application script
7. **Upload results** - Saves results as artifacts

### Automation Process

The script will:
1. ✅ Login to CareerViet with your credentials
2. ✅ Search for "quan ly" (management) positions
3. ✅ Filter by salary >= 50,000,000 VND ($2000 USD)
4. ✅ Apply to ALL matching jobs automatically
5. ✅ Continue until daily limit is reached
6. ✅ Save results to artifacts

## 📁 Results

After each run, check the **Artifacts** section:
- `careerviet-results-{run_number}` - Contains:
  - `results/careerviet_YYYYMMDD_HHMMSS.txt` - Execution results
  - `*.log` - Detailed logs

## ⚙️ Configuration

### Change Schedule

Edit `.github/workflows/careerviet-auto-apply.yml`:

```yaml
on:
  schedule:
    # Run at 9 AM Vietnam time (2 AM UTC)
    - cron: '0 2 * * *'
```

**Common schedules:**
- Every day at 9 AM: `'0 2 * * *'`
- Every Monday at 9 AM: `'0 2 * * 1'`
- Twice daily (9 AM & 6 PM): `'0 2,11 * * *'`

Use https://crontab.guru/ to create custom schedules.

### Modify Search Criteria

Edit `Upgrade/careerviet_gemini_headless.py`:

```python
task = """
    ...
    Tìm kiếm:
    - Vị trí: "your keywords here"
    - Lương: >= your_salary_requirement
    ...
"""
```

## 🔒 Security

### Credentials

**NEVER commit credentials to the repository!**

✅ **Correct:** Use GitHub Secrets
```yaml
env:
  GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
```

❌ **Wrong:** Hardcode in files
```python
api_key = "AIza..."  # DON'T DO THIS!
```

### Account Safety

The CareerViet credentials are **hardcoded in the script** for this example. For production:

1. **Option 1:** Add as GitHub Secrets
   ```yaml
   env:
     CAREERVIET_EMAIL: ${{ secrets.CAREERVIET_EMAIL }}
     CAREERVIET_PASSWORD: ${{ secrets.CAREERVIET_PASSWORD }}
   ```

2. **Option 2:** Use environment variables in script
   ```python
   email = os.getenv("CAREERVIET_EMAIL")
   password = os.getenv("CAREERVIET_PASSWORD")
   ```

## 🐛 Troubleshooting

### Workflow Fails

**Check logs:**
1. Go to Actions → Failed workflow
2. Click on the job
3. Expand each step to see errors

**Common issues:**

| Error | Solution |
|-------|----------|
| `GOOGLE_API_KEY not set` | Add secret in repository settings |
| `playwright install failed` | Check Ubuntu compatibility |
| `Login failed` | Verify CareerViet credentials |
| `Timeout` | Increase `max_steps` in script |

### No Jobs Applied

Possible reasons:
- Daily application limit already reached
- No jobs match the criteria
- Website structure changed

Check the artifacts for detailed logs.

### Rate Limiting

If you get rate limited:
- Reduce frequency (run less often)
- Add delays between applications
- Use different accounts

## 💡 Tips

### 1. Test Locally First

Before running in GitHub Actions:
```bash
cd /Users/apple/browseruse/browser-use
python3.11 Upgrade/careerviet_gemini_headless.py
```

### 2. Monitor Results

Set up notifications:
- GitHub Actions → Settings → Notifications
- Get email alerts on workflow failures

### 3. Optimize Costs

**GitHub Actions (Free tier):**
- Public repos: Unlimited minutes
- Private repos: 2,000 minutes/month
- Each run: ~10-15 minutes

**Gemini API (Free tier):**
- 1,500 requests/day
- Each run: ~50-100 requests

### 4. Backup Strategy

If GitHub Actions fails:
- Run locally as backup
- Use multiple automation methods
- Keep manual application as fallback

## 📈 Advanced Features

### Multiple Accounts

Create separate workflows for different accounts:
```yaml
# .github/workflows/careerviet-account1.yml
# .github/workflows/careerviet-account2.yml
```

### Parallel Jobs

Apply to multiple job boards simultaneously:
```yaml
jobs:
  careerviet:
    runs-on: ubuntu-latest
    ...
  
  vietnamworks:
    runs-on: ubuntu-latest
    ...
```

### Conditional Execution

Run only on weekdays:
```yaml
on:
  schedule:
    - cron: '0 2 * * 1-5'  # Monday to Friday
```

## 🔗 Resources

- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **Cron Syntax:** https://crontab.guru/
- **Browser-Use Docs:** https://docs.browser-use.com
- **Gemini API:** https://aistudio.google.com/

## ✨ Summary

You now have a **fully automated job application system** that:

✅ Runs daily in GitHub Actions (headless)  
✅ Applies to management jobs automatically  
✅ Handles login, search, filtering, and applications  
✅ Saves results for review  
✅ Costs $0 (free tiers)  
✅ Requires zero manual intervention  

**Set it and forget it!** 🚀
