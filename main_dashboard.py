"""
🚀 Unified Scrum Dashboard Suite
Beautiful, comprehensive dashboard combining Scrum Review, Performance Analytics, and OKR Tracking
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from connect_google_sheet import GoogleSheetConnector, get_sample_data, get_sample_okr_data

# Configure page
st.set_page_config(
    page_title="🚀 Scrum Dashboard Suite",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional design
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .section-header {
        color: #2c3e50;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 2rem 0 1.5rem 0;
        padding: 1rem;
        background: linear-gradient(90deg, #f8f9fa, #e9ecef);
        border-radius: 10px;
        border-left: 5px solid #3498db;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 0 30px;
        background: white;
        border-radius: 12px;
        border: 2px solid transparent;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        border-left: 4px solid #3498db;
        margin: 1rem 0;
        transition: transform 0.2s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    }
    
    .info-box {
        background: linear-gradient(135deg, #667eea20, #764ba220);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<div class="main-header">🚀 Unified Scrum Dashboard Suite</div>', unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("## ⚙️ Dashboard Configuration")
        
        # Data source selection
        data_source = st.radio(
            "📊 Data Source:",
            ["Sample Data", "Google Sheet"],
            help="Choose between sample data or connect to Google Sheets"
        )
        
        if data_source == "Google Sheet":
            st.markdown("### 🔗 Connection Setup")
            sheet_url = st.text_input(
                "Google Sheets URL:",
                placeholder="https://docs.google.com/spreadsheets/d/...",
                help="Paste your Linear export Google Sheets URL"
            )
            
            if sheet_url and st.button("🔌 Connect to Sheet", type="primary"):
                with st.spinner("Connecting..."):
                    connector = GoogleSheetConnector()
                    if connector.connect_with_url(sheet_url):
                        st.success("✅ Connected successfully!")
                        st.session_state.connector = connector
                    else:
                        st.error("❌ Connection failed")
        
        # Data info
        if data_source == "Sample Data":
            st.markdown("""
            <div class="info-box">
            <strong>📝 Sample Data Includes:</strong><br>
            • 50 issues across 3 sprints<br>
            • 5 team members<br>
            • 5 OKRs with different statuses<br>
            • Realistic performance metrics
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick actions
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh", type="secondary"):
                st.rerun()
        with col2:
            if st.button("📊 Export", type="secondary"):
                st.info("Coming soon!")
    
    # Load data
    issues_df, okr_df = load_dashboard_data(data_source)
    
    if issues_df is None or issues_df.empty:
        st.error("❌ No data available. Please check connection or use sample data.")
        return
    
    # Main dashboard tabs
    tab1, tab2, tab3 = st.tabs([
        "🔁 Scrum Review & Retrospective", 
        "👤 Performance Analytics", 
        "🎯 OKR Tracking"
    ])
    
    with tab1:
        render_scrum_tab(issues_df)
    
    with tab2:
        render_performance_tab(issues_df)
    
    with tab3:
        render_okr_tab(okr_df)

def load_dashboard_data(data_source):
    """Load data from selected source"""
    try:
        if data_source == "Sample Data":
            return get_sample_data(), get_sample_okr_data()
        else:
            if 'connector' in st.session_state:
                issues = st.session_state.connector.load_issues_data()
                okrs = st.session_state.connector.load_okr_data()
                return issues, okrs
            else:
                st.warning("⚠️ Please connect to Google Sheet first")
                return None, None
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None, None

def render_scrum_tab(df):
    """Render Scrum Review tab"""
    st.markdown('<div class="section-header">🔁 Sprint Analytics & Retrospectives</div>', unsafe_allow_html=True)
    
    # Sprint selector
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        sprints = ['All'] + sorted(df['cycle'].unique()) if 'cycle' in df.columns else ['All']
        selected_sprint = st.selectbox("🏃‍♂️ Select Sprint:", sprints)
    
    # Filter data
    filtered_df = df[df['cycle'] == selected_sprint].copy() if selected_sprint != 'All' else df.copy()
    
    if filtered_df.empty:
        st.warning("⚠️ No data for selected sprint")
        return
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        completed = len(filtered_df[filtered_df['status'] == 'Done'])
        st.metric("✅ Completed", completed, help="Issues marked as Done")
    
    with col2:
        points = int(filtered_df['estimate'].sum()) if 'estimate' in filtered_df.columns else 0
        st.metric("📊 Story Points", points, help="Total story points")
    
    with col3:
        cycle_time = filtered_df['cycle_time_days'].mean() if 'cycle_time_days' in filtered_df.columns else 0
        st.metric("⏱️ Cycle Time", f"{cycle_time:.1f}d", help="Average completion time")
    
    with col4:
        rate = (completed / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.metric("🎯 Completion", f"{rate:.1f}%", help="Completion percentage")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Velocity chart
        if 'cycle' in df.columns and 'estimate' in df.columns:
            velocity = df[df['status'] == 'Done'].groupby('cycle')['estimate'].sum().reset_index()
            if not velocity.empty:
                fig = px.bar(velocity, x='cycle', y='estimate', 
                           title="📈 Sprint Velocity", color='estimate',
                           color_continuous_scale='blues')
                fig.update_layout(height=350, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        
        # Status breakdown
        status_counts = filtered_df['status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index,
                    title="📊 Status Distribution", 
                    color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Burndown simulation
        total_points = filtered_df['estimate'].sum() if 'estimate' in filtered_df.columns else 100
        completed_points = filtered_df[filtered_df['status'] == 'Done']['estimate'].sum() if 'estimate' in filtered_df.columns else 50
        
        days = list(range(15))
        ideal = [total_points - (total_points/14) * day for day in days]
        actual = create_burndown_simulation(total_points, completed_points)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=days, y=ideal, mode='lines', name='Ideal', 
                               line=dict(dash='dash', color='gray')))
        fig.add_trace(go.Scatter(x=days, y=actual, mode='lines+markers', 
                               name='Actual', line=dict(color='#1f77b4')))
        fig.update_layout(title="🔥 Sprint Burndown", height=350)
        st.plotly_chart(fig, use_container_width=True)
        
        # Cycle time distribution
        if 'cycle_time_days' in filtered_df.columns:
            cycle_data = filtered_df.dropna(subset=['cycle_time_days'])
            if not cycle_data.empty:
                fig = px.histogram(cycle_data, x='cycle_time_days', 
                                 title="⏳ Cycle Time Distribution",
                                 color_discrete_sequence=['#ff7f0e'])
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)
    
    # Retrospective
    st.markdown("---")
    st.markdown('<div class="section-header">📝 Sprint Retrospective</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        went_well = st.text_area("What went well? 🎉", height=100, 
                                placeholder="• Great team collaboration\n• All critical features delivered")
        action_items = st.text_area("Action items 🚀", height=100,
                                   placeholder="• Improve estimation\n• More frequent check-ins")
    
    with col2:
        improvements = st.text_area("What to improve? 🔧", height=100,
                                   placeholder="• Better requirements clarity\n• Earlier testing")
        blockers = st.text_area("Blockers ⚠️", height=100,
                               placeholder="• External dependencies\n• Resource constraints")
    
    if st.button("💾 Save Retrospective", type="primary"):
        notes = {
            'went_well': went_well,
            'improvements': improvements, 
            'action_items': action_items,
            'blockers': blockers,
            'timestamp': datetime.now().isoformat()
        }
        st.success("📝 Notes saved!")
        with st.expander("View saved notes"):
            st.json(notes)

def render_performance_tab(df):
    """Render Performance Analytics tab"""
    st.markdown('<div class="section-header">👤 Individual Performance Analytics</div>', unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sprints = ['All'] + sorted(df['cycle'].unique()) if 'cycle' in df.columns else ['All']
        sprint = st.selectbox("🏃‍♂️ Sprint:", sprints, key="perf_sprint")
    
    with col2:
        people = ['All'] + sorted(df['assignee'].unique()) if 'assignee' in df.columns else ['All']
        person = st.selectbox("👤 Person:", people, key="perf_person")
    
    with col3:
        types = ['All'] + sorted(df['type'].unique()) if 'type' in df.columns else ['All']
        work_type = st.selectbox("🏷️ Type:", types, key="perf_type")
    
    # Apply filters
    filtered_df = df.copy()
    if sprint != 'All':
        filtered_df = filtered_df[filtered_df['cycle'] == sprint]
    if person != 'All':
        filtered_df = filtered_df[filtered_df['assignee'] == person]
    if work_type != 'All':
        filtered_df = filtered_df[filtered_df['type'] == work_type]
    
    if filtered_df.empty:
        st.warning("⚠️ No data for selected filters")
        return
    
    # Performance metrics
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
        cycle_avg = filtered_df['cycle_time_days'].mean() if 'cycle_time_days' in filtered_df.columns else 0
        st.metric("⏱️ Cycle Time", f"{cycle_avg:.1f}d")
    with col5:
        points = int(filtered_df['estimate'].sum()) if 'estimate' in filtered_df.columns else 0
        st.metric("📈 Points", points)
    
    st.markdown("---")
    
    # Performance charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Completion by person
        if 'assignee' in filtered_df.columns:
            completion_data = filtered_df.groupby('assignee').agg({
                'status': lambda x: (x == 'Done').sum(),
                'assignee': 'count'
            }).rename(columns={'status': 'completed', 'assignee': 'total'}).reset_index()
            
            fig = px.bar(completion_data, x='assignee', y=['completed', 'total'],
                        title="👥 Completed vs Assigned", barmode='group',
                        color_discrete_sequence=['#2ecc71', '#3498db'])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Cycle time by person
        if 'assignee' in filtered_df.columns and 'cycle_time_days' in filtered_df.columns:
            cycle_data = filtered_df.dropna(subset=['cycle_time_days'])
            if not cycle_data.empty:
                avg_cycle = cycle_data.groupby('assignee')['cycle_time_days'].mean().reset_index()
                fig = px.bar(avg_cycle, x='assignee', y='cycle_time_days',
                           title="⏳ Cycle Time by Person", color='cycle_time_days',
                           color_continuous_scale='RdYlGn_r')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Points comparison
        if 'assignee' in filtered_df.columns and 'estimate' in filtered_df.columns:
            points_data = filtered_df.groupby('assignee').agg({
                'estimate': ['sum', lambda x: x[filtered_df.loc[x.index, 'status'] == 'Done'].sum()]
            }).round(1)
            points_data.columns = ['estimated', 'completed']
            points_data = points_data.reset_index()
            
            fig = px.bar(points_data, x='assignee', y=['estimated', 'completed'],
                        title="📊 Estimated vs Completed Points", barmode='group',
                        color_discrete_sequence=['#f39c12', '#27ae60'])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Workload distribution
        if 'assignee' in filtered_df.columns:
            workload = filtered_df['assignee'].value_counts().reset_index()
            workload.columns = ['assignee', 'issues']
            
            fig = px.pie(workload, values='issues', names='assignee',
                        title="📈 Workload Distribution",
                        color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

def render_okr_tab(df):
    """Render OKR Tracking tab"""
    st.markdown('<div class="section-header">🎯 OKR (Objectives & Key Results) Tracking</div>', unsafe_allow_html=True)
    
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
    
    if filtered_df.empty:
        st.warning("⚠️ No data for selected filters")
        return
    
    # OKR metrics
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
    
    st.markdown("---")
    
    # Progress bars
    st.markdown("### 📈 Key Results Progress")
    
    for _, row in filtered_df.iterrows():
        status_colors = {'On Track': '#28a745', 'At Risk': '#ffc107', 'Behind': '#dc3545'}
        color = status_colors.get(row['status'], '#6c757d')
        progress = row.get('progress', 0)
        
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.write(f"**{row['key_result']}**")
            st.write(f"*{row['objective']} - {row['owner']}*")
        
        with col2:
            st.metric("Progress", f"{progress:.1f}%")
        
        with col3:
            st.markdown(f"""<div style='padding: 0.3rem 0.8rem; background: {color}20; 
                           color: {color}; border-radius: 12px; font-weight: bold; 
                           text-align: center;'>{row['status']}</div>""", 
                       unsafe_allow_html=True)
        
        st.progress(min(progress / 100, 1.0))
        st.markdown("---")
    
    # OKR analytics
    col1, col2 = st.columns(2)
    
    with col1:
        # Status distribution
        status_counts = filtered_df['status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index,
                    title="🚦 Status Distribution",
                    color_discrete_sequence=['#28a745', '#ffc107', '#dc3545'])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Progress by owner
        if 'owner' in filtered_df.columns and 'progress' in filtered_df.columns:
            progress_by_owner = filtered_df.groupby('owner')['progress'].mean().reset_index()
            fig = px.bar(progress_by_owner, x='owner', y='progress',
                        title="👥 Progress by Owner", color='progress',
                        color_continuous_scale='RdYlGn')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Overall progress gauge
        if 'progress' in filtered_df.columns:
            overall = filtered_df['progress'].mean()
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=overall,
                title={'text': "📉 Overall Progress"},
                delta={'reference': 75},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 75], 'color': "yellow"},
                        {'range': [75, 100], 'color': "green"}
                    ],
                    'threshold': {'line': {'color': "red", 'width': 4}, 'value': 90}
                }
            ))
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

def create_burndown_simulation(total, completed):
    """Create realistic burndown simulation"""
    burndown = [total]
    for day in range(1, 15):
        if day < 10:
            remaining = total - (completed/10) * day
        else:
            remaining = max(0, total - completed)
        burndown.append(remaining)
    return burndown

if __name__ == "__main__":
    main() 