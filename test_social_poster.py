"""
Test if social poster is properly configured
یہ script check کرے گا کہ social poster کے لیے سب کچھ ٹھیک ہے یا نہیں
"""

import sys
from pathlib import Path

print("=" * 60)
print("Social Poster Configuration Test")
print("یہ script آپ کی configuration check کرے گا")
print("=" * 60)
print()

errors = []
warnings = []

# Check 1: Python version
print("[1/8] Checking Python version...")
if sys.version_info >= (3, 8):
    print(f"  ✓ Python {sys.version_info.major}.{sys.version_info.minor} (OK)")
else:
    errors.append("✗ Python version too old. Need 3.8+")
    print(f"  {errors[-1]}")

# Check 2: Playwright
print("\n[2/8] Checking Playwright...")
try:
    from playwright.sync_api import sync_playwright
    print("  ✓ Playwright module installed")
    
    # Try to check if browsers are installed
    try:
        import subprocess
        result = subprocess.run(['playwright', 'install', '--dry-run'], 
                              capture_output=True, text=True, timeout=5)
        print("  ✓ Playwright CLI available")
    except:
        warnings.append("⚠ Playwright CLI might not be in PATH")
        print(f"  {warnings[-1]}")
        
except ImportError:
    errors.append("✗ Playwright not installed")
    print(f"  {errors[-1]}")
    print("  Fix: pip install playwright")
    print("  Then: playwright install chromium")

# Check 3: python-dotenv
print("\n[3/8] Checking python-dotenv...")
try:
    from dotenv import load_dotenv
    print("  ✓ python-dotenv installed")
except ImportError:
    errors.append("✗ python-dotenv not installed")
    print(f"  {errors[-1]}")
    print("  Fix: pip install python-dotenv")

# Check 4: .env file
print("\n[4/8] Checking .env file...")
env_path = Path('.env')
if env_path.exists():
    print("  ✓ .env file exists")
    
    # Load and check credentials
    try:
        from dotenv import load_dotenv
        import os
        load_dotenv()
        
        linkedin_email = os.getenv('LINKEDIN_EMAIL', '')
        linkedin_password = os.getenv('LINKEDIN_PASSWORD', '')
        
        if linkedin_email and linkedin_email != 'your.email@example.com':
            print("  ✓ LinkedIn email configured")
        else:
            warnings.append("⚠ LinkedIn email not configured in .env")
            print(f"  {warnings[-1]}")
        
        if linkedin_password and linkedin_password != 'your_password':
            print("  ✓ LinkedIn password configured")
        else:
            warnings.append("⚠ LinkedIn password not configured in .env")
            print(f"  {warnings[-1]}")
            
    except Exception as e:
        warnings.append(f"⚠ Could not verify .env contents: {e}")
        print(f"  {warnings[-1]}")
else:
    errors.append("✗ .env file not found")
    print(f"  {errors[-1]}")
    print("  Fix: copy .env.example .env")
    print("  Then edit .env with your credentials")

# Check 5: Vault directory
print("\n[5/8] Checking AI_Employee_Vault...")
vault_path = Path('AI_Employee_Vault')
if vault_path.exists():
    print("  ✓ AI_Employee_Vault folder exists")
else:
    errors.append("✗ AI_Employee_Vault folder missing")
    print(f"  {errors[-1]}")
    print("  Fix: create_vault.bat")

# Check 6: Social_Queue folder
print("\n[6/8] Checking Social_Queue...")
queue_path = Path('AI_Employee_Vault/Social_Queue')
if queue_path.exists():
    print("  ✓ Social_Queue folder exists")
    
    # Check subdirectories
    posted_path = queue_path / 'Posted'
    failed_path = queue_path / 'Failed'
    
    if posted_path.exists():
        print("  ✓ Posted folder exists")
    else:
        warnings.append("⚠ Posted folder missing")
        print(f"  {warnings[-1]}")
    
    if failed_path.exists():
        print("  ✓ Failed folder exists")
    else:
        warnings.append("⚠ Failed folder missing")
        print(f"  {warnings[-1]}")
        
else:
    errors.append("✗ Social_Queue folder missing")
    print(f"  {errors[-1]}")
    print("  Fix: create_social_queue_v2.bat")

# Check 7: Logs directory
print("\n[7/8] Checking Logs folder...")
logs_path = Path('AI_Employee_Vault/Logs')
if logs_path.exists():
    print("  ✓ Logs folder exists")
else:
    warnings.append("⚠ Logs folder missing (will be auto-created)")
    print(f"  {warnings[-1]}")

# Check 8: social_poster.py
print("\n[8/8] Checking social_poster.py...")
script_path = Path('social_poster.py')
if script_path.exists():
    print("  ✓ social_poster.py exists")
else:
    errors.append("✗ social_poster.py not found")
    print(f"  {errors[-1]}")

# Summary
print()
print("=" * 60)
print("Test Summary / خلاصہ")
print("=" * 60)
print()

if not errors and not warnings:
    print("✅ All checks passed! / سب ٹھیک ہے!")
    print()
    print("You can run: python social_poster.py")
    print("آپ چلا سکتے ہیں: python social_poster.py")
    print()
    sys.exit(0)

if errors:
    print("❌ Critical Issues Found / اہم مسائل:")
    print()
    for i, error in enumerate(errors, 1):
        print(f"  {i}. {error}")
    print()
    print("Please fix these errors before running social_poster.py")
    print("براہ کرم یہ errors ٹھیک کریں")
    print()

if warnings:
    print("⚠️  Warnings / انتباہات:")
    print()
    for i, warning in enumerate(warnings, 1):
        print(f"  {i}. {warning}")
    print()
    print("These are not critical but recommended to fix")
    print("یہ بہت ضروری نہیں لیکن ٹھیک کرنا بہتر ہے")
    print()

# Quick fix suggestions
if errors or warnings:
    print("=" * 60)
    print("Quick Fix / فوری حل:")
    print("=" * 60)
    print()
    
    if any('Playwright not installed' in e for e in errors):
        print("1. Install Playwright:")
        print("   pip install playwright")
        print("   playwright install chromium")
        print()
    
    if any('.env file not found' in e for e in errors):
        print("2. Create .env file:")
        print("   copy .env.example .env")
        print("   Then edit .env with your credentials")
        print()
    
    if any('Social_Queue' in e for e in errors):
        print("3. Create Social_Queue folders:")
        print("   create_social_queue_v2.bat")
        print()
    
    if warnings and not errors:
        print("Your setup is mostly complete!")
        print("You can proceed, but check the warnings above.")
        print()
        print("آپ کا setup تقریباً مکمل ہے!")
        print("آگے بڑھ سکتے ہیں، لیکن اوپر warnings دیکھیں۔")
        print()

sys.exit(1 if errors else 0)
