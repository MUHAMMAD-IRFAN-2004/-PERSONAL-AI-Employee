# Social Poster Troubleshooting Guide
# Error اور Debug مسائل کا حل

## سب سے عام Errors اور Solutions

### Error 1: Playwright Not Installed

**Error Message:**
```
ERROR: playwright not installed. Run: pip install playwright
Then run: playwright install chromium
```

**حل (Solution):**
```bash
pip install playwright
playwright install chromium
```

---

### Error 2: Browser Launch Failed

**Error Message:**
```
Failed to start browser
Executable doesn't exist at ...
```

**حل:**
```bash
# Chromium browser install کریں
playwright install chromium

# یا complete installation
python -m playwright install
```

---

### Error 3: Login Credentials Missing

**Error Message:**
```
ERROR: LinkedIn credentials not found in .env
ERROR: LINKEDIN_EMAIL or LINKEDIN_PASSWORD not set
```

**حل:**

`.env` file میں یہ add کریں:
```env
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password_here
```

---

### Error 4: Social_Queue Folder Not Found

**Error Message:**
```
FileNotFoundError: [WinError 3] The system cannot find the path specified:
'AI_Employee_Vault\\Social_Queue'
```

**حل:**
```bash
# Folders بنائیں
create_social_queue_v2.bat
```

---

### Error 5: Debug/Traceback Errors

**اگر آپ کو یہ دیکھ رہے ہیں:**
```
Traceback (most recent call last):
  File "social_poster.py", line X, in <function>
  ...
```

**یہ کریں:**

1. **Complete error message copy کریں:**
   ```bash
   python social_poster.py 2> error.txt
   ```

2. **Error file کھولیں:**
   ```bash
   type error.txt
   ```

3. **Error کی آخری lines دیکھیں** - وہاں actual problem ہوگا

---

## Debug Mode چلانے کا طریقہ

### Method 1: Verbose Logging

`.env` میں یہ set کریں:
```env
LOG_LEVEL=DEBUG
SOCIAL_HEADLESS=false    # Browser دیکھنے کے لیے
```

پھر چلائیں:
```bash
python social_poster.py
```

### Method 2: Direct Error Capture

```bash
python social_poster.py > output.log 2>&1
type output.log
```

### Method 3: Debug Batch Script

```bash
debug_social_poster.bat
```

یہ automatically error save کرے گا

---

## Common Debug Errors کی List

### 1. Import Errors

**Error:**
```python
ImportError: cannot import name 'sync_playwright'
ModuleNotFoundError: No module named 'playwright'
```

**حل:**
```bash
pip install playwright
pip install python-dotenv
```

### 2. Permission Errors

**Error:**
```
PermissionError: [WinError 5] Access is denied
```

**حل:**
- Administrator mode سے run کریں
- Antivirus temporarily disable کریں
- Folder permissions check کریں

### 3. Timeout Errors

**Error:**
```
TimeoutError: Timeout 30000ms exceeded
```

**حل:**

`.env` میں timeout بڑھائیں:
```env
PLAYWRIGHT_TIMEOUT=60000
```

یا internet connection check کریں

### 4. Login Failed

**Error:**
```
Login failed: Invalid credentials
Login failed: 2FA required
```

**حل:**
- Credentials دوبارہ check کریں
- 2FA temporarily disable کریں
- Browser manually open کریں (`SOCIAL_HEADLESS=false`)

---

## Step-by-Step Debug Process

### Step 1: Check Prerequisites

```bash
# Python check
python --version

# Playwright check
python -c "from playwright.sync_api import sync_playwright; print('OK')"

# Chromium check
playwright install chromium --dry-run
```

### Step 2: Check Files

```bash
# .env file exists?
dir .env

# Social_Queue exists?
dir AI_Employee_Vault\Social_Queue

# Script exists?
dir social_poster.py
```

### Step 3: Run with Debug

```bash
# Debug mode میں چلائیں
set LOG_LEVEL=DEBUG
python social_poster.py
```

### Step 4: Check Logs

```bash
# Latest log دیکھیں
type AI_Employee_Vault\Logs\social_poster_*.log
```

---

## Error Messages Guide (Urdu)

| Error | مطلب | حل |
|-------|------|-----|
| `ModuleNotFoundError` | Package install نہیں | `pip install <package>` |
| `FileNotFoundError` | File/Folder نہیں ملی | Path check کریں یا folder بنائیں |
| `PermissionError` | Permission نہیں ہے | Admin mode سے run کریں |
| `TimeoutError` | وقت ختم | Timeout بڑھائیں یا internet check کریں |
| `LoginError` | Login fail ہوا | Credentials check کریں |

---

## Quick Fix Commands

```bash
# سب کچھ دوبارہ install کریں
pip install --upgrade playwright python-dotenv
playwright install chromium

# Folders دوبارہ بنائیں
create_social_queue_v2.bat

# .env file setup
copy .env.example .env

# Debug mode میں test کریں
set LOG_LEVEL=DEBUG
set SOCIAL_HEADLESS=false
python social_poster.py
```

---

## Error Reporting Template

اگر مسئلہ حل نہ ہو تو یہ information share کریں:

**1. Error Message:**
```
[یہاں complete error paste کریں]
```

**2. Last Log Lines:**
```bash
type AI_Employee_Vault\Logs\social_poster_*.log | more +n -10
```

**3. Environment:**
```bash
python --version
pip list | findstr playwright
dir .env
```

**4. What you did:**
- کونسا command run کیا
- کیا error آیا
- کیا expect کر رہے تھے

---

## Testing Script

**File:** `test_social_poster.py`

```python
"""Test if social poster is properly configured"""

import sys
from pathlib import Path

print("=" * 50)
print("Social Poster Configuration Test")
print("=" * 50)
print()

errors = []

# Check 1: Playwright
try:
    from playwright.sync_api import sync_playwright
    print("✓ Playwright installed")
except ImportError:
    errors.append("✗ Playwright not installed")
    print(errors[-1])

# Check 2: dotenv
try:
    from dotenv import load_dotenv
    print("✓ python-dotenv installed")
except ImportError:
    errors.append("✗ python-dotenv not installed")
    print(errors[-1])

# Check 3: .env file
if Path('.env').exists():
    print("✓ .env file exists")
else:
    errors.append("✗ .env file missing")
    print(errors[-1])

# Check 4: Social_Queue folder
queue_path = Path('AI_Employee_Vault/Social_Queue')
if queue_path.exists():
    print("✓ Social_Queue folder exists")
else:
    errors.append("✗ Social_Queue folder missing")
    print(errors[-1])

# Check 5: Credentials
if Path('.env').exists():
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    if os.getenv('LINKEDIN_EMAIL'):
        print("✓ LinkedIn email configured")
    else:
        errors.append("✗ LinkedIn email not in .env")
        print(errors[-1])
    
    if os.getenv('LINKEDIN_PASSWORD'):
        print("✓ LinkedIn password configured")
    else:
        errors.append("✗ LinkedIn password not in .env")
        print(errors[-1])

print()
print("=" * 50)

if errors:
    print("❌ Configuration Issues Found:")
    for error in errors:
        print(f"  {error}")
    print()
    print("Please fix these issues before running social_poster.py")
    sys.exit(1)
else:
    print("✅ All checks passed!")
    print("You can run: python social_poster.py")
    print()

```

**Run test:**
```bash
python test_social_poster.py
```

---

## Browser Specific Issues

### Chrome/Chromium Not Found

**Error:**
```
browserType.launchPersistentContext: Executable doesn't exist at
```

**حل:**
```bash
# Specific path پر install کریں
playwright install chromium --with-deps

# یا manual download
python -m playwright install chromium
```

### Browser Crashes

**Error:**
```
Browser closed unexpectedly
```

**حل:**
```bash
# Browser session clear کریں
rmdir /s /q .social_browser_data

# دوبارہ login کریں
python social_poster.py
```

---

## Contact کے لیے

اگر error solve نہ ہو:

1. **Complete error message** save کریں
2. **Log file** دیکھیں
3. **Test script** چلائیں
4. سب information share کریں

---

**Quick Debug Commands:**

```bash
# Full diagnosis
python test_social_poster.py

# Debug mode
debug_social_poster.bat

# Check logs
type AI_Employee_Vault\Logs\social_poster_*.log

# Reinstall everything
pip install --force-reinstall playwright python-dotenv
playwright install chromium
```
