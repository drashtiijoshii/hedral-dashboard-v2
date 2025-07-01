# 📊 Automated Scrum Dashboards with Streamlit

A comprehensive dashboard suite for Scrum teams to track sprint progress, individual performance, and OKRs with real-time data from Linear via Google Sheets.

## 🎯 Overview

This project provides three interconnected dashboards:

1. **🔁 Scrum Review Dashboard** - Sprint velocity, burndown charts, retrospectives
2. **👤 Performance Dashboard** - Individual team member KPIs and analytics  
3. **🎯 OKR Dashboard** - Objectives and Key Results tracking with progress visualization

## 🏗️ Architecture

```
Linear → Google Sheets (auto-sync) → Python/Streamlit → Interactive Dashboards
```

- **Data Source**: Linear issues exported to Google Sheets (hourly auto-updates)
- **Processing**: Python with pandas for data transformation
- **Visualization**: Streamlit + Plotly for interactive charts
- **Deployment**: Local or Streamlit Cloud

## 📁 Project Structure

```
📁 Streamlit Scrum Dashboards
├── 📄 connect_google_sheet.py          # Google Sheets connector
├── 📄 scrum_dashboard.py               # Sprint analytics & retrospectives
├── 📄 performance_dashboard.py         # Individual performance metrics
├── 📄 okr_dashboard.py                 # OKR tracking & progress
├── 📄 requirements.txt                 # Python dependencies
└── 📄 README.md                        # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Linear → Google Sheets Integration

1. Go to Linear → Settings → Integrations → Google Sheets
2. Enable export and authorize your Google account
3. Select the sheet where issues will auto-sync (hourly updates)
4. Make the sheet publicly readable or set up service account credentials

### 3. Run Dashboards

**Scrum Review Dashboard:**
```bash
streamlit run scrum_dashboard.py
```

**Performance Dashboard:**
```bash
streamlit run performance_dashboard.py
```

**OKR Dashboard:**
```bash
streamlit run okr_dashboard.py
```

### 4. Connect Your Data

- Choose "Google Sheet" as data source
- Enter your Google Sheets URL
- Or use "Sample Data" for testing

## 📊 Dashboard Features

### 🔁 Scrum Review Dashboard

- **📈 Sprint Velocity**: Story points completed per sprint
- **🔥 Burndown Chart**: Daily progress tracking
- **📊 Status Breakdown**: Issue distribution by status
- **⏳ Cycle Time Analysis**: Time from start to completion
- **🎯 Scope Completion**: Planned vs actual delivery
- **📝 Retrospective Notes**: Capture what went well, improvements, and action items

### 👤 Performance Dashboard

- **📋 Individual Metrics**: Completed issues, cycle time, story points
- **📊 Workload Analysis**: Assigned vs completed work distribution
- **⏱️ Cycle Time Comparison**: Performance benchmarking across team members
- **🔍 Individual Deep Dive**: Detailed analysis for selected team members
- **📈 Progress Tracking**: Estimated vs completed points

### 🎯 OKR Dashboard

- **📈 Progress Visualization**: Progress bars for each key result
- **🚦 Color-coded Status**: On Track (Green), At Risk (Yellow), Behind (Red)
- **📊 Status Distribution**: Overall OKR health overview
- **👥 Owner Analysis**: Progress breakdown by owner
- **🎯 Objective Tracking**: Progress by objective categories
- **📋 Detailed Tables**: Comprehensive OKR status and metrics

## 🔧 Configuration

### Google Sheets Data Format

**Issues Sheet (from Linear):**
- `title`: Issue title
- `assignee`: Team member assigned
- `status`: Current status (Done, In Progress, Todo, etc.)
- `estimate`: Story points estimate
- `createdat`: Issue creation date
- `completedat`: Issue completion date
- `startedat`: Issue start date
- `cycle`: Sprint/cycle name
- `priority`: Priority level
- `type`: Issue type (Feature, Bug, Task, Story)

**OKRs Sheet:**
- `objective`: High-level objective
- `key_result`: Specific key result
- `owner`: Person responsible
- `target`: Target value
- `current`: Current progress value
- `status`: Status (On Track, At Risk, Behind)

### Sample Data

Both dashboards include sample data generators for testing:
- 50 sample issues across 3 sprints with 5 team members
- 5 sample OKRs across different objectives

## 🌐 Deployment Options

### Local Development
```bash
streamlit run scrum_dashboard.py
```

### Streamlit Cloud (Free)
1. Push code to GitHub repository
2. Connect to [share.streamlit.io](https://share.streamlit.io)
3. Deploy and share dashboard URLs

### Custom Hosting
- Deploy on any cloud provider (AWS, GCP, Azure)
- Use Docker for containerized deployment
- Set up reverse proxy for custom domains

## 🔒 Security & Access

### Public Google Sheets
- Make sheets publicly readable for simple setup
- No authentication required
- Suitable for non-sensitive data

### Private Google Sheets
- Use service account credentials
- Store credentials securely (environment variables)
- Better for sensitive organizational data

### Service Account Setup
1. Create service account in Google Cloud Console
2. Generate JSON credentials
3. Share Google Sheet with service account email
4. Use `connect_with_credentials()` method

## 📈 Advanced Features

### Data Refresh
- Linear auto-syncs to Google Sheets hourly
- Dashboards refresh on page reload
- Consider caching for large datasets

### Customization
- Modify chart types and colors in each dashboard
- Add new metrics by extending data processing functions
- Create custom filters and date ranges

### Integration Extensions
- Add Slack notifications for OKR updates
- Export dashboard data to other tools
- Create automated reports via email

## 🐛 Troubleshooting

### Common Issues

**"Failed to connect to Google Sheet"**
- Verify sheet URL format
- Check sheet permissions (public or shared with service account)
- Ensure Linear export is working

**"No data found"**
- Confirm Linear → Google Sheets sync is active
- Check worksheet names match code expectations
- Verify data format matches expected columns

**Import Errors**
```bash
pip install -r requirements.txt
```

**Plotly Charts Not Displaying**
- Clear browser cache
- Try different browser
- Check for ad blockers interfering

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add new dashboard features or improvements
4. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for rapid dashboard development
- Uses [Plotly](https://plotly.com/) for interactive visualizations
- Integrates with [Linear](https://linear.app/) for issue tracking
- Data connection via [gspread](https://github.com/burnash/gspread)

---

## 📞 Support

For questions, issues, or feature requests:
- Create an issue in the repository
- Check the troubleshooting section above
- Review Streamlit and Plotly documentation for customization help

**Happy Scrum Tracking! 🚀** 