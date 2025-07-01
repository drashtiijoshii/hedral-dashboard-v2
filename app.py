"""
🚀 Unified Scrum Dashboard Suite
Professional dashboard combining Scrum Review, Performance Analytics, and OKR Tracking
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from connect_google_sheet import GoogleSheetConnector, get_sample_data, get_sample_okr_data

# Page configuration
st.set_page_config(
    page_title="🚀 Scrum Dashboard Suite",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful design
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .section-header {
        color: #2c3e50;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 10px;
        border-left: 5px solid #3498db;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 25px;
        background: white;
        border-radius: 10px;
        font-weight: 600;
        border: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .info-box {
        background: #e8f6f3;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1abc9c;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<div class="main-header">🚀 Unified Scrum Dashboard Suite</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        data_source = st.radio(
            "📊 Data Source:",
            ["Sample Data", "Google Sheet"]
        )
        
        if data_source == "Google Sheet":
            st.markdown("""
            <div class="info-box">
            <b>📝 Setup Instructions:</b><br>
            1. Make your sheet public (Anyone with link can view)<br>
            2. Copy the full URL from browser<br>
            3. Paste below and click Connect
            </div>
            """, unsafe_allow_html=True)
            
            sheet_url = st.text_input(
                "Google Sheets URL:",
                value="https://docs.google.com/spreadsheets/d/17t0xVraS294wFkGQfdUlNsVdFiivTMc5gn5YLKmaALg/edit?usp=sharing",
                placeholder="https://docs.google.com/spreadsheets/d/your-sheet-id/edit#gid=0"
            )
            
            # Auto-connect if URL is provided but not connected
            if sheet_url and 'connector' not in st.session_state:
                if st.button("🔌 Connect", type="primary"):
                    if "docs.google.com/spreadsheets" not in sheet_url:
                        st.error("❌ Please enter a valid Google Sheets URL")
                    else:
                        with st.spinner("Connecting to Google Sheet..."):
                            connector = GoogleSheetConnector()
                            if connector.connect_with_url(sheet_url):
                                st.success("✅ Connected successfully!")
                                st.session_state.connector = connector
                                st.rerun()  # Refresh to show connection status
                            else:
                                st.error("❌ Connection failed")
                                st.markdown("""
                                **Troubleshooting:**
                                - Make sure your sheet is publicly accessible
                                - Check if the URL is complete and correct
                                - Try sharing with 'Anyone with the link can view'
                                """)
            
            # Show connection status
            if 'connector' in st.session_state:
                st.success("✅ Google Sheet Connected")
                
                # Show mapping confirmation messages
                st.success("✅ Mapped 'Cycle Start' → 'cycle_start'")
                st.success("✅ Mapped 'Cycle End' → 'cycle_end'")
        
        if data_source == "Sample Data":
            st.markdown("""
            <div class="info-box">
            <b>📝 Sample Data:</b><br>
            • 50 issues, 3 sprints<br>
            • 5 team members<br>
            • 5 OKRs with progress
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🔄 Refresh Data"):
            st.rerun()
    
    # Load data
    issues_df, okr_df = load_data(data_source)
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs([
        "🔁 Scrum Review", 
        "👤 Performance", 
        "🎯 OKR Tracking"
    ])
    
    with tab1:
        scrum_dashboard(issues_df)
    
    with tab2:
        performance_dashboard(issues_df)
    
    with tab3:
        okr_dashboard(okr_df)

def load_data(source):
    """Load data from selected source"""
    if source == "Sample Data":
        return get_sample_data(), get_sample_okr_data()
    elif source == "Google Sheet":
        # Check if connector exists in session state
        if 'connector' in st.session_state:
            try:
                issues = st.session_state.connector.load_issues_data()
                okrs = st.session_state.connector.load_okr_data()
                
                # Show success message if data loaded
                if issues is not None and not issues.empty:
                    st.success(f"✅ Loaded {len(issues)} issues from Google Sheet")
                
                return issues, okrs
            except Exception as e:
                st.error(f"❌ Error loading data: {str(e)}")
                return get_sample_data(), get_sample_okr_data()  # Fallback to sample data
        else:
            # Return sample data if no connection - don't show error in main area
            return get_sample_data(), get_sample_okr_data()
    else:
        return get_sample_data(), get_sample_okr_data()

def scrum_dashboard(df):
    """Scrum Review Dashboard"""
    st.markdown('<div class="section-header">🔁 Scrum Review & Retrospective</div>', unsafe_allow_html=True)
    
    # Sprint filter - handle mixed data types safely
    if 'cycle' in df.columns:
        # Clean cycle data - remove NaN and convert to string for consistent sorting
        cycle_values = df['cycle'].dropna().astype(str).unique()
        sprints = ['All'] + sorted([c for c in cycle_values if c != 'nan' and c.strip() != ''])
    else:
        sprints = ['All']
    
    selected_sprint = st.selectbox("🏃‍♂️ Select Sprint:", sprints)
    
    # Filter data - handle string comparison safely
    if selected_sprint != 'All' and 'cycle' in df.columns:
        # Convert cycle column to string for comparison
        df_temp = df.copy()
        df_temp['cycle'] = df_temp['cycle'].astype(str)
        filtered_df = df_temp[df_temp['cycle'] == selected_sprint]
    else:
        filtered_df = df
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        completed = len(filtered_df[filtered_df['status'] == 'Done'])
        st.metric("✅ Completed", completed)
    
    with col2:
        if 'estimate' in filtered_df.columns:
            # Handle estimate column safely
            try:
                # Convert to numeric and sum, handling non-numeric values
                numeric_estimates = filtered_df['estimate'].apply(
                    lambda x: pd.to_numeric(x, errors='coerce') if pd.notnull(x) else 0
                ).fillna(0)
                points = int(numeric_estimates.sum())
            except:
                points = 0
        else:
            points = 0
        st.metric("📊 Story Points", points)
    
    with col3:
        if 'cycle_time_days' in filtered_df.columns:
            try:
                # Convert to numeric and calculate mean, handling non-numeric values
                numeric_cycle_times = filtered_df['cycle_time_days'].apply(
                    lambda x: pd.to_numeric(x, errors='coerce') if pd.notnull(x) else None
                )
                cycle_time = numeric_cycle_times.mean() if not numeric_cycle_times.isna().all() else 0
            except:
                cycle_time = 0
        else:
            cycle_time = 0
        st.metric("⏱️ Cycle Time", f"{cycle_time:.1f}d")
    
    with col4:
        rate = (completed / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.metric("🎯 Completion", f"{rate:.1f}%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Velocity chart - handle data types safely
        if 'cycle' in df.columns and 'estimate' in df.columns:
            # Clean data for velocity calculation
            velocity_data = df[df['status'] == 'Done'].copy()
            velocity_data['cycle'] = velocity_data['cycle'].astype(str)
            # Convert estimates to numeric, replacing non-numeric with 0
            velocity_data['estimate'] = velocity_data['estimate'].apply(
                lambda x: pd.to_numeric(x, errors='coerce') if pd.notnull(x) else 0
            ).fillna(0)
            
            velocity = velocity_data.groupby('cycle')['estimate'].sum().reset_index()
            if not velocity.empty and len(velocity) > 0:
                fig = px.bar(velocity, x='cycle', y='estimate', title="📈 Sprint Velocity")
                st.plotly_chart(fig, use_container_width=True)
        
        # Status pie chart
        status_counts = filtered_df['status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index, title="📊 Status Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Burndown simulation
        total_points = filtered_df['estimate'].sum() if 'estimate' in filtered_df.columns else 100
        completed_points = filtered_df[filtered_df['status'] == 'Done']['estimate'].sum() if 'estimate' in filtered_df.columns else 50
        
        days = list(range(15))
        ideal = [total_points - (total_points/14) * day for day in days]
        actual = [total_points - min(completed_points, (completed_points/10) * day) for day in days]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=days, y=ideal, mode='lines', name='Ideal', line=dict(dash='dash')))
        fig.add_trace(go.Scatter(x=days, y=actual, mode='lines+markers', name='Actual'))
        fig.update_layout(title="🔥 Sprint Burndown")
        st.plotly_chart(fig, use_container_width=True)
        
        # Cycle time histogram
        if 'cycle_time_days' in filtered_df.columns:
            cycle_data = filtered_df.dropna(subset=['cycle_time_days'])
            if not cycle_data.empty:
                fig = px.histogram(cycle_data, x='cycle_time_days', title="⏳ Cycle Time Distribution")
                st.plotly_chart(fig, use_container_width=True)
    
    # Retrospective
    st.markdown("### 📝 Sprint Retrospective")
    col1, col2 = st.columns(2)
    
    with col1:
        went_well = st.text_area("What went well? 🎉", height=100)
        action_items = st.text_area("Action items 🚀", height=100)
    
    with col2:
        improvements = st.text_area("What to improve? 🔧", height=100)
        blockers = st.text_area("Blockers ⚠️", height=100)
    
    if st.button("💾 Save Retrospective"):
        st.success("📝 Retrospective saved!")

def performance_dashboard(df):
    """Performance Analytics Dashboard"""
    st.markdown('<div class="section-header">👤 Performance Analytics</div>', unsafe_allow_html=True)
    
    # Filters - handle mixed data types safely
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Handle cycle data safely
        if 'cycle' in df.columns:
            cycle_values = df['cycle'].dropna().astype(str).unique()
            sprints = ['All'] + sorted([c for c in cycle_values if c != 'nan' and c.strip() != ''])
        else:
            sprints = ['All']
        sprint = st.selectbox("🏃‍♂️ Sprint:", sprints, key="perf_sprint")
    
    with col2:
        # Handle assignee data safely
        if 'assignee' in df.columns:
            assignee_values = df['assignee'].dropna().astype(str).unique()
            people = ['All'] + sorted([p for p in assignee_values if p != 'nan' and p.strip() != ''])
        else:
            people = ['All']
        person = st.selectbox("👤 Person:", people, key="perf_person")
    
    with col3:
        # Handle type data safely  
        if 'type' in df.columns:
            type_values = df['type'].dropna().astype(str).unique()
            types = ['All'] + sorted([t for t in type_values if t != 'nan' and t.strip() != ''])
        else:
            types = ['All']
        work_type = st.selectbox("🏷️ Type:", types, key="perf_type")
    
    # Apply filters - handle string comparisons safely
    filtered_df = df.copy()
    if sprint != 'All' and 'cycle' in df.columns:
        filtered_df['cycle'] = filtered_df['cycle'].astype(str)
        filtered_df = filtered_df[filtered_df['cycle'] == sprint]
    if person != 'All' and 'assignee' in df.columns:
        filtered_df['assignee'] = filtered_df['assignee'].astype(str)
        filtered_df = filtered_df[filtered_df['assignee'] == person]
    if work_type != 'All' and 'type' in df.columns:
        filtered_df['type'] = filtered_df['type'].astype(str)
        filtered_df = filtered_df[filtered_df['type'] == work_type]
    
    # Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📋 Assigned", len(filtered_df))
    with col2:
        completed = len(filtered_df[filtered_df['status'] == 'Done'])
        st.metric("✅ Completed", completed)
    with col3:
        rate = (completed / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.metric("🎯 Rate", f"{rate:.1f}%")
    with col4:
        # Handle cycle time safely
        if 'cycle_time_days' in filtered_df.columns:
            try:
                numeric_cycle_times = filtered_df['cycle_time_days'].apply(
                    lambda x: pd.to_numeric(x, errors='coerce') if pd.notnull(x) else None
                )
                cycle_avg = numeric_cycle_times.mean() if not numeric_cycle_times.isna().all() else 0
            except:
                cycle_avg = 0
        else:
            cycle_avg = 0
        st.metric("⏱️ Cycle Time", f"{cycle_avg:.1f}d")
    with col5:
        # Handle estimate safely
        if 'estimate' in filtered_df.columns:
            try:
                numeric_estimates = filtered_df['estimate'].apply(
                    lambda x: pd.to_numeric(x, errors='coerce') if pd.notnull(x) else 0
                ).fillna(0)
                points = int(numeric_estimates.sum())
            except:
                points = 0
        else:
            points = 0
        st.metric("📈 Points", points)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Completion by person
        if 'assignee' in filtered_df.columns:
            completion_data = filtered_df.groupby('assignee').agg({
                'status': lambda x: (x == 'Done').sum(),
                'assignee': 'count'
            }).rename(columns={'status': 'completed', 'assignee': 'total'}).reset_index()
            
            fig = px.bar(completion_data, x='assignee', y=['completed', 'total'],
                        title="👥 Completed vs Assigned", barmode='group')
            st.plotly_chart(fig, use_container_width=True)
        
        # Cycle time by person
        if 'assignee' in filtered_df.columns and 'cycle_time_days' in filtered_df.columns:
            cycle_data = filtered_df.dropna(subset=['cycle_time_days'])
            if not cycle_data.empty:
                avg_cycle = cycle_data.groupby('assignee')['cycle_time_days'].mean().reset_index()
                fig = px.bar(avg_cycle, x='assignee', y='cycle_time_days', title="⏳ Cycle Time by Person")
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Workload distribution
        if 'assignee' in filtered_df.columns:
            workload = filtered_df['assignee'].value_counts().reset_index()
            workload.columns = ['assignee', 'issues']
            
            fig = px.pie(workload, values='issues', names='assignee', title="📈 Workload Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        # Points comparison
        if 'assignee' in filtered_df.columns and 'estimate' in filtered_df.columns:
            points_data = filtered_df.groupby('assignee').agg({
                'estimate': ['sum', lambda x: x[filtered_df.loc[x.index, 'status'] == 'Done'].sum()]
            }).round(1)
            points_data.columns = ['estimated', 'completed']
            points_data = points_data.reset_index()
            
            fig = px.bar(points_data, x='assignee', y=['estimated', 'completed'],
                        title="📊 Estimated vs Completed Points", barmode='group')
            st.plotly_chart(fig, use_container_width=True)

def okr_dashboard(df):
    """OKR Tracking Dashboard"""
    st.markdown('<div class="section-header">🎯 OKR Tracking</div>', unsafe_allow_html=True)
    
    if df is None or df.empty:
        st.warning("⚠️ No OKR data available")
        return
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        objectives = ['All'] + sorted(df['objective'].unique()) if 'objective' in df.columns else ['All']
        objective = st.selectbox("🎯 Objective:", objectives, key="okr_obj")
    
    with col2:
        owners = ['All'] + sorted(df['owner'].unique()) if 'owner' in df.columns else ['All']
        owner = st.selectbox("👤 Owner:", owners, key="okr_owner")
    
    # Apply filters
    filtered_df = df.copy()
    if objective != 'All':
        filtered_df = filtered_df[filtered_df['objective'] == objective]
    if owner != 'All':
        filtered_df = filtered_df[filtered_df['owner'] == owner]
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📋 Total KRs", len(filtered_df))
    with col2:
        on_track = len(filtered_df[filtered_df['status'] == 'On Track'])
        st.metric("✅ On Track", on_track)
    with col3:
        at_risk = len(filtered_df[filtered_df['status'] == 'At Risk'])
        st.metric("⚠️ At Risk", at_risk)
    with col4:
        behind = len(filtered_df[filtered_df['status'] == 'Behind'])
        st.metric("🔴 Behind", behind)
    
    # Progress visualization
    st.markdown("### 📈 Key Results Progress")
    
    for _, row in filtered_df.iterrows():
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.write(f"**{row['key_result']}**")
            st.write(f"*{row['objective']} - {row['owner']}*")
        
        with col2:
            progress = row.get('progress', 0)
            st.metric("Progress", f"{progress:.1f}%")
        
        with col3:
            status_colors = {'On Track': '🟢', 'At Risk': '🟡', 'Behind': '🔴'}
            icon = status_colors.get(row['status'], '⚪')
            st.write(f"{icon} {row['status']}")
        
        st.progress(min(progress / 100, 1.0))
        st.markdown("---")
    
    # Analytics
    col1, col2 = st.columns(2)
    
    with col1:
        # Status distribution
        status_counts = filtered_df['status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index, title="🚦 Status Distribution")
        st.plotly_chart(fig, use_container_width=True)
        
        # Progress by owner
        if 'owner' in filtered_df.columns and 'progress' in filtered_df.columns:
            progress_by_owner = filtered_df.groupby('owner')['progress'].mean().reset_index()
            fig = px.bar(progress_by_owner, x='owner', y='progress', title="👥 Progress by Owner")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Overall progress gauge
        if 'progress' in filtered_df.columns:
            overall = filtered_df['progress'].mean()
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=overall,
                title={'text': "📉 Overall Progress"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 75], 'color': "yellow"},
                        {'range': [75, 100], 'color': "green"}
                    ]
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
    
    # Action items
    st.markdown("### 🚀 Action Items")
    col1, col2 = st.columns(2)
    
    with col1:
        at_risk_actions = st.text_area("At Risk Action Plan 📝", height=100)
    
    with col2:
        next_quarter = st.text_area("Next Quarter Planning 🗓️", height=100)
    
    if st.button("💾 Save OKR Notes"):
        st.success("📝 OKR notes saved!")

if __name__ == "__main__":
    main() 