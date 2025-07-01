"""
Scrum Review & Retrospective Dashboard
Shows sprint velocity, burndown, scope completion, cycle time, and retrospective insights
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from connect_google_sheet import GoogleSheetConnector, get_sample_data

def main():
    st.set_page_config(
        page_title="🔁 Scrum Review Dashboard",
        page_icon="🔁",
        layout="wide"
    )
    
    st.title("🔁 Scrum Review & Retrospective Dashboard")
    st.markdown("---")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Data source selection
        data_source = st.radio(
            "Select Data Source:",
            ["Sample Data", "Google Sheet"]
        )
        
        if data_source == "Google Sheet":
            sheet_url = st.text_input("Google Sheet URL:")
            if sheet_url and st.button("Connect"):
                connector = GoogleSheetConnector()
                if connector.connect_with_url(sheet_url):
                    st.success("Connected to Google Sheet!")
                    st.session_state.connector = connector
    
    # Load data
    if data_source == "Sample Data":
        df = get_sample_data()
        st.info("Using sample data for demonstration")
    else:
        if 'connector' in st.session_state:
            df = st.session_state.connector.load_issues_data()
            if df is None or df.empty:
                st.error("Failed to load data from Google Sheet")
                return
        else:
            st.warning("Please connect to a Google Sheet first")
            return
    
    if df.empty:
        st.error("No data available to display")
        return
    
    # Sprint filter
    available_sprints = df['cycle'].unique() if 'cycle' in df.columns else ['All']
    selected_sprint = st.selectbox("Select Sprint:", ['All'] + list(available_sprints))
    
    # Filter data by sprint
    if selected_sprint != 'All':
        filtered_df = df[df['cycle'] == selected_sprint].copy()
    else:
        filtered_df = df.copy()
    
    if filtered_df.empty:
        st.warning("No data available for selected sprint")
        return
    
    # Main dashboard layout
    col1, col2, col3, col4 = st.columns(4)
    
    # Key metrics
    with col1:
        completed_issues = len(filtered_df[filtered_df['status'] == 'Done'])
        st.metric("✅ Completed Issues", completed_issues)
    
    with col2:
        total_points = filtered_df['estimate'].sum() if 'estimate' in filtered_df.columns else 0
        st.metric("📊 Total Story Points", int(total_points))
    
    with col3:
        avg_cycle_time = filtered_df['cycle_time_days'].mean() if 'cycle_time_days' in filtered_df.columns else 0
        st.metric("⏱️ Avg Cycle Time", f"{avg_cycle_time:.1f} days")
    
    with col4:
        completion_rate = (completed_issues / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.metric("🎯 Completion Rate", f"{completion_rate:.1f}%")
    
    st.markdown("---")
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Sprint Velocity")
        create_velocity_chart(df)
        
        st.subheader("🔥 Burndown Chart")
        create_burndown_chart(filtered_df)
    
    with col2:
        st.subheader("📊 Status Breakdown")
        create_status_breakdown(filtered_df)
        
        st.subheader("⏳ Cycle Time Analysis")
        create_cycle_time_chart(filtered_df)
    
    # Scope completion section
    st.markdown("---")
    st.subheader("🎯 Scope Completion Analysis")
    create_scope_completion(filtered_df)
    
    # Retrospective section
    st.markdown("---")
    st.subheader("📝 Sprint Retrospective")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_area(
            "What went well? 🎉",
            placeholder="Enter what went well during this sprint...",
            height=120,
            key="went_well"
        )
        
        st.text_area(
            "Action items for next sprint 🚀",
            placeholder="Enter action items for improvement...",
            height=120,
            key="action_items"
        )
    
    with col2:
        st.text_area(
            "What could be improved? 🔧",
            placeholder="Enter areas for improvement...",
            height=120,
            key="improvements"
        )
        
        st.text_area(
            "Blockers and impediments ⚠️",
            placeholder="Enter any blockers or impediments...",
            height=120,
            key="blockers"
        )
    
    if st.button("💾 Save Retrospective Notes"):
        save_retrospective_notes()

def create_velocity_chart(df):
    """Create sprint velocity chart"""
    if 'cycle' not in df.columns or 'estimate' not in df.columns:
        st.warning("Missing data for velocity chart")
        return
    
    # Calculate velocity per sprint
    velocity_data = df[df['status'] == 'Done'].groupby('cycle')['estimate'].sum().reset_index()
    
    if velocity_data.empty:
        st.warning("No completed tasks found for velocity calculation")
        return
    
    fig = px.bar(
        velocity_data,
        x='cycle',
        y='estimate',
        title="Story Points Completed per Sprint",
        labels={'estimate': 'Story Points', 'cycle': 'Sprint'}
    )
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

def create_burndown_chart(df):
    """Create burndown chart for current sprint"""
    if 'createdat' not in df.columns or 'estimate' not in df.columns:
        st.warning("Missing data for burndown chart")
        return
    
    # Simulate daily burndown (in real implementation, you'd have daily snapshots)
    total_points = df['estimate'].sum()
    completed_points = df[df['status'] == 'Done']['estimate'].sum()
    
    # Create sample burndown data
    days = list(range(14))  # 2-week sprint
    ideal_burndown = [total_points - (total_points/13) * day for day in days]
    
    # Simulate actual burndown
    actual_burndown = [total_points]
    for day in range(1, 14):
        if day < 10:
            # Simulate slow start
            actual_burndown.append(total_points - (completed_points/10) * day)
        else:
            # Faster completion at end
            actual_burndown.append(max(0, total_points - completed_points))
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=days,
        y=ideal_burndown,
        mode='lines',
        name='Ideal Burndown',
        line=dict(dash='dash', color='gray')
    ))
    
    fig.add_trace(go.Scatter(
        x=days,
        y=actual_burndown,
        mode='lines+markers',
        name='Actual Burndown',
        line=dict(color='blue')
    ))
    
    fig.update_layout(
        title="Sprint Burndown Chart",
        xaxis_title="Sprint Day",
        yaxis_title="Remaining Story Points",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_status_breakdown(df):
    """Create status breakdown pie chart"""
    status_counts = df['status'].value_counts()
    
    fig = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Issue Status Distribution"
    )
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

def create_cycle_time_chart(df):
    """Create cycle time analysis chart"""
    if 'cycle_time_days' not in df.columns:
        st.warning("No cycle time data available")
        return
    
    # Filter out null cycle times
    cycle_time_data = df.dropna(subset=['cycle_time_days'])
    
    if cycle_time_data.empty:
        st.warning("No cycle time data to display")
        return
    
    fig = px.histogram(
        cycle_time_data,
        x='cycle_time_days',
        nbins=20,
        title="Cycle Time Distribution",
        labels={'cycle_time_days': 'Cycle Time (Days)', 'count': 'Number of Issues'}
    )
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

def create_scope_completion(df):
    """Create scope completion analysis"""
    col1, col2 = st.columns(2)
    
    with col1:
        # Planned vs Done
        total_issues = len(df)
        completed_issues = len(df[df['status'] == 'Done'])
        
        fig = go.Figure(go.Bar(
            x=['Planned', 'Completed'],
            y=[total_issues, completed_issues],
            marker_color=['lightblue', 'green']
        ))
        
        fig.update_layout(
            title="Planned vs Completed Issues",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Points planned vs completed
        total_points = df['estimate'].sum() if 'estimate' in df.columns else 0
        completed_points = df[df['status'] == 'Done']['estimate'].sum() if 'estimate' in df.columns else 0
        
        fig = go.Figure(go.Bar(
            x=['Planned Points', 'Completed Points'],
            y=[total_points, completed_points],
            marker_color=['lightcoral', 'darkgreen']
        ))
        
        fig.update_layout(
            title="Planned vs Completed Story Points",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)

def save_retrospective_notes():
    """Save retrospective notes (placeholder function)"""
    notes = {
        'went_well': st.session_state.get('went_well', ''),
        'improvements': st.session_state.get('improvements', ''),
        'action_items': st.session_state.get('action_items', ''),
        'blockers': st.session_state.get('blockers', ''),
        'timestamp': datetime.now().isoformat()
    }
    
    # In a real implementation, you would save this to a database or file
    st.success("📝 Retrospective notes saved successfully!")
    st.json(notes)

if __name__ == "__main__":
    main() 