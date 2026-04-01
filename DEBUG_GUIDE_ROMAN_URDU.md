# Social Poster Debug Guide (Roman Urdu)

## 🔧 Jab Error Aaye To Kya Karein

### **Pehla Kaam: Test Chalayein**

```bash
python test_social_poster.py
```

**Ye batayega:**
- Kya Playwright install hai?
- Kya .env file hai?
- Kya LinkedIn credentials set hain?
- Kya folders ban gaye hain?

---

## ❌ Aam Errors Aur Unka Hal

### Error 1: Playwright Nahi Mila

**Error:**
```
ModuleNotFoundError: No module named 'playwright'
```

**Hal:**
```bash
pip install playwright
playwright install chromium
```

---

### Error 2: Browser Start Nahi Hua

**Error:**
```
Executable doesn't exist
Browser launch failed
```

**Hal:**
```bash
playwright install chromium
# Ya phir
python -m playwright install chromium
```

---

### Error 3: Credentials Nahi Milein

**Error:**
```
LinkedIn credentials not found
LINKEDIN_EMAIL not set
```

**Hal:**

`.env` file mein ye add karein:
```env
LINKEDIN_EMAIL=apka.email@example.com
LINKEDIN_PASSWORD=apka_password
SOCIAL_HEADLESS=false
```

---

### Error 4: Folder Nahi Mila

**Error:**
```
FileNotFoundError: 'AI_Employee_Vault\Social_Queue'
```

**Hal:**
```bash
create_social_queue_v2.bat
```

---

## 🔍 Debug Mode Chalane Ka Tareeqa

### Tareeqa 1: Complete Error Dekhein

```bash
python social_poster.py 2> error.txt
type error.txt
```

Error complete save ho jayega `error.txt` mein!

### Tareeqa 2: Debug Batch File

```bash
debug_social_poster.bat
```

Ye automatically error capture karega.

### Tareeqa 3: Verbose Logging

`.env` mein ye set karein:
```env
LOG_LEVEL=DEBUG
SOCIAL_HEADLESS=false
```

Phir chalayein:
```bash
python social_poster.py
```

Sab kuch detail mein dikhega!

---

## 📝 Step-by-Step Debug Kaise Karein

### Step 1: Prerequisites Check

```bash
# Python check
python --version
# 3.8 ya zyada hona chahiye

# Playwright check
python -c "from playwright.sync_api import sync_playwright; print('OK')"
# 'OK' aana chahiye
```

### Step 2: Files Check

```bash
# .env file hai?
dir .env

# Social_Queue folder hai?
dir AI_Employee_Vault\Social_Queue

# Script file hai?
dir social_poster.py
```

### Step 3: Test Script Chalayein

```bash
python test_social_poster.py
```

**Ye batayega:**
- ✓ Kya sahi hai
- ✗ Kya galat hai
- ⚠ Kya warning hai

### Step 4: Logs Dekhein

```bash
type AI_Employee_Vault\Logs\social_poster_*.log
```

Yahaan actual problem likha hoga!

---

## 🚨 Common Problems Aur Solutions

### Problem 1: Import Error

**Dikhai deta hai:**
```
ImportError: cannot import name 'sync_playwright'
```

**Kya karein:**
```bash
pip uninstall playwright
pip install playwright
playwright install chromium
```

### Problem 2: Permission Denied

**Dikhai deta hai:**
```
PermissionError: Access is denied
```

**Kya karein:**
- Command Prompt ko **Run as Administrator** se chalayein
- Antivirus temporarily band karein
- Folder ka path check karein

### Problem 3: Timeout Error

**Dikhai deta hai:**
```
TimeoutError: Timeout 30000ms exceeded
```

**Kya karein:**
- Internet connection check karein
- `.env` mein timeout badhayein:
```env
PLAYWRIGHT_TIMEOUT=60000
```

### Problem 4: Login Fail

**Dikhai deta hai:**
```
Login failed: Invalid credentials
2FA required
```

**Kya karein:**
1. Credentials dobara check karein `.env` mein
2. 2FA temporarily disable karein
3. Browser visible mode mein chalayein:
```env
SOCIAL_HEADLESS=false
```

---

## 🔧 Quick Fix Commands

Sab kuch dobara install karein:

```bash
# Packages install
pip install --upgrade playwright python-dotenv

# Browser install
playwright install chromium

# Folders banayein
create_social_queue_v2.bat

# .env setup
copy .env.example .env
```

Phir `.env` edit karke apne credentials add karein!

---

## 📊 Error Message Samajhne Ka Tareeqa

### Traceback Kya Hota Hai?

Jab ye dikhta hai:
```
Traceback (most recent call last):
  File "social_poster.py", line 123
  ...
  Error: Something went wrong
```

**Matlab:** Koi error hui hai, aur:
- **Akhri line** mein actual problem hai
- **Pehli lines** mein code ka path hai

**Kya dekhein:**
1. **Sabse neeche ki line** padho - wahan error type hai
2. **Line number** dekho - kahan error aaya
3. **Error message** padho - kya galat hua

---

## ✅ Testing Checklist

Har cheez check karein:

- [ ] Python 3.8+ installed
- [ ] Playwright installed: `pip list | findstr playwright`
- [ ] Chromium installed: `playwright install chromium`
- [ ] .env file exists aur credentials set hain
- [ ] Social_Queue folder ban gaya hai
- [ ] social_poster.py file hai
- [ ] Internet connection theek hai

---

## 🎯 Agar Phir Bhi Kaam Na Kare

### Complete Information Collect Karein:

**1. Error Message:**
```bash
python social_poster.py 2> full_error.txt
type full_error.txt
```

**2. Test Results:**
```bash
python test_social_poster.py > test_results.txt
type test_results.txt
```

**3. Environment Info:**
```bash
python --version > env_info.txt
pip list >> env_info.txt
type env_info.txt
```

**4. Log Files:**
```bash
type AI_Employee_Vault\Logs\social_poster_*.log
```

Ye sab information save karein aur share karein!

---

## 💡 Tips Aur Tricks

### Tip 1: Browser Dikhayein
Jab pehli dafa chalayein to browser dikhayein:
```env
SOCIAL_HEADLESS=false
```
Isse aap dekh sakte ho kya ho raha hai!

### Tip 2: Logs Detail Mein
Debug mode on karein:
```env
LOG_LEVEL=DEBUG
```
Har cheez logs mein aajayegi!

### Tip 3: Internet Check
LinkedIn login ke liye internet chahiye:
```bash
ping linkedin.com
```

### Tip 4: Credentials Double Check
`.env` file khol ke dekho:
```bash
notepad .env
```
Kya email/password sahi hai?

---

## 📞 Help Ke Liye Files

Maine ye files banai hain help ke liye:

1. **`test_social_poster.py`**
   - Run karein: `python test_social_poster.py`
   - Configuration check karega

2. **`debug_social_poster.bat`**
   - Run karein: `debug_social_poster.bat`
   - Errors capture karega

3. **`SOCIAL_POSTER_DEBUG.md`**
   - Padho: Complete guide hai

---

## 🚀 Sab Theek Karne Ka Complete Process

Ye steps follow karein agar koi problem ho:

```bash
# 1. Sab packages install karein
pip install --force-reinstall playwright python-dotenv
playwright install chromium

# 2. Folders banayein
create_social_queue_v2.bat

# 3. .env setup
copy .env.example .env
notepad .env
# Yahaan credentials add karein

# 4. Test karein
python test_social_poster.py

# 5. Agar sab OK hai to chalayein
python social_poster.py
```

---

## ❓ FAQ (Frequently Asked Questions)

**Q: Kya har bar browser login hoga?**
A: Nahi! Pehli bar ke baad session save hota hai.

**Q: Kya LinkedIn 2FA se kaam karega?**
A: Pehli bar 2FA code dena hoga, phir save ho jayega.

**Q: Kitne posts kar sakta hoon?**
A: Default: 5 LinkedIn posts per day. `.env` mein badha sakte ho.

**Q: Kya Twitter par bhi post hoga?**
A: Haan! Agar platforms mein `twitter` add karo.

**Q: Browser background mein chal sakta hai?**
A: Haan! `SOCIAL_HEADLESS=true` set karo.

---

## 🎉 Success Message

Agar sab kaam kare to ye dikhega:

```
========================================
Starting Social Media Poster
========================================

[INFO] Social poster started
[INFO] Loading LinkedIn session...
[INFO] Starting browser...
[INFO] Opening LinkedIn...
[INFO] Logging in...
[INFO] Login successful!
[INFO] Scanning Social_Queue/...
[INFO] Found 1 post
[INFO] Posting to LinkedIn...
[INFO] ✓ Posted successfully!
[INFO] Moved to Posted/
```

LinkedIn pe check karo - post dikhai dega! 🎊

---

**Koi aur sawal? Poochein! 😊**

**Quick Commands Yaad Rakho:**
```bash
# Test
python test_social_poster.py

# Debug
debug_social_poster.bat

# Chalao
python social_poster.py
```
