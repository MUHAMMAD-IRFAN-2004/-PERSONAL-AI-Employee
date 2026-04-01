# Gmail Token Expired - Fix Guide (Roman Urdu)

## ❌ Problem: Token Expired

**Error dikhai de raha hai:**
```
Authentication failed: Token has been expired or revoked
```

**Matlab:** Gmail ka access token expire ho gaya hai ya revoke kar diya gaya hai.

---

## ✅ Aasan Solution (1 Command)

```bash
fix_gmail_token.bat
```

Ye automatically:
- ✅ Purana token delete karega
- ✅ Gmail watcher chalayega
- ✅ Browser mein authentication karega

---

## 📝 Manual Fix (Step by Step)

### Step 1: Purana Token Delete Karo

```bash
# Backup banao (optional)
copy token.json token.json.backup

# Delete karo
del token.json
```

### Step 2: Gmail Watcher Dobara Chalao

```bash
python gmail_watcher.py
```

### Step 3: Browser Mein Login Karo

**Kya hoga:**

1. **Browser automatic khulega** (Chrome/Firefox)
2. **Google login page dikhega**
3. **Apne Google account se login karo**
4. **Permission screen dikhegi:**
   ```
   Personal AI Employee wants to:
   - Read your emails
   ```
5. **Click "Allow"** ya "Continue"
6. **Success message dikhega!**
7. **Browser band ho jayega**
8. **Gmail Watcher chalna shuru ho jayega** ✅

### Step 4: Verify Token Created

```bash
# Check karo naya token ban gaya
dir token.json
```

**Output:**
```
token.json - XX KB
```

Agar file dikhe to successful! ✅

---

## 🔍 Why Token Expire Hota Hai?

### Common Reasons:

1. **Time se expire** - Tokens automatically 7 days ya zyada baad expire hote hain
2. **Password change** - Google account password change kiya
3. **Security settings** - Google ne revoke kar diya (suspicious activity)
4. **Manual revoke** - Khud permissions revoke kar diye Google account settings se
5. **Refresh token fail** - Refresh token bhi expire ho gaya

---

## 🔧 Complete Fix Process

```bash
# 1. Stop any running Gmail Watcher
# Press Ctrl+C if running

# 2. Delete old token
del token.json

# 3. Verify credentials exist
dir credentials.json

# 4. Run Gmail Watcher
python gmail_watcher.py

# 5. Browser khulega - login karo
# 6. "Allow" click karo
# 7. Done! ✅
```

---

## ⚠️ Agar Browser Nahi Khule

**Problem:** Browser automatically nahi khula

**Solutions:**

### Solution 1: Manual Browser Open

Terminal mein ye dikhega:
```
Please visit this URL to authorize:
https://accounts.google.com/o/oauth2/auth?client_id=...
```

**Copy karo URL aur browser mein paste karo**

### Solution 2: Port Already Used

```bash
# Error: Port 8080 already in use

# Task manager mein dekho koi process use kar raha hai?
# Ya restart karo computer
```

---

## 📋 Token Refresh Process

Gmail API tokens 2 types ke hote hain:

### 1. Access Token
- **Life:** 1 hour
- **Purpose:** Actual API calls
- **Auto-refresh:** Haan

### 2. Refresh Token
- **Life:** 7 days to 6 months (depends on settings)
- **Purpose:** New access token generate karna
- **Auto-refresh:** Nahi

**Jab refresh token expire ho:**
- Manual re-authentication chahiye
- Browser login karna padega
- Nayi token.json banti hai

---

## 🎯 Prevent Future Token Issues

### Tip 1: Gmail Watcher Continuously Chalao

```bash
# Startup mein add karo
# Win+R > shell:startup
# Shortcut rakho start_watcher.bat ka
```

Agar continuously chalta rahe to token refresh hota rehta hai!

### Tip 2: Google Security Settings

1. Go to: https://myaccount.google.com/security
2. **"Less secure app access"** - Allow karo (agar option hai)
3. **"2-Step Verification"** - Optional (lekin recommended)

### Tip 3: Regular Monitoring

```bash
# Har hafte ek bar check karo
python gmail_watcher.py
```

---

## 🔍 Troubleshooting

### Problem 1: credentials.json Invalid

**Error:**
```
credentials.json not found
```

**Solution:**
1. Google Cloud Console: https://console.cloud.google.com
2. Enable Gmail API
3. Create OAuth credentials
4. Download as credentials.json
5. Place in project folder

---

### Problem 2: Scope Changed

**Error:**
```
Token scope mismatch
```

**Solution:**
```bash
# Delete token aur re-authenticate
del token.json
python gmail_watcher.py
```

---

### Problem 3: Multiple Google Accounts

**Problem:** Galat account se login ho raha

**Solution:**
1. Browser mein incognito mode use karo
2. Ya correct account select karo login screen par

---

### Problem 4: "Access Blocked" Message

**Error:**
```
This app is blocked
```

**Solution:**
1. Check OAuth consent screen
2. Add your email as "Test User"
3. Publish app (ya testing mode rakho)

---

## ✅ Success Checklist

Token successfully refresh hua agar:

- [ ] Browser mein Google login screen aaya
- [ ] Successfully login hua
- [ ] "Allow" permissions click kiya
- [ ] Browser automatic close hua
- [ ] `token.json` file ban gayi
- [ ] Gmail Watcher chalna shuru ho gaya
- [ ] Terminal mein ye dikha:
  ```
  ✓ Gmail service initialized
  Checking for new emails...
  ```

---

## 📊 Log Messages - Kya Dikhe To Kya Matlab

### Success Messages:
```
✓ Gmail service initialized          → Theek hai
Checking for new emails...            → Kaam kar raha hai
Found 0 new important emails          → Koi naya email nahi
```

### Warning Messages:
```
Refreshing Gmail API token...         → Token refresh ho raha (normal)
No credentials found                  → credentials.json missing
```

### Error Messages:
```
Token has been expired or revoked     → Token delete karo
Authentication failed                 → Re-authenticate karo
Invalid credentials                   → credentials.json check karo
```

---

## 🚀 Quick Fix Commands

```bash
# Complete reset
del token.json
del token.json.backup
python gmail_watcher.py

# Verify setup
python verify_credentials.py

# Check status
python gmail_watcher.py
# Should see: "Checking for new emails..."
```

---

## 💡 Pro Tips

**Tip 1:** Token.json backup rakho safe jagah par
```bash
copy token.json D:\Backup\token.json.backup
```

**Tip 2:** Auto-restart script banao:
```batch
:retry
python gmail_watcher.py
timeout /t 10
goto retry
```

**Tip 3:** Log monitor karo:
```bash
type AI_Employee_Vault\Logs\gmail_watcher_*.log
```

---

## 📞 Agar Kuch Kaam Na Kare

**Mujhe batao:**
1. Complete error message
2. Browser khula ya nahi?
3. credentials.json hai ya nahi?
4. Google account ka 2FA on hai?

---

## 🎉 Expected Working Output

Jab sab theek ho:

```
Gmail Watcher for AI Employee
==================================================
Vault: AI_Employee_Vault
Credentials: credentials.json
DRY_RUN: True
Check Interval: 120s
==================================================

2026-04-02 03:30:00 - GmailWatcher - INFO - Starting Gmail Watcher
2026-04-02 03:30:01 - GmailWatcher - INFO - ✓ Gmail service initialized
2026-04-02 03:30:01 - GmailWatcher - INFO - Checking for new emails...
2026-04-02 03:30:02 - GmailWatcher - INFO - Found 0 new important emails
2026-04-02 03:30:02 - GmailWatcher - INFO - Waiting 120 seconds...
```

---

**Ab try karo:**

```bash
fix_gmail_token.bat
```

**Phir batao - token refresh ho gaya? Gmail Watcher chal raha hai? 😊**
