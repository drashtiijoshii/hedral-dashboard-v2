# 📊 Google Sheets Setup Guide

## 🚀 Quick Setup (3 Steps)

### 1. Make Your Sheet Public
- Open your Google Sheet with Linear data
- Click **Share** button (top-right)
- Change access to **"Anyone with the link can view"**
- Click **Copy link**

### 2. Debug Your Linear Columns (RECOMMENDED)
- Go to **http://localhost:8505** (Column Debug Dashboard)
- Paste your sheet URL and click "Analyze Columns"
- See exactly what columns Linear exports
- Get suggested mappings for the dashboard

### 3. Connect to Dashboard
- Go to **http://localhost:8500** (main dashboard)
- Select **"Google Sheet"** as data source
- Paste your sheet URL and click **"🔌 Connect"**
- Dashboard will auto-map Linear columns

## 🎯 Linear-Specific Information

### Common Linear Column Names
Linear typically exports these columns:
- `identifier` - Issue ID (e.g., "ENG-123")
- `title` - Issue title
- `state` or `state.name` - Status (Todo, In Progress, Done)
- `assignee.name` - Assigned team member
- `estimate` or `storyPoints` - Story points
- `team.name` - Team name
- `cycle.name` - Sprint/cycle name
- `createdAt` - Creation timestamp
- `completedAt` - Completion timestamp
- `priority.name` - Priority level

### Auto-Mapping Features
The dashboard automatically maps Linear columns:
- ✅ `identifier` → `id`
- ✅ `state.name` → `status`
- ✅ `assignee.name` → `assignee`
- ✅ `cycle.name` → `cycle`
- ✅ `createdAt` → `createdat`
- ✅ And many more...

## 🔧 Your Dashboard URLs

### 🔍 **Debug Tool (Use This First!)**
**http://localhost:8505** - Analyze your Linear columns

### 🚀 **Main Dashboard**
**http://localhost:8500** - Unified Scrum Dashboard

### 📊 Individual Dashboards
- **http://localhost:8501** - Scrum Review
- **http://localhost:8502** - Performance Analytics
- **http://localhost:8503** - OKR Tracking

## 🛠️ Troubleshooting

### ❌ "No such file or directory" Error
**FIXED!** This error is now resolved. The dashboard uses public access instead of service account authentication.

### ❌ "Sheet is not publicly accessible"
**Solution:** Check sharing settings
- The link should work in an incognito browser
- No sign-in should be required to view

### ❌ "Invalid Google Sheets URL format"
**Solution:** Use the correct URL format
- ✅ Good: `https://docs.google.com/spreadsheets/d/abc123/edit#gid=0`
- ❌ Bad: `https://sheets.google.com/...`

### ❌ "No data available" in Dashboard
**Solution:** Use the debug tool first
1. Go to http://localhost:8505
2. Analyze your sheet structure
3. Check if Linear exported data correctly

## 📋 Expected Data Structure

Your Linear export should have:
- At least 10-20 columns (Linear exports many fields)
- Issue identifiers like "ENG-123", "PROD-456"
- Status values like "Todo", "In Progress", "Done"
- Date fields in ISO format (2024-01-15T10:30:00.000Z)
- Numeric estimates/story points

## 🧪 Testing Your Setup

### Method 1: Debug Tool
1. Go to http://localhost:8505
2. Enter your sheet URL
3. See column analysis and mappings

### Method 2: Manual Test
1. Copy your sheet URL
2. Open it in an incognito browser
3. Should see Linear data without login

### Method 3: Direct CSV Test
Replace `SHEET_ID` with your actual sheet ID:
```
https://docs.google.com/spreadsheets/d/SHEET_ID/export?format=csv&gid=0
```

## 💡 Pro Tips

### 🔄 **Auto-Refresh Data**
- Linear updates Google Sheets hourly
- Refresh dashboard to see latest data
- No manual exports needed

### 📈 **Best Practices**
- Export 2-3 months of Linear data for trends
- Include completed and in-progress issues
- Make sure assignees and cycles are populated

### 🎯 **Column Optimization**
- Export team, cycle, and priority fields
- Include story points/estimates for velocity
- Add labels/tags for better categorization

---

**🚀 Ready to go?** Start with the debug tool at http://localhost:8505 to see your Linear data structure! 