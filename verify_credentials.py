"""
Verify credentials.json for Gmail API integration

This script validates the credentials.json file structure and configuration
for the Gmail Watcher in the Personal AI Employee system.
"""

import json
import os
from pathlib import Path

def verify_credentials():
    """Verify credentials.json file exists and is properly formatted."""
    
    print("=" * 60)
    print("Gmail API Credentials Verification")
    print("=" * 60)
    print()
    
    # Check if file exists
    credentials_path = Path('credentials.json')
    
    if not credentials_path.exists():
        print("❌ ERROR: credentials.json not found!")
        print()
        print("To fix this:")
        print("1. Go to Google Cloud Console: https://console.cloud.google.com")
        print("2. Enable Gmail API")
        print("3. Create OAuth 2.0 credentials")
        print("4. Download as credentials.json")
        print("5. Place in project root directory")
        return False
    
    print("✓ credentials.json file exists")
    print()
    
    # Verify JSON format
    try:
        with open(credentials_path, 'r') as f:
            creds = json.load(f)
        print("✓ Valid JSON format")
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: Invalid JSON format: {e}")
        return False
    
    print()
    
    # Verify structure
    print("Checking credential structure...")
    print()
    
    if 'installed' not in creds and 'web' not in creds:
        print("❌ ERROR: Missing 'installed' or 'web' key")
        print("   Credentials should have either 'installed' or 'web' configuration")
        return False
    
    # Get the config (prefer 'installed' for desktop apps)
    config = creds.get('installed') or creds.get('web')
    config_type = 'installed' if 'installed' in creds else 'web'
    
    print(f"✓ Configuration type: {config_type}")
    print()
    
    # Required fields
    required_fields = [
        'client_id',
        'client_secret',
        'auth_uri',
        'token_uri',
        'redirect_uris'
    ]
    
    missing_fields = []
    
    for field in required_fields:
        if field in config:
            print(f"✓ {field}: Present")
            
            # Show partial values for verification (hide sensitive parts)
            value = str(config[field])
            if field == 'client_id':
                print(f"  Value: {value[:20]}...{value[-15:]}")
            elif field == 'client_secret':
                print(f"  Value: {value[:10]}... (hidden)")
            elif field == 'redirect_uris':
                print(f"  Value: {value}")
            else:
                print(f"  Value: {value}")
        else:
            print(f"❌ {field}: MISSING")
            missing_fields.append(field)
        print()
    
    if missing_fields:
        print(f"❌ ERROR: Missing required fields: {', '.join(missing_fields)}")
        return False
    
    # Optional but useful fields
    print("Optional fields:")
    optional_fields = ['project_id', 'auth_provider_x509_cert_url']
    
    for field in optional_fields:
        if field in config:
            print(f"✓ {field}: {config[field]}")
        else:
            print(f"⚠ {field}: Not present (optional)")
    
    print()
    
    # Verify redirect URIs for installed app
    if config_type == 'installed':
        redirect_uris = config.get('redirect_uris', [])
        if 'http://localhost' in redirect_uris or any('localhost' in uri for uri in redirect_uris):
            print("✓ Redirect URI includes localhost (correct for desktop app)")
        else:
            print("⚠ WARNING: Redirect URI should include http://localhost for desktop app")
    
    print()
    
    # Check for token.json
    token_path = Path('token.json')
    if token_path.exists():
        print("✓ token.json found (already authenticated)")
        print("  You can run gmail_watcher.py without re-authentication")
    else:
        print("⚠ token.json not found")
        print("  First run of gmail_watcher.py will require browser authentication")
    
    print()
    
    # Check for required Python packages
    print("Checking required Python packages...")
    print()
    
    try:
        import google.auth
        print("✓ google-auth installed")
    except ImportError:
        print("❌ google-auth NOT installed")
        print("   Run: pip install google-auth")
    
    try:
        import google_auth_oauthlib
        print("✓ google-auth-oauthlib installed")
    except ImportError:
        print("❌ google-auth-oauthlib NOT installed")
        print("   Run: pip install google-auth-oauthlib")
    
    try:
        import googleapiclient
        print("✓ google-api-python-client installed")
    except ImportError:
        print("❌ google-api-python-client NOT installed")
        print("   Run: pip install google-api-python-client")
    
    print()
    
    # Summary
    print("=" * 60)
    print("✅ VERIFICATION COMPLETE")
    print("=" * 60)
    print()
    print("Your credentials.json appears to be valid!")
    print()
    print("Next steps:")
    print("1. Ensure all required packages are installed:")
    print("   pip install google-auth google-auth-oauthlib google-api-python-client")
    print()
    print("2. Run the Gmail Watcher:")
    print("   python gmail_watcher.py")
    print()
    print("3. On first run, a browser will open for authentication")
    print("4. Grant access to your Gmail account")
    print("5. token.json will be created for future runs")
    print()
    
    return True


if __name__ == '__main__':
    try:
        verify_credentials()
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
