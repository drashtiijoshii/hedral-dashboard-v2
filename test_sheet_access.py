"""
🧪 Quick Google Sheet Access Test
Tests if your sheet can be accessed as CSV
"""

import requests
import sys

def test_sheet_access(sheet_url):
    """Test if a Google Sheet can be accessed publicly"""
    
    print(f"🔍 Testing sheet access...")
    print(f"URL provided: {sheet_url}")
    
    try:
        # Extract sheet ID from URL
        if "/spreadsheets/d/" in sheet_url:
            sheet_id = sheet_url.split("/spreadsheets/d/")[1].split("/")[0]
            print(f"📊 Sheet ID extracted: {sheet_id}")
            
            # Convert to CSV export URL
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
            print(f"🔗 CSV URL: {csv_url}")
            
            # Test access
            print(f"⏳ Testing access...")
            response = requests.get(csv_url, timeout=10)
            
            print(f"📡 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ SUCCESS: Sheet is publicly accessible!")
                
                # Show first few lines
                lines = response.text.split('\n')[:5]
                print(f"📋 First 5 lines of data:")
                for i, line in enumerate(lines, 1):
                    print(f"  {i}: {line[:100]}...")
                
                # Count columns
                if lines:
                    columns = lines[0].split(',')
                    print(f"📊 Found {len(columns)} columns")
                    print(f"🏷️ Column names: {', '.join(columns[:10])}...")
                
                return True
                
            else:
                print(f"❌ FAILED: Cannot access sheet (Status: {response.status_code})")
                return False
                
        else:
            print("❌ FAILED: Invalid Google Sheets URL format")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    # Test with user's URL
    test_url = input("Enter your Google Sheets URL: ").strip()
    
    if test_url:
        success = test_sheet_access(test_url)
        if success:
            print("\n🎉 Your sheet is ready for the dashboard!")
        else:
            print("\n🔧 Please check the troubleshooting steps below:")
            print("1. Make sure the sheet is public (Anyone with link can view)")
            print("2. Use the complete URL format")
            print("3. Try opening the URL in an incognito browser")
    else:
        print("No URL provided") 