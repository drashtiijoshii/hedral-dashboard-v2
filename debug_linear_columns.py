"""
🔍 Linear Column Debug Dashboard
Shows exactly what columns Linear exports to your Google Sheet
"""

import streamlit as st
import pandas as pd
from connect_google_sheet import GoogleSheetConnector
import requests
from io import StringIO

st.set_page_config(page_title="🔍 Linear Column Debugger", page_icon="🔍", layout="wide")

st.title("🔍 Linear Column Debug Dashboard")
st.markdown("This tool shows exactly what columns Linear exports to your Google Sheet")

# Google Sheets URL input
st.markdown("### 📊 Enter Your Google Sheets URL")
sheet_url = st.text_input(
    "Google Sheets URL:",
    placeholder="https://docs.google.com/spreadsheets/d/your-sheet-id/edit#gid=0",
    help="Make sure your sheet is public (Anyone with link can view)"
)

if sheet_url and st.button("🔍 Analyze Columns"):
    if "docs.google.com/spreadsheets" not in sheet_url:
        st.error("❌ Please enter a valid Google Sheets URL")
    else:
        try:
            # Extract sheet ID
            sheet_id = sheet_url.split("/spreadsheets/d/")[1].split("/")[0]
            
            # Extract gid (sheet tab) from URL if present
            gid = "0"  # default
            if "gid=" in sheet_url:
                gid = sheet_url.split("gid=")[1].split("&")[0].split("#")[0]
            
            st.info(f"📊 **Detected Sheet ID:** {sheet_id}")
            st.info(f"📋 **Detected Sheet Tab (gid):** {gid}")
            
            # Try multiple approaches to access the sheet
            success = False
            df = None
            
            # List of gids to try (including common Linear export gids)
            gids_to_try = [gid, "0", "1413191165", "2", "1"]
            
            with st.spinner("Fetching data from Google Sheet..."):
                for try_gid in gids_to_try:
                    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={try_gid}"
                    st.info(f"🔗 **Trying CSV Export URL:** {csv_url}")
                    
                    try:
                        response = requests.get(csv_url, timeout=10)
                        
                        if response.status_code == 200:
                            # Check if we got actual data (not empty or error page)
                            lines = response.text.strip().split('\n')
                            if len(lines) > 1 and 'ID' in lines[0]:  # Linear data should have ID column
                                df = pd.read_csv(StringIO(response.text))
                                st.success(f"✅ **SUCCESS with gid={try_gid}!** Found {len(df)} rows of data")
                                success = True
                                break
                            else:
                                st.warning(f"⚠️ gid={try_gid} accessible but no Linear data found")
                        else:
                            st.warning(f"❌ gid={try_gid} failed with status {response.status_code}")
                    except Exception as e:
                        st.warning(f"❌ gid={try_gid} failed with error: {str(e)}")
                
                if success and df is not None:
                    
                    st.success(f"✅ Successfully loaded {len(df)} rows of data!")
                    
                    # Show column analysis
                    st.markdown("### 📋 Column Analysis")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**📊 All Columns Found:**")
                        for i, col in enumerate(df.columns, 1):
                            st.write(f"{i}. `{col}`")
                    
                    with col2:
                        st.markdown("**🔍 Column Details:**")
                        st.write(f"Total columns: {len(df.columns)}")
                        st.write(f"Total rows: {len(df)}")
                        
                        # Show data types
                        st.markdown("**Data Types:**")
                        for col in df.columns:
                            dtype = str(df[col].dtype)
                            sample_value = str(df[col].iloc[0]) if len(df) > 0 else "N/A"
                            st.write(f"• `{col}`: {dtype} (e.g., '{sample_value[:50]}...' if len(sample_value) > 50 else sample_value)")
                    
                    # Show first few rows
                    st.markdown("### 👀 Sample Data (First 5 Rows)")
                    st.dataframe(df.head(), use_container_width=True)
                    
                    # Linear column mapping suggestions
                    st.markdown("### 🎯 Suggested Column Mappings")
                    st.markdown("Based on your columns, here are the suggested mappings for the dashboard:")
                    
                    mapping_suggestions = {
                        'id': [col for col in df.columns if any(x in col.lower() for x in ['id', 'identifier', 'number'])],
                        'title': [col for col in df.columns if any(x in col.lower() for x in ['title', 'name', 'summary'])],
                        'status': [col for col in df.columns if any(x in col.lower() for x in ['status', 'state'])],
                        'assignee': [col for col in df.columns if any(x in col.lower() for x in ['assignee', 'assigned'])],
                        'estimate': [col for col in df.columns if any(x in col.lower() for x in ['estimate', 'points', 'story'])],
                        'team': [col for col in df.columns if any(x in col.lower() for x in ['team', 'group'])],
                        'cycle': [col for col in df.columns if any(x in col.lower() for x in ['cycle', 'sprint', 'iteration'])],
                        'created': [col for col in df.columns if any(x in col.lower() for x in ['created', 'start'])],
                        'completed': [col for col in df.columns if any(x in col.lower() for x in ['completed', 'finished', 'done'])],
                    }
                    
                    for dashboard_field, candidates in mapping_suggestions.items():
                        if candidates:
                            st.write(f"**{dashboard_field.upper()}:** {', '.join([f'`{c}`' for c in candidates])}")
                        else:
                            st.write(f"**{dashboard_field.upper()}:** ❌ No matching column found")
                    
                    # Export column list
                    st.markdown("### 📋 Column List for Reference")
                    columns_text = "\n".join([f"'{col}'" for col in df.columns])
                    st.text_area(
                        "Copy this list of columns:",
                        columns_text,
                        height=200,
                        help="You can copy this list to help with manual mapping if needed"
                    )
                    
                else:
                    st.error(f"❌ Cannot access sheet. Status code: {response.status_code}")
                    st.markdown("""
                    **Troubleshooting:**
                    1. Make sure your sheet is public (Anyone with link can view)
                    2. Check if the URL is correct
                    3. Try opening the URL in an incognito browser to verify it's accessible
                    """)
                
        except Exception as e:
            st.error(f"❌ Error analyzing sheet: {str(e)}")
            st.markdown("""
            **Common Issues:**
            - Sheet is not public
            - Invalid URL format
            - Network connectivity issues
            """)

# Instructions
st.markdown("### 📝 How to Use This Tool")
st.markdown("""
1. **Make your Linear → Google Sheets export public**
   - Open your Google Sheet
   - Click "Share" → "Anyone with the link can view"
   
2. **Enter the sheet URL above**
   - Copy the full URL from your browser
   - Paste it in the input field
   
3. **Click "Analyze Columns"**
   - This will show you exactly what Linear exports
   - You'll see suggested mappings for the dashboard
   
4. **Use the results to configure your main dashboard**
   - The column mappings will help the dashboard understand your data
""")

if __name__ == "__main__":
    st.markdown("---")
    st.markdown("**💡 Pro Tip:** Run this first to understand your Linear data structure before using the main dashboard!") 