# CareerViet Enhanced Automation - README

## 🎯 Features

### 1. External Task File
- Task stored in `tasks/careerviet_task.txt`
- Easy to modify without touching code
- Just edit the text file and run

### 2. Multiple API Keys with Auto-Retry
- Configure multiple API keys in `tasks/api_keys.txt`
- Automatic fallback if one key fails
- No interruption - seamlessly switches to next key

### 3. Flexible Configuration
- Works locally (visible browser) or headless (GitHub Actions)
- Environment variable support
- File-based or env-based configuration

---

## 📁 File Structure

```
browser-use-crontab/
├── tasks/
│   ├── careerviet_task.txt      # Task description (EDIT THIS)
│   └── api_keys.txt              # API keys (EDIT THIS)
├── careerviet_enhanced.py        # Main script
└── results/                      # Auto-generated results
```

---

## 🚀 Quick Start

### 1. Configure Task

Edit `tasks/careerviet_task.txt`:
```
Truy cập trang https://careerviet.vn

Đăng nhập với:
- Email: your-email@gmail.com
- Mật khẩu: your-password

... (modify as needed)
```

### 2. Configure API Keys

Edit `tasks/api_keys.txt`:
```
# Primary key
GOOGLE_API_KEY_1=AIzaSy...your-key-1

# Backup key
GOOGLE_API_KEY_2=AIzaSy...your-key-2

# Additional backup
GOOGLE_API_KEY_3=AIzaSy...your-key-3
```

### 3. Run

**Local (visible browser):**
```bash
cd browser-use-crontab
python3.11 careerviet_enhanced.py
```

**Headless:**
```bash
export HEADLESS=true
python3.11 careerviet_enhanced.py
```

---

## ⚙️ Configuration Options

### Option 1: File-Based (Recommended)

**Task:** `tasks/careerviet_task.txt`
**API Keys:** `tasks/api_keys.txt`

**Pros:**
- Easy to edit
- Version control friendly
- No environment setup needed

### Option 2: Environment Variables

```bash
export GOOGLE_API_KEY_1="your-key-1"
export GOOGLE_API_KEY_2="your-key-2"
export GOOGLE_API_KEY_3="your-key-3"
export HEADLESS=true
python3.11 careerviet_enhanced.py
```

### Option 3: Mixed

Use files for task, environment for keys:
```bash
export GOOGLE_API_KEY="your-key"
python3.11 careerviet_enhanced.py
```

---

## 🔄 API Key Retry Logic

### How It Works

1. **Try Key #1** → If fails, try Key #2
2. **Try Key #2** → If fails, try Key #3
3. **Try Key #3** → If fails, report error
4. **Success** → Use that key and continue

### Example Output

```
🔑 Attempting with API key #1/3
❌ API key #1 failed: Rate limit exceeded
🔄 Retrying with next API key...

🔑 Attempting with API key #2/3
✅ Success with API key #2!
```

### Benefits

- **No interruption** - Automatic failover
- **Rate limit protection** - Switch when limit hit
- **Redundancy** - Multiple backup keys
- **Cost optimization** - Use free tiers across keys

---

## 📝 Modifying the Task

### Edit Task File

```bash
nano tasks/careerviet_task.txt
```

**Example modifications:**

**Change search keywords:**
```
- Vị trí: "data engineer" hoặc "machine learning"
```

**Change salary:**
```
- Lương: >= 100,000,000 VND
```

**Change credentials:**
```
- Email: different-email@gmail.com
- Mật khẩu: different-password
```

**No code changes needed!** Just save and run.

---

## 🔑 Managing API Keys

### Get Free API Keys

1. Go to https://aistudio.google.com/app/apikey
2. Create new API key
3. Copy and paste into `tasks/api_keys.txt`
4. Repeat for backup keys

### Key Format

```
GOOGLE_API_KEY_1=AIzaSyABC123...
GOOGLE_API_KEY_2=AIzaSyDEF456...
GOOGLE_API_KEY_3=AIzaSyGHI789...
```

**Important:**
- One key per line
- No spaces around `=`
- Remove placeholder text
- Keep keys secret!

---

## 🐛 Troubleshooting

### Task File Not Found

```
FileNotFoundError: Task file not found
```

**Solution:** Create `tasks/careerviet_task.txt`

### No API Keys Found

```
ValueError: No API keys found!
```

**Solutions:**
1. Edit `tasks/api_keys.txt` and add real keys
2. Or set `GOOGLE_API_KEY` environment variable
3. Or set `GOOGLE_API_KEY_1`, `GOOGLE_API_KEY_2`, etc.

### All API Keys Failed

```
⚠️  All 3 API keys failed!
```

**Possible causes:**
- All keys hit rate limit
- All keys expired/invalid
- Network issue

**Solutions:**
- Wait for rate limit reset
- Add more API keys
- Check key validity

---

## 🎯 GitHub Actions Integration

### Update Workflow

Edit `.github/workflows/careerviet-auto-apply.yml`:

```yaml
- name: Run CareerViet automation
  env:
    GOOGLE_API_KEY_1: ${{ secrets.GOOGLE_API_KEY_1 }}
    GOOGLE_API_KEY_2: ${{ secrets.GOOGLE_API_KEY_2 }}
    GOOGLE_API_KEY_3: ${{ secrets.GOOGLE_API_KEY_3 }}
    HEADLESS: true
  run: |
    python careerviet_enhanced.py
```

### Set GitHub Secrets

Add multiple secrets:
- `GOOGLE_API_KEY_1`
- `GOOGLE_API_KEY_2`
- `GOOGLE_API_KEY_3`

---

## ✨ Summary

**Before (Old Version):**
- ❌ Task hardcoded in script
- ❌ Single API key
- ❌ Fails if key has issues
- ❌ Need to edit code to change task

**After (Enhanced Version):**
- ✅ Task in separate file
- ✅ Multiple API keys with retry
- ✅ Automatic failover
- ✅ Edit task without touching code
- ✅ No interruption on key failure

**Just edit the text files and run!** 🚀
