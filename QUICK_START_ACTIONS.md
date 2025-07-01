# 🚀 QUICK START - Do This Right Now!

## 📱 Your Dashboards Are Live - Test Them Now!

**Open these URLs in your browser:**

1. **🎯 UNIFIED DASHBOARD (START HERE):** http://localhost:8500
   - All 3 dashboards in beautiful tabs
   - Best user experience
   - Professional design

2. **Individual Dashboards** (if needed):
   - Scrum Review: http://localhost:8501
   - Performance: http://localhost:8502  
   - OKR Tracking: http://localhost:8503

---

## ⚡ Phase 1: Connect Real Data (Next 30 minutes)

### Step 1: Set Up Linear Export (10 minutes)
```
1. Open Linear in browser
2. Go to Settings → Integrations
3. Find "Google Sheets" → Click Connect
4. Choose "Hourly" export frequency
5. Select these fields:
   ✓ Title, Assignee, Status, Estimate
   ✓ Created Date, Completed Date, Started Date
   ✓ Cycle/Sprint, Priority, Type
6. Click "Create Export"
7. Wait for Linear to create the Google Sheet
```

### Step 2: Make Sheet Public (5 minutes)
```
1. Open the new Google Sheet Linear created
2. Click "Share" (top right)
3. Click "Change to anyone with the link"
4. Set to "Viewer" permission
5. Copy the sheet URL (save it!)
```

### Step 3: Connect to Dashboard (5 minutes)
```
1. Go to http://localhost:8500
2. In sidebar: Select "Google Sheet" 
3. Paste your sheet URL
4. Click "🔌 Connect"
5. You should see "✅ Connected!"
```

### Step 4: Verify It Works (10 minutes)
```
✅ Check Scrum tab - see your real sprints?
✅ Check Performance tab - see your team members?
✅ Do the numbers look correct?
✅ Try filtering by different sprints
```

---

## ⚡ Phase 2: Share with Team (Next 15 minutes)

### Option A: Quick Network Share
```bash
# In terminal, run this command:
streamlit run app.py --server.address=0.0.0.0 --server.port=8500

# Find your IP address:
# Mac: ifconfig | grep "inet " | grep -v 127.0.0.1
# Windows: ipconfig | findstr "IPv4"

# Share this URL with team:
# http://YOUR_IP:8500
# Example: http://192.168.1.100:8500
```

### Option B: Deploy to Cloud (Free)
```
1. Create GitHub account (if needed)
2. Create new repository: "scrum-dashboard"
3. Upload your files to GitHub
4. Go to share.streamlit.io
5. Connect GitHub → Deploy app.py
6. Get public URL → Share with team
```

---

## ⚡ Phase 3: Customize (Next 20 minutes)

### Quick Branding
```python
# Edit app.py - find the CSS section and change colors:

# Line ~25: Change main header color
background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);

# Line ~60: Change tab colors  
background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);

# Save file → Refresh browser
```

### Add Company Logo
```python
# Add this at top of main() function in app.py:
st.image("your_logo.png", width=200)
st.markdown('<div class="main-header">YOUR COMPANY - Scrum Dashboard</div>', unsafe_allow_html=True)
```

---

## 🎯 What You'll Have After 1 Hour:

✅ **Real Linear data** flowing automatically every hour  
✅ **Team access** via shared URL  
✅ **Professional dashboard** with your branding  
✅ **Automated insights** for sprints, performance, OKRs  
✅ **Time savings** of 6+ hours per week  

---

## 📞 Need Help? Check These:

**❌ Can't connect to Linear data?**
- Wait 1 hour after Linear export setup
- Check if Google Sheet has data
- Verify sheet is public/shared

**❌ Dashboard won't start?**
```bash
# Run these commands:
cd ~/Desktop/hedral_dashboard_2
pip install -r requirements.txt
streamlit run app.py
```

**❌ Team can't access?**
- Check firewall settings
- Try cloud deployment instead
- Verify IP address is correct

---

## 🚀 Success Checklist

Check these off as you complete them:

**Setup:**
- [ ] Linear → Google Sheets export working
- [ ] Dashboard shows real data  
- [ ] Team can access dashboard
- [ ] Basic customization done

**Using the Dashboard:**
- [ ] Check sprint progress daily
- [ ] Use for sprint planning meetings
- [ ] Track OKR progress weekly
- [ ] Capture retrospective notes

**Next Steps:**
- [ ] Train team on dashboard features
- [ ] Set up email reports (optional)
- [ ] Add more custom metrics
- [ ] Plan advanced features

---

**🎉 You're ready to revolutionize your Scrum process with automated, beautiful dashboards!**

## 📖 For More Details:
- **Complete Guide:** `AUTOMATION_GUIDE_DETAILED.md` 
- **Troubleshooting:** Check the detailed guide
- **Customization:** Follow Phase 4 in detailed guide 