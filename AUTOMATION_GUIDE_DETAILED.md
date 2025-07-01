# 🚀 Complete Dashboard Automation Guide
## Step-by-Step Instructions for Automated Scrum Dashboards

---

## 📊 Current Status - What You Have Now

✅ **Your Dashboards Are Running:**
- **Unified Dashboard**: http://localhost:8500 (RECOMMENDED - All 3 dashboards in one!)
- **Individual Dashboards**:
  - Scrum Review: http://localhost:8501
  - Performance Analytics: http://localhost:8502  
  - OKR Tracking: http://localhost:8503

✅ **What's Working:**
- Sample data with 50 realistic issues
- 3 sprints with 5 team members
- 5 OKRs with progress tracking
- All charts and analytics functional

---

## 🎯 Phase 1: Connect Your Real Linear Data (15-30 minutes)

### Step 1.1: Set Up Linear → Google Sheets Export

**1. Open Linear in your browser:**
```
→ Go to your Linear workspace
→ Click on your profile/settings (bottom left)
→ Select "Workspace Settings"
```

**2. Enable Google Sheets Integration:**
```
→ Click "Integrations" in the left sidebar
→ Find "Google Sheets" 
→ Click "Connect" or "Enable"
→ Authorize with your Google account when prompted
```

**3. Configure the Export:**
```
→ Select "Export issues to Google Sheets"
→ Choose frequency: "Hourly" (recommended for real-time data)
→ Select fields to export:
   ✓ Title
   ✓ Assignee  
   ✓ Status
   ✓ Estimate (Story Points)
   ✓ Created Date
   ✓ Completed Date
   ✓ Started Date
   ✓ Cycle/Sprint
   ✓ Priority
   ✓ Type/Labels
→ Click "Create Export"
```

**4. Get Your Google Sheet URL:**
```
→ Linear will create a new Google Sheet
→ Open the sheet in Google Sheets
→ Copy the URL from your browser address bar
→ It should look like: https://docs.google.com/spreadsheets/d/1ABC...XYZ/edit
```

### Step 1.2: Make Your Sheet Accessible

**Option A: Public Access (Simple - for non-sensitive data):**
```
1. In Google Sheets, click "Share" (top right)
2. Click "Change to anyone with the link"
3. Set permission to "Viewer"
4. Click "Copy link"
5. Save this URL - you'll need it for the dashboard
```

**Option B: Private Access (Secure - for sensitive data):**
```
1. Go to Google Cloud Console (console.cloud.google.com)
2. Create new project or select existing one
3. Enable Google Sheets API
4. Create Service Account:
   → IAM & Admin → Service Accounts
   → Create Service Account
   → Download JSON credentials file
5. Share your Google Sheet with the service account email
6. Keep the credentials file secure
```

### Step 1.3: Connect to Your Dashboard

**1. Open your unified dashboard:**
```
→ Go to http://localhost:8500
```

**2. Connect your data:**
```
→ In the left sidebar, select "Google Sheet" (instead of Sample Data)
→ Paste your Google Sheets URL in the text box
→ Click "🔌 Connect"
→ You should see "✅ Connected!" message
```

**3. Verify your data:**
```
→ Check the Scrum Review tab - you should see your real sprints
→ Check Performance tab - you should see your actual team members
→ If you have OKR data in a separate sheet, connect that too
```

---

## 🌐 Phase 2: Deploy for Team Access (30-60 minutes)

### Option A: Streamlit Cloud (FREE & Recommended)

**Step 2A.1: Prepare Your Code**
```bash
# In your terminal, from your project directory:
cd ~/Desktop/hedral_dashboard_2

# Initialize git if not already done
git init

# Add all files
git add .

# Commit your changes
git commit -m "Add automated scrum dashboard suite"
```

**Step 2A.2: Push to GitHub**
```bash
# Create a new repository on GitHub.com
# Then connect it to your local repository:

git remote add origin https://github.com/YOUR_USERNAME/scrum-dashboard.git
git branch -M main
git push -u origin main
```

**Step 2A.3: Deploy to Streamlit Cloud**
```
1. Go to https://share.streamlit.io
2. Click "New app"
3. Connect your GitHub account
4. Select your repository: "scrum-dashboard"
5. Set main file path: "app.py"
6. Click "Deploy!"
7. Wait 2-3 minutes for deployment
8. You'll get a public URL like: https://your-app-name.streamlit.app
```

**Step 2A.4: Share with Your Team**
```
→ Copy the Streamlit Cloud URL
→ Share with your team via Slack/email
→ Everyone can access without installation
→ Updates automatically when you push to GitHub
```

### Option B: Local Network Sharing (Quick)

**Step 2B.1: Find Your IP Address**
```bash
# On Mac/Linux:
ifconfig | grep "inet " | grep -v 127.0.0.1

# On Windows:
ipconfig | findstr "IPv4"

# Note your IP address (e.g., 192.168.1.100)
```

**Step 2B.2: Start Dashboard for Network Access**
```bash
# Stop current dashboard first (Ctrl+C in terminal)
# Then start with network access:
streamlit run app.py --server.address=0.0.0.0 --server.port=8500

# Your team can now access at:
# http://YOUR_IP_ADDRESS:8500
# Example: http://192.168.1.100:8500
```

---

## 🔄 Phase 3: Set Up Full Automation (1-2 hours)

### Step 3.1: Automatic Data Refresh

**Your data is already automated! Here's how:**
```
✅ Linear exports to Google Sheets every hour
✅ Dashboard loads fresh data on each page refresh
✅ Charts update automatically with new data
✅ No manual data entry required!
```

**To force refresh:**
```
→ Click "🔄 Refresh Data" button in sidebar
→ Or simply refresh your browser page
```

### Step 3.2: Set Up Email Reports (Optional)

**Create weekly email summaries:**

1. **Install additional packages:**
```bash
pip install schedule smtplib email-mime
```

2. **Create email automation script:**
```python
# Create file: email_reports.py
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_weekly_report():
    # Load your dashboard data
    # Generate summary
    # Send email to team
    print("Weekly report sent!")

# Schedule weekly reports
schedule.every().monday.at("09:00").do(send_weekly_report)

# Keep running
while True:
    schedule.run_pending()
    time.sleep(3600)  # Check every hour
```

3. **Run the scheduler:**
```bash
python email_reports.py &
```

### Step 3.3: Set Up Slack Notifications (Optional)

**Get notified about at-risk OKRs:**

1. **Create Slack App:**
```
→ Go to api.slack.com/apps
→ Create New App
→ Get Bot Token
```

2. **Add Slack integration:**
```python
# Add to your dashboard
import slack_sdk

def check_at_risk_okrs():
    # Check OKR status
    # Send Slack message if any are "At Risk"
    pass
```

---

## 🎨 Phase 4: Customization Guide (30 minutes)

### Step 4.1: Brand Your Dashboard

**Update colors and styling:**
```python
# In app.py, find the CSS section and modify:

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);
        # Change to your company colors
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);
        # Match your brand
    }
</style>
""", unsafe_allow_html=True)
```

**Add your company logo:**
```python
# At the top of main():
st.image("your_logo.png", width=200)
st.markdown('<div class="main-header">Your Company - Scrum Dashboard</div>', unsafe_allow_html=True)
```

### Step 4.2: Add Custom Metrics

**Add company-specific KPIs:**
```python
# In scrum_dashboard() function, add:
with col5:  # Add a 5th column
    bug_count = len(filtered_df[filtered_df['type'] == 'Bug'])
    st.metric("🐛 Bugs", bug_count, help="Total bugs in sprint")
```

**Add custom charts:**
```python
# Add priority breakdown
priority_counts = filtered_df['priority'].value_counts()
fig = px.pie(values=priority_counts.values, names=priority_counts.index, 
             title="Priority Distribution")
st.plotly_chart(fig, use_container_width=True)
```

### Step 4.3: Add New Dashboard Tabs

**To add a fourth tab (e.g., "Risk Analysis"):**

1. **Update the tabs definition:**
```python
tab1, tab2, tab3, tab4 = st.tabs([
    "🔁 Scrum Review", 
    "👤 Performance", 
    "🎯 OKR Tracking",
    "⚠️ Risk Analysis"  # New tab
])
```

2. **Add the new tab content:**
```python
with tab4:
    risk_analysis_dashboard(issues_df)

def risk_analysis_dashboard(df):
    st.markdown('<div class="section-header">⚠️ Risk Analysis</div>', unsafe_allow_html=True)
    
    # Add your custom risk analysis logic here
    overdue_issues = df[df['status'] != 'Done']  # Example
    st.metric("⏰ Overdue Issues", len(overdue_issues))
    
    # Add more risk analysis features
```

---

## 🐛 Troubleshooting Guide

### Common Issues & Solutions

**❌ "Failed to connect to Google Sheet"**
```
Solutions:
1. Check if sheet URL is correct
2. Ensure sheet is public or properly shared
3. Verify Linear export is working
4. Try reconnecting after a few minutes
```

**❌ "No data found in worksheet"**
```
Solutions:
1. Check if Linear has exported data yet (wait 1 hour after setup)
2. Verify worksheet name (should be "Sheet1" by default)
3. Check if column headers match expected format
4. Ensure Linear export includes all required fields
```

**❌ Charts not displaying properly**
```
Solutions:
1. Refresh the page
2. Clear browser cache
3. Check browser console for errors
4. Try a different browser
5. Restart the Streamlit app
```

**❌ Dashboard is slow**
```
Solutions:
1. Reduce data range (filter by recent sprints)
2. Optimize Google Sheets (remove unnecessary columns)
3. Add caching to your dashboard
4. Consider data pagination for large datasets
```

### Performance Optimization

**Add caching for faster loading:**
```python
import streamlit as st

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data_cached(source):
    return load_data(source)

# Use cached version in main()
issues_df, okr_df = load_data_cached(data_source)
```

**Optimize data loading:**
```python
# Only load data when needed
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = load_data(data_source)
    
issues_df, okr_df = st.session_state.data_loaded
```

---

## 📈 Usage & Best Practices

### Daily Usage
```
✅ Morning: Check sprint progress and team performance
✅ Standups: Review burndown chart and blockers
✅ Planning: Use velocity data for estimation
✅ Reviews: Capture retrospective notes
```

### Weekly Usage
```
✅ Monday: Review previous sprint completion
✅ Wednesday: Check OKR progress and at-risk items
✅ Friday: Plan next sprint based on velocity trends
✅ Updates: Share dashboard URL with stakeholders
```

### Monthly Usage
```
✅ Review team performance trends
✅ Update OKR targets based on progress
✅ Analyze cycle time improvements
✅ Plan process improvements
```

---

## 🚀 Future Enhancements Roadmap

### Next 2 Weeks
- [ ] Deploy to production (Streamlit Cloud)
- [ ] Connect real Linear data
- [ ] Customize branding and colors
- [ ] Train team on dashboard usage

### Next Month
- [ ] Add email report automation
- [ ] Set up Slack notifications
- [ ] Add forecasting capabilities
- [ ] Create mobile-responsive version

### Next Quarter
- [ ] AI-powered insights and recommendations
- [ ] Integration with GitHub for code metrics
- [ ] Advanced analytics and reporting
- [ ] Custom dashboard for executives

---

## 📞 Getting Help

**If you get stuck:**

1. **Check the troubleshooting section above**
2. **Review error messages carefully**
3. **Test with sample data first**
4. **Check Linear and Google Sheets connectivity**
5. **Restart the dashboard application**

**For advanced customization:**
- Streamlit documentation: https://docs.streamlit.io
- Plotly charts: https://plotly.com/python/
- Pandas data manipulation: https://pandas.pydata.org/docs/

---

## ✅ Quick Start Checklist

Copy this checklist and check off each step:

**Setup (Do Once):**
- [ ] Linear → Google Sheets integration enabled
- [ ] Google Sheet URL copied
- [ ] Dashboard connected to real data
- [ ] Team has access to dashboard URL

**Daily Operations:**
- [ ] Check dashboard each morning
- [ ] Update retrospective notes after reviews
- [ ] Monitor at-risk OKRs
- [ ] Share insights with team

**Weekly Maintenance:**
- [ ] Review data quality
- [ ] Update any custom configurations
- [ ] Check for new Linear features/updates
- [ ] Gather team feedback for improvements

---

**🎉 Congratulations! You now have a fully automated, professional Scrum dashboard that will save your team hours every week and provide real-time insights for better decision making!** 