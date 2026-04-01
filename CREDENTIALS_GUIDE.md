# Gmail API Credentials Guide

## Overview

The `credentials.json` file contains OAuth 2.0 credentials for accessing the Gmail API. This file is required for the Gmail Watcher to monitor your email inbox.

## Current Status

✅ **Your credentials.json is present and properly configured!**

**Configuration Details:**
- **Type:** Desktop/Installed Application
- **Project:** hacthon-0
- **Client ID:** 748578789656-1s2vrnhptfd9h2839oosmaj6o8vjs3g1.apps.googleusercontent.com
- **Redirect URI:** http://localhost (correct for desktop app)

## What is credentials.json?

`credentials.json` is the OAuth 2.0 client configuration file downloaded from Google Cloud Console. It contains:

1. **Client ID** - Identifies your application to Google
2. **Client Secret** - Secret key for OAuth authentication
3. **Auth URI** - Google's OAuth authorization endpoint
4. **Token URI** - Google's token endpoint
5. **Redirect URIs** - Where Google sends the user after authentication

## Security Considerations

### ⚠️ IMPORTANT SECURITY NOTES

1. **Never commit to Git**
   - Already in `.gitignore` ✅
   - Contains sensitive client_secret
   - Should remain local only

2. **Keep secret**
   - Don't share client_secret publicly
   - Don't post in support forums
   - Don't include in screenshots

3. **Limited scope**
   - Currently configured for Gmail read-only access
   - Scope: `https://www.googleapis.com/auth/gmail.readonly`
   - Cannot send emails or modify inbox

## How It Works

### First Run Authentication

**Step 1: Run Gmail Watcher**
```bash
python gmail_watcher.py
```

**Step 2: Browser Opens**
- Google OAuth consent screen appears
- Shows what permissions are requested

**Step 3: Grant Access**
- Select your Google account
- Review permissions (Gmail read-only)
- Click "Allow"

**Step 4: Token Created**
- `token.json` is created
- Contains your access token
- Automatically refreshed when expired

### Subsequent Runs

- Uses existing `token.json`
- No browser authentication needed
- Automatic token refresh
- Runs unattended

## File Structure

### credentials.json (OAuth Client Config)
```json
{
  "installed": {
    "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
    "project_id": "your-project",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "YOUR_CLIENT_SECRET",
    "redirect_uris": ["http://localhost"]
  }
}
```

### token.json (User Access Token)
```json
{
  "token": "ya29.a0AfH6...",
  "refresh_token": "1//0gK...",
  "token_uri": "https://oauth2.googleapis.com/token",
  "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
  "client_secret": "YOUR_CLIENT_SECRET",
  "scopes": ["https://www.googleapis.com/auth/gmail.readonly"]
}
```

## Verification

### Automated Verification

Run the verification script:

```bash
# Windows
verify_credentials.bat

# Or directly with Python
python verify_credentials.py
```

**Checks performed:**
- ✓ File exists
- ✓ Valid JSON format
- ✓ Required fields present
- ✓ Proper structure
- ✓ Redirect URIs configured
- ✓ Python packages installed
- ✓ token.json status

### Manual Verification

**1. Check file exists:**
```bash
dir credentials.json
```

**2. Validate JSON:**
```bash
python -c "import json; print('Valid' if json.load(open('credentials.json')) else 'Invalid')"
```

**3. Check fields:**
```bash
python -c "import json; c=json.load(open('credentials.json')); print('client_id' in c.get('installed', {}))"`
```

## Troubleshooting

### Error: credentials.json not found

**Solution:**
1. Download from Google Cloud Console
2. Place in project root directory
3. Verify filename is exactly `credentials.json`

### Error: Invalid client

**Problem:** Client ID or secret is wrong

**Solution:**
1. Re-download credentials.json from Google Cloud
2. Replace existing file
3. Delete token.json
4. Re-authenticate

### Error: Redirect URI mismatch

**Problem:** Redirect URI in Cloud Console doesn't match credentials.json

**Solution:**
1. Go to Google Cloud Console
2. Navigate to APIs & Services > Credentials
3. Edit OAuth 2.0 Client ID
4. Add `http://localhost` to Authorized redirect URIs
5. Save and re-download credentials.json

### Error: Access denied

**Problem:** User didn't grant permissions

**Solution:**
1. Delete token.json
2. Re-run gmail_watcher.py
3. Complete OAuth flow
4. Click "Allow" on all permissions

### Error: Token expired

**Normal behavior:**
- Tokens expire automatically
- Refresh token used to get new access token
- No re-authentication needed
- If refresh fails, delete token.json and re-authenticate

## Creating New Credentials

If you need to create credentials.json from scratch:

### Step 1: Google Cloud Console

1. Go to https://console.cloud.google.com
2. Create new project or select existing
3. Enable Gmail API:
   - APIs & Services > Library
   - Search "Gmail API"
   - Click "Enable"

### Step 2: Create OAuth Credentials

1. APIs & Services > Credentials
2. Click "Create Credentials"
3. Select "OAuth client ID"
4. Application type: "Desktop app"
5. Name: "Personal AI Employee Gmail Watcher"
6. Click "Create"

### Step 3: Configure OAuth Consent Screen

1. APIs & Services > OAuth consent screen
2. User Type: "External"
3. App name: "Personal AI Employee"
4. Support email: Your email
5. Scopes: Add Gmail readonly scope
6. Test users: Add your email
7. Save

### Step 4: Download Credentials

1. Go to Credentials page
2. Find your OAuth 2.0 Client ID
3. Click download icon (⬇️)
4. Save as `credentials.json`
5. Move to project root directory

## Scopes and Permissions

### Current Scope

```python
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
```

**Allows:**
- ✅ Read emails
- ✅ List messages
- ✅ Get message details
- ✅ Search inbox

**Does NOT allow:**
- ❌ Send emails
- ❌ Delete emails
- ❌ Modify labels
- ❌ Trash messages

### Adding More Scopes

To enable email sending (for future features):

1. Update scope in `gmail_watcher.py`:
```python
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]
```

2. Delete `token.json`
3. Re-authenticate to grant new permissions

## Token Management

### token.json Location

- Created in project root
- Same directory as credentials.json
- Automatically managed by Google Auth library

### Token Refresh

**Automatic:**
- Happens transparently
- Uses refresh_token
- No user intervention

**Manual refresh:**
```python
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

creds = Credentials.from_authorized_user_file('token.json', SCOPES)
if creds.expired:
    creds.refresh(Request())
```

### Token Revocation

To revoke access:

1. **Option 1:** Delete token.json (local only)
2. **Option 2:** Revoke in Google Account settings:
   - https://myaccount.google.com/permissions
   - Find "Personal AI Employee"
   - Click "Remove Access"

## Best Practices

### Security

✅ **DO:**
- Keep credentials.json private
- Add to .gitignore
- Use read-only scopes when possible
- Regularly review granted permissions
- Revoke access when not needed

❌ **DON'T:**
- Commit to public repositories
- Share client_secret
- Use in untrusted environments
- Grant unnecessary scopes

### Deployment

For production use:

1. Use service account (for server deployments)
2. Store credentials in secure vault
3. Rotate secrets regularly
4. Monitor API usage
5. Set up quota limits

## Related Files

- **gmail_watcher.py** - Uses credentials.json for authentication
- **token.json** - Stores access/refresh tokens (auto-generated)
- **.gitignore** - Excludes credentials.json and token.json
- **.env** - Configuration (doesn't contain credentials)

## Support Resources

### Google Documentation

- [Gmail API Python Quickstart](https://developers.google.com/gmail/api/quickstart/python)
- [OAuth 2.0 for Desktop Apps](https://developers.google.com/identity/protocols/oauth2/native-app)
- [Gmail API Scopes](https://developers.google.com/gmail/api/auth/scopes)

### Project Documentation

- `SILVER_TIER_GUIDE.md` - Complete Silver Tier setup
- `README.md` - Project overview
- `gmail_watcher.py` - Implementation details

## Verification Checklist

Before running Gmail Watcher:

- [ ] credentials.json exists in project root
- [ ] Valid JSON format
- [ ] Contains all required fields
- [ ] Redirect URI includes localhost
- [ ] Google API packages installed
- [ ] Gmail API enabled in Cloud Console
- [ ] OAuth consent screen configured

After first run:

- [ ] Browser opened for authentication
- [ ] Granted permissions successfully
- [ ] token.json created
- [ ] Gmail Watcher running without errors
- [ ] Emails being detected

---

**Status:** ✅ Verified and Working  
**Last Updated:** Today  
**Version:** 1.0.0
