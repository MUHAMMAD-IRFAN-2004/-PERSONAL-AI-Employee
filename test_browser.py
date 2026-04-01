"""
Test Browser - Blank Page Issue Check Karne Ke Liye
Is script se pata chalega browser theek se kaam kar raha hai ya nahi
"""

from playwright.sync_api import sync_playwright
import time
import sys

print("=" * 60)
print("Browser Test Script")
print("Blank page issue check karne ke liye")
print("=" * 60)
print()

try:
    print("[Step 1/5] Playwright import ho raha hai...")
    from playwright.sync_api import sync_playwright
    print("  ✓ Playwright import successful")
    print()
    
    print("[Step 2/5] Browser launch kar rahe hain...")
    print("  (Browser window khulegi - wait karein)")
    print()
    
    with sync_playwright() as p:
        # Launch browser (visible mode)
        browser = p.chromium.launch(
            headless=False,
            slow_mo=1000  # Slow motion for debugging
        )
        print("  ✓ Browser launched successfully")
        print()
        
        print("[Step 3/5] New page khol rahe hain...")
        page = browser.new_page()
        print("  ✓ Page created")
        print()
        
        print("[Step 4/5] LinkedIn ja rahe hain...")
        print("  URL: https://www.linkedin.com/login")
        print("  Please wait...")
        
        try:
            page.goto("https://www.linkedin.com/login", timeout=30000)
            print("  ✓ LinkedIn page loaded!")
            print()
            
            # Check if page loaded correctly
            title = page.title()
            print(f"  Page title: {title}")
            
            if "LinkedIn" in title or "Sign In" in title:
                print("  ✓ LinkedIn login page dikhai de raha hai!")
            else:
                print("  ⚠ Unexpected page title")
            print()
            
        except Exception as e:
            print(f"  ✗ LinkedIn load nahi hua: {e}")
            print()
        
        print("[Step 5/5] 15 seconds wait kar rahe hain...")
        print("  Browser window ko dekho:")
        print("  - Kya LinkedIn login page dikhai de raha hai?")
        print("  - Ya blank/white page hai?")
        print()
        
        for i in range(15, 0, -1):
            print(f"  Closing in {i} seconds...", end='\r')
            time.sleep(1)
        
        print()
        print()
        browser.close()
        print("Browser band ho gaya")
        
    print()
    print("=" * 60)
    print("Test Complete!")
    print("=" * 60)
    print()
    print("Results:")
    print("  Agar LinkedIn page dikha:")
    print("    ✓ Browser aur internet theek hai")
    print("    ✓ social_poster.py mein koi aur issue hai")
    print()
    print("  Agar blank page dikha:")
    print("    ✗ Browser ya internet ka issue hai")
    print("    ✗ Troubleshooting steps follow karo")
    print()
    
except ImportError as e:
    print(f"✗ Error: {e}")
    print()
    print("Playwright install nahi hai!")
    print("Install karo:")
    print("  pip install playwright")
    print("  playwright install chromium")
    sys.exit(1)
    
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    print()
    print("Error details:")
    import traceback
    traceback.print_exc()
    sys.exit(1)
