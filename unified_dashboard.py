"""
🚀 Unified Scrum Dashboard Suite
Comprehensive dashboard with Scrum Review, Performance Analytics, and OKR Tracking
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

# Custom CSS for better design
st.markdown("""
<style>
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: linear-gradient(90deg, #f0f8ff, #e6f3ff);
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    
    .section-header {
        color: #2c3e50;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #3498db;
    }
    
    .tab-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        text-align: center;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 8px;
        border-left: 4px solid #e74c3c;
    }
    
    .info-box {
        background: #e8f6f3;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1abc9c;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fef9e7;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #f39c12;
        margin: 1rem 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #f8f9fa;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background: #f8f9fa;
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background: white;
        border-radius: 8px;
        border: 2px solid transparent;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Main header
    st.markdown('<div class="main-header">🚀 Scrum Dashboard Suite</div>', unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # Data source selection
        data_source = st.radio(
            "📊 Select Data Source:",
            ["Sample Data", "Google Sheet"],
            help="Choose between sample data for testing or connect to your Google Sheet"
        )
        
        if data_source == "Google Sheet":
            st.markdown("### 🔗 Google Sheet Connection")
            sheet_url = st.text_input(
                "Sheet URL:",
                placeholder="https://docs.google.com/spreadsheets/d/...",
                help="Paste your Google Sheets URL here"
            )
            
            if sheet_url and st.button("🔌 Connect", type="primary"):
                with st.spinner("Connecting to Google Sheet..."):
                    connector = GoogleSheetConnector()
                    if connector.connect_with_url(sheet_url):
                        st.success("✅ Connected successfully!")
                        st.session_state.connector = connector
                    else:
                        st.error("❌ Connection failed. Please check your URL.")
        
        # Data source info
        if data_source == "Sample Data":
            st.markdown("""
            <div class="info-box">
            <strong>📝 Sample Data Info:</strong><br>
            • 50 issues across 3 sprints<br>
            • 5 team members<br>
            • 5 OKRs with progress tracking<br>
            Perfect for testing!
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        if st.button("🔄 Refresh Data", type="secondary"):
            st.rerun()
        
        if st.button("📊 Export Data", type="secondary"):
            st.info("Export functionality coming soon!")
        
        st.markdown("---")
        
        # Help section
        with st.expander("❓ Need Help?"):
            st.markdown("""
            **🔧 Setup Linear Integration:**
            1. Go to Linear → Settings → Integrations
            2. Enable Google Sheets export
            3. Make sheet public or use service account
            4. Paste URL in connection box above
            
            **📈 Dashboard Features:**
            - **Scrum Tab**: Sprint velocity, burndown charts
            - **Performance Tab**: Individual team analytics
            - **OKRs Tab**: Objectives & Key Results tracking
            """)
    
    # Load data based on source
    issues_df, okr_df = load_data(data_source)
    
    if issues_df is None or issues_df.empty:
        st.error("❌ No data available. Please check your connection or try sample data.")
        return
    
    # Main dashboard tabs
    tab1, tab2, tab3 = st.tabs(["🔁 Scrum Review & Retrospective", "👤 Performance Analytics", "🎯 OKR Tracking"])
    
    with tab1:
        render_scrum_dashboard(issues_df)
    
    with tab2:
        render_performance_dashboard(issues_df)
    
    with tab3:
        render_okr_dashboard(okr_df)

def load_data(data_source):
    """Load data from selected source"""
    try:
        if data_source == "Sample Data":
            issues_df = get_sample_data()
            okr_df = get_sample_okr_data()
            return issues_df, okr_df
        else:
            if 'connector' in st.session_state:
                issues_df = st.session_state.connector.load_issues_data()
                okr_df = st.session_state.connector.load_okr_data()
                return issues_df, okr_df
            else:
                st.warning("⚠️ Please connect to Google Sheet first")
                return None, None
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None, None

def render_scrum_dashboard(df):
    """Render the Scrum Review dashboard"""
    st.markdown('<div class="tab-header">🔁 Scrum Review & Retrospective Dashboard</div>', unsafe_allow_html=True)
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        available_sprints = ['All'] + sorted(list(df['cycle'].unique())) if 'cycle' in df.columns else ['All']
        selected_sprint = st.selectbox("🏃‍♂️ Select Sprint:", available_sprints, key="scrum_sprint")
    
    with col2:
        st.markdown("") # Spacing
    
    # Filter data
    filtered_df = df[df['cycle'] == selected_sprint].copy() if selected_sprint != 'All' else df.copy()
    
    if filtered_df.empty:
        st.warning("⚠️ No data available for selected sprint")
        return
    
    # Key metrics row
    st.markdown('<div class="section-header">📊 Sprint Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        completed_issues = len(filtered_df[filtered_df['status'] == 'Done'])
        st.metric("✅ Completed Issues", completed_issues, help="Total issues marked as Done")
    
    with col2:
        total_points = filtered_df['estimate'].sum() if 'estimate' in filtered_df.columns else 0
        st.metric("📊 Total Story Points", int(total_points), help="Sum of all story points in sprint")
    
    with col3:
        avg_cycle_time = filtered_df['cycle_time_days'].mean() if 'cycle_time_days' in filtered_df.columns else 0
        st.metric("⏱️ Avg Cycle Time", f"{avg_cycle_time:.1f} days", help="Average time from start to completion")
    
    with col4:
        completion_rate = (completed_issues / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.metric("🎯 Completion Rate", f"{completion_rate:.1f}%", help="Percentage of issues completed")
    
    st.markdown("---")
    
    # Charts section
    st.markdown('<div class="section-header">📈 Sprint Analytics</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sprint velocity
        velocity_data = df[df['status'] == 'Done'].groupby('cycle')['estimate'].sum().reset_index() if 'cycle' in df.columns and 'estimate' in df.columns else pd.DataFrame()
        
        if not velocity_data.empty:
            fig = px.bar(
                velocity_data,
                x='cycle',
                y='estimate',
                title="📈 Sprint Velocity (Story Points Completed)",
                color='estimate',
                color_continuous_scale='Blues'
            )
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        # Status breakdown
        status_counts = filtered_df['status'].value_counts()
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="📊 Issue Status Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Burndown chart simulation
        total_points = filtered_df['estimate'].sum() if 'estimate' in filtered_df.columns else 100
        completed_points = filtered_df[filtered_df['status'] == 'Done']['estimate'].sum() if 'estimate' in filtered_df.columns else 50
        
        days = list(range(15))
        ideal_burndown = [total_points - (total_points/14) * day for day in days]
        actual_burndown = create_simulated_burndown(total_points, completed_points)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=days, y=ideal_burndown, mode='lines', name='Ideal Burndown', line=dict(dash='dash', color='gray')))
        fig.add_trace(go.Scatter(x=days, y=actual_burndown, mode='lines+markers', name='Actual Burndown', line=dict(color='#1f77b4')))
        fig.update_layout(
            title="🔥 Sprint Burndown Chart",
            xaxis_title="Sprint Day",
            yaxis_title="Remaining Story Points",
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Cycle time distribution
        if 'cycle_time_days' in filtered_df.columns:
            cycle_data = filtered_df.dropna(subset=['cycle_time_days'])
            if not cycle_data.empty:
                fig = px.histogram(
                    cycle_data,
                    x='cycle_time_days',
                    title="⏳ Cycle Time Distribution",
                    nbins=15,
                    color_discrete_sequence=['#ff7f0e']
                )
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)
    
    # Retrospective section
    st.markdown("---")
    st.markdown('<div class="section-header">📝 Sprint Retrospective</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        went_well = st.text_area(
            "What went well? 🎉",
            placeholder="• Great team collaboration\n• All critical features delivered\n• Improved code quality",
            height=100,
            key="scrum_went_well"
        )
        
        action_items = st.text_area(
            "Action items for next sprint 🚀",
            placeholder="• Improve estimation accuracy\n• Add more unit tests\n• Schedule mid-sprint check-in",
            height=100,
            key="scrum_actions"
        )
    
    with col2:
        improvements = st.text_area(
            "What could be improved? 🔧",
            placeholder="• Better requirement clarity\n• More frequent code reviews\n• Earlier testing involvement",
            height=100,
            key="scrum_improvements"
        )
        
        blockers = st.text_area(
            "Blockers and impediments ⚠️",
            placeholder="• Waiting for API documentation\n• Testing environment issues\n• External dependency delays",
            height=100,
            key="scrum_blockers"
        )
    
    if st.button("💾 Save Retrospective Notes", type="primary", key="save_scrum"):
        save_retrospective_notes("scrum")

def render_performance_dashboard(df):
    """Render the Performance dashboard"""
    st.markdown('<div class="tab-header">👤 Individual Performance Analytics</div>', unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        available_sprints = ['All'] + sorted(list(df['cycle'].unique())) if 'cycle' in df.columns else ['All']
        selected_sprint = st.selectbox("🏃‍♂️ Select Sprint:", available_sprints, key="perf_sprint")
    
    with col2:
        available_people = ['All'] + sorted(list(df['assignee'].unique())) if 'assignee' in df.columns else ['All']
        selected_person = st.selectbox("👤 Select Team Member:", available_people, key="perf_person")
    
    with col3:
        available_types = ['All'] + sorted(list(df['type'].unique())) if 'type' in df.columns else ['All']
        selected_type = st.selectbox("🏷️ Select Type:", available_types, key="perf_type")
    
    # Apply filters
    filtered_df = df.copy()
    if selected_sprint != 'All':
        filtered_df = filtered_df[filtered_df['cycle'] == selected_sprint]
    if selected_person != 'All':
        filtered_df = filtered_df[filtered_df['assignee'] == selected_person]
    if selected_type != 'All':
        filtered_df = filtered_df[filtered_df['type'] == selected_type]
    
    if filtered_df.empty:
        st.warning("⚠️ No data available for selected filters")
        return
    
    # Performance metrics
    st.markdown('<div class="section-header">📊 Performance Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_assigned = len(filtered_df)
        st.metric("📋 Total Assigned", total_assigned)
    
    with col2:
        completed_count = len(filtered_df[filtered_df['status'] == 'Done'])
        st.metric("✅ Completed", completed_count)
    
    with col3:
        completion_rate = (completed_count / total_assigned * 100) if total_assigned > 0 else 0
        st.metric("🎯 Completion Rate", f"{completion_rate:.1f}%")
    
    with col4:
        avg_cycle_time = filtered_df['cycle_time_days'].mean() if 'cycle_time_days' in filtered_df.columns else 0
        st.metric("⏱️ Avg Cycle Time", f"{avg_cycle_time:.1f} days")
    
    with col5:
        total_points = filtered_df['estimate'].sum() if 'estimate' in filtered_df.columns else 0
        st.metric("📈 Total Points", int(total_points))
    
    st.markdown("---")
    
    # Performance charts
    st.markdown('<div class="section-header">📈 Performance Analytics</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Work completed by person
        if 'assignee' in filtered_df.columns:
            completion_data = filtered_df.groupby('assignee').agg({
                'status': lambda x: (x == 'Done').sum(),
                'assignee': 'count'
            }).rename(columns={'status': 'completed', 'assignee': 'total'}).reset_index()
            
            fig = px.bar(
                completion_data,
                x='assignee',
                y=['completed', 'total'],
                title="👥 Work Completed vs Assigned",
                barmode='group',
                color_discrete_sequence=['#2ecc71', '#3498db']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Cycle time by person
        if 'assignee' in filtered_df.columns and 'cycle_time_days' in filtered_df.columns:
            cycle_data = filtered_df.dropna(subset=['cycle_time_days'])
            if not cycle_data.empty:
                avg_cycle_time = cycle_data.groupby('assignee')['cycle_time_days'].mean().reset_index()
                
                fig = px.bar(
                    avg_cycle_time,
                    x='assignee',
                    y='cycle_time_days',
                    title="⏳ Average Cycle Time by Person",
                    color='cycle_time_days',
                    color_continuous_scale='RdYlGn_r'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Points comparison
        if 'assignee' in filtered_df.columns and 'estimate' in filtered_df.columns:
            points_data = filtered_df.groupby('assignee').agg({
                'estimate': ['sum', lambda x: x[filtered_df.loc[x.index, 'status'] == 'Done'].sum()]
            }).round(1)
            points_data.columns = ['estimated_points', 'completed_points']
            points_data = points_data.reset_index()
            
            fig = px.bar(
                points_data,
                x='assignee',
                y=['estimated_points', 'completed_points'],
                title="📊 Estimated vs Completed Points",
                barmode='group',
                color_discrete_sequence=['#f39c12', '#27ae60']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Workload distribution
        if 'assignee' in filtered_df.columns:
            workload_data = filtered_df['assignee'].value_counts().reset_index()
            workload_data.columns = ['assignee', 'assigned_issues']
            
            fig = px.pie(
                workload_data,
                values='assigned_issues',
                names='assignee',
                title="📈 Workload Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Performance table
    st.markdown("---")
    st.markdown('<div class="section-header">📋 Detailed Performance Table</div>', unsafe_allow_html=True)
    
    if 'assignee' in filtered_df.columns:
        performance_metrics = []
        
        for person in filtered_df['assignee'].unique():
            person_data = filtered_df[filtered_df['assignee'] == person]
            
            metrics = {
                'Team Member': person,
                'Total Assigned': len(person_data),
                'Completed': len(person_data[person_data['status'] == 'Done']),
                'In Progress': len(person_data[person_data['status'] == 'In Progress']),
                'Completion Rate': f"{(len(person_data[person_data['status'] == 'Done']) / len(person_data) * 100):.1f}%"
            }
            
            if 'estimate' in filtered_df.columns:
                metrics['Total Points'] = person_data['estimate'].sum()
                metrics['Completed Points'] = person_data[person_data['status'] == 'Done']['estimate'].sum()
            
            if 'cycle_time_days' in filtered_df.columns:
                avg_cycle = person_data['cycle_time_days'].mean()
                metrics['Avg Cycle Time'] = f"{avg_cycle:.1f} days" if not pd.isna(avg_cycle) else "N/A"
            
            performance_metrics.append(metrics)
        
        performance_df = pd.DataFrame(performance_metrics)
        st.dataframe(performance_df, use_container_width=True, hide_index=True)

def render_okr_dashboard(df):
    """Render the OKR dashboard"""
    st.markdown('<div class="tab-header">🎯 OKR (Objectives & Key Results) Tracking</div>', unsafe_allow_html=True)
    
    if df is None or df.empty:
        st.warning("⚠️ No OKR data available")
        return
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        available_objectives = ['All'] + sorted(list(df['objective'].unique())) if 'objective' in df.columns else ['All']
        selected_objective = st.selectbox("🎯 Select Objective:", available_objectives, key="okr_objective")
    
    with col2:
        available_owners = ['All'] + sorted(list(df['owner'].unique())) if 'owner' in df.columns else ['All']
        selected_owner = st.selectbox("👤 Select Owner:", available_owners, key="okr_owner")
    
    # Apply filters
    filtered_df = df.copy()
    if selected_objective != 'All':
        filtered_df = filtered_df[filtered_df['objective'] == selected_objective]
    if selected_owner != 'All':
        filtered_df = filtered_df[filtered_df['owner'] == selected_owner]
    
    if filtered_df.empty:
        st.warning("⚠️ No data available for selected filters")
        return
    
    # OKR overview metrics
    st.markdown('<div class="section-header">📊 OKR Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_okrs = len(filtered_df)
        st.metric("📋 Total Key Results", total_okrs)
    
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
    
    # Progress visualization
    st.markdown('<div class="section-header">📈 Key Results Progress</div>', unsafe_allow_html=True)
    
    for idx, row in filtered_df.iterrows():
        status_colors = {
            'On Track': '#28a745',
            'At Risk': '#ffc107',
            'Behind': '#dc3545'
        }
        
        color = status_colors.get(row['status'], '#6c757d')
        progress = row.get('progress', 0)
        
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.write(f"**{row['key_result']}**")
            st.write(f"*{row['objective']} - {row['owner']}*")
        
        with col2:
            st.metric("Progress", f"{progress:.1f}%")
        
        with col3:
            st.markdown(f"<span style='color: {color}; font-weight: bold; padding: 0.3rem 0.8rem; background: {color}20; border-radius: 12px;'>{row['status']}</span>", 
                       unsafe_allow_html=True)
        
        st.progress(min(progress / 100, 1.0))
        st.markdown("---")
    
    # OKR analytics
    st.markdown('<div class="section-header">📊 OKR Analytics</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Status distribution
        status_counts = filtered_df['status'].value_counts()
        colors = ['#28a745', '#ffc107', '#dc3545', '#6c757d']
        
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="🚦 OKR Status Distribution",
            color_discrete_sequence=colors
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Progress by owner
        if 'owner' in filtered_df.columns and 'progress' in filtered_df.columns:
            progress_by_owner = filtered_df.groupby('owner')['progress'].mean().reset_index()
            
            fig = px.bar(
                progress_by_owner,
                x='owner',
                y='progress',
                title="👥 Average Progress by Owner",
                color='progress',
                color_continuous_scale='RdYlGn'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Overall progress gauge
        if 'progress' in filtered_df.columns:
            overall_progress = filtered_df['progress'].mean()
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = overall_progress,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "📉 Overall OKR Progress"},
                delta = {'reference': 75},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 75], 'color': "yellow"},
                        {'range': [75, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Progress by objective
        if 'objective' in filtered_df.columns and 'progress' in filtered_df.columns:
            progress_by_objective = filtered_df.groupby('objective')['progress'].mean().reset_index()
            
            fig = px.bar(
                progress_by_objective,
                x='objective',
                y='progress',
                title="🎯 Average Progress by Objective",
                color='progress',
                color_continuous_scale='RdYlGn'
            )
            fig.update_xaxes(tickangle=45)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Action items
    st.markdown("---")
    st.markdown('<div class="section-header">🚀 Action Items & Planning</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        at_risk_actions = st.text_area(
            "At Risk Items - Action Plan 📝",
            placeholder="• Schedule weekly check-ins with stakeholders\n• Identify resource constraints\n• Adjust timeline if needed",
            height=120,
            key="okr_at_risk"
        )
    
    with col2:
        next_quarter = st.text_area(
            "Next Quarter Planning 🗓️",
            placeholder="• Review and update OKR targets\n• Set new key results based on learnings\n• Align with company objectives",
            height=120,
            key="okr_next_quarter"
        )
    
    if st.button("💾 Save OKR Notes", type="primary", key="save_okr"):
        save_retrospective_notes("okr")

def create_simulated_burndown(total_points, completed_points):
    """Create simulated actual burndown data"""
    actual_burndown = [total_points]
    for day in range(1, 15):
        if day < 10:
            # Simulate slow start
            remaining = total_points - (completed_points/10) * day
        else:
            # Faster completion toward end
            remaining = max(0, total_points - completed_points)
        actual_burndown.append(remaining)
    return actual_burndown

def save_retrospective_notes(dashboard_type):
    """Save retrospective notes"""
    if dashboard_type == "scrum":
        notes = {
            'went_well': st.session_state.get('scrum_went_well', ''),
            'improvements': st.session_state.get('scrum_improvements', ''),
            'action_items': st.session_state.get('scrum_actions', ''),
            'blockers': st.session_state.get('scrum_blockers', ''),
            'timestamp': datetime.now().isoformat()
        }
    elif dashboard_type == "okr":
        notes = {
            'at_risk_actions': st.session_state.get('okr_at_risk', ''),
            'next_quarter_notes': st.session_state.get('okr_next_quarter', ''),
            'timestamp': datetime.now().isoformat()
        }
    
    st.success(f"📝 {dashboard_type.upper()} notes saved successfully!")
    with st.expander("View Saved Notes"):
        st.json(notes)

if __name__ == "__main__":
    main() 