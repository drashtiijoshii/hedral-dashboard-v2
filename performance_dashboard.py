"""
Individual Team Member Performance Dashboard
Shows per-person KPIs: completed issues, speed, cycle time, workload analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from connect_google_sheet import GoogleSheetConnector, get_sample_data

def main():
    st.set_page_config(
        page_title="👤 Performance Dashboard",
        page_icon="👤",
        layout="wide"
    )
    
    st.title("👤 Individual Team Member Performance Dashboard")
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
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        available_sprints = ['All'] + list(df['cycle'].unique()) if 'cycle' in df.columns else ['All']
        selected_sprint = st.selectbox("Select Sprint:", available_sprints)
    
    with col2:
        available_people = ['All'] + sorted(list(df['assignee'].unique())) if 'assignee' in df.columns else ['All']
        selected_person = st.selectbox("Select Team Member:", available_people)
    
    with col3:
        available_roles = ['All'] + list(df['type'].unique()) if 'type' in df.columns else ['All']
        selected_role = st.selectbox("Select Role/Type:", available_roles)
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_sprint != 'All':
        filtered_df = filtered_df[filtered_df['cycle'] == selected_sprint]
    
    if selected_person != 'All':
        filtered_df = filtered_df[filtered_df['assignee'] == selected_person]
    
    if selected_role != 'All':
        filtered_df = filtered_df[filtered_df['type'] == selected_role]
    
    if filtered_df.empty:
        st.warning("No data available for selected filters")
        return
    
    # Overview metrics
    st.subheader("📊 Performance Overview")
    
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
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👥 Work Completed by Person")
        create_completion_by_person_chart(filtered_df)
        
        st.subheader("📊 Estimated vs Completed Points")
        create_points_comparison_chart(filtered_df)
    
    with col2:
        st.subheader("⏳ Average Cycle Time by Person")
        create_cycle_time_by_person_chart(filtered_df)
        
        st.subheader("📈 Workload Distribution")
        create_workload_distribution_chart(filtered_df)
    
    # Detailed performance table
    st.markdown("---")
    st.subheader("📋 Detailed Performance Table")
    create_performance_table(filtered_df)
    
    # Individual deep dive
    if selected_person != 'All':
        st.markdown("---")
        st.subheader(f"🔍 Deep Dive: {selected_person}")
        create_individual_deep_dive(filtered_df, selected_person)

def create_completion_by_person_chart(df):
    """Create bar chart of completed work by person"""
    if 'assignee' not in df.columns:
        st.warning("No assignee data available")
        return
    
    completion_data = df.groupby('assignee').agg({
        'status': lambda x: (x == 'Done').sum(),
        'assignee': 'count'
    }).rename(columns={'status': 'completed', 'assignee': 'total'})
    
    completion_data = completion_data.reset_index()
    
    fig = px.bar(
        completion_data,
        x='assignee',
        y=['completed', 'total'],
        title="Completed vs Total Issues by Person",
        labels={'value': 'Number of Issues', 'assignee': 'Team Member'},
        barmode='group'
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def create_points_comparison_chart(df):
    """Create comparison of estimated vs completed points"""
    if 'assignee' not in df.columns or 'estimate' not in df.columns:
        st.warning("Missing data for points comparison")
        return
    
    points_data = df.groupby('assignee').agg({
        'estimate': ['sum', lambda x: x[df.loc[x.index, 'status'] == 'Done'].sum()]
    }).round(1)
    
    points_data.columns = ['estimated_points', 'completed_points']
    points_data = points_data.reset_index()
    
    fig = px.bar(
        points_data,
        x='assignee',
        y=['estimated_points', 'completed_points'],
        title="Estimated vs Completed Story Points",
        labels={'value': 'Story Points', 'assignee': 'Team Member'},
        barmode='group'
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def create_cycle_time_by_person_chart(df):
    """Create cycle time analysis by person"""
    if 'assignee' not in df.columns or 'cycle_time_days' not in df.columns:
        st.warning("Missing data for cycle time analysis")
        return
    
    # Filter out null cycle times
    cycle_data = df.dropna(subset=['cycle_time_days'])
    
    if cycle_data.empty:
        st.warning("No cycle time data available")
        return
    
    avg_cycle_time = cycle_data.groupby('assignee')['cycle_time_days'].mean().reset_index()
    
    fig = px.bar(
        avg_cycle_time,
        x='assignee',
        y='cycle_time_days',
        title="Average Cycle Time by Person",
        labels={'cycle_time_days': 'Average Cycle Time (Days)', 'assignee': 'Team Member'}
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def create_workload_distribution_chart(df):
    """Create workload distribution chart"""
    if 'assignee' not in df.columns:
        st.warning("No assignee data for workload analysis")
        return
    
    workload_data = df['assignee'].value_counts().reset_index()
    workload_data.columns = ['assignee', 'assigned_issues']
    
    fig = px.pie(
        workload_data,
        values='assigned_issues',
        names='assignee',
        title="Workload Distribution (Total Assigned Issues)"
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def create_performance_table(df):
    """Create detailed performance table"""
    if 'assignee' not in df.columns:
        st.warning("No assignee data for performance table")
        return
    
    # Calculate performance metrics per person
    performance_metrics = []
    
    for person in df['assignee'].unique():
        person_data = df[df['assignee'] == person]
        
        metrics = {
            'Team Member': person,
            'Total Assigned': len(person_data),
            'Completed': len(person_data[person_data['status'] == 'Done']),
            'In Progress': len(person_data[person_data['status'] == 'In Progress']),
            'Completion Rate': f"{(len(person_data[person_data['status'] == 'Done']) / len(person_data) * 100):.1f}%"
        }
        
        if 'estimate' in df.columns:
            metrics['Total Points'] = person_data['estimate'].sum()
            metrics['Completed Points'] = person_data[person_data['status'] == 'Done']['estimate'].sum()
        
        if 'cycle_time_days' in df.columns:
            avg_cycle = person_data['cycle_time_days'].mean()
            metrics['Avg Cycle Time'] = f"{avg_cycle:.1f} days" if not pd.isna(avg_cycle) else "N/A"
        
        performance_metrics.append(metrics)
    
    performance_df = pd.DataFrame(performance_metrics)
    
    # Style the dataframe
    st.dataframe(
        performance_df,
        use_container_width=True,
        hide_index=True
    )

def create_individual_deep_dive(df, person_name):
    """Create individual performance deep dive"""
    person_data = df[df['assignee'] == person_name]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📈 Work Distribution by Status**")
        status_dist = person_data['status'].value_counts()
        fig = px.pie(values=status_dist.values, names=status_dist.index)
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("**📊 Work Distribution by Type**")
        if 'type' in person_data.columns:
            type_dist = person_data['type'].value_counts()
            fig = px.pie(values=type_dist.values, names=type_dist.index)
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No type information available")
    
    # Recent work timeline
    st.write("**📅 Recent Work Timeline**")
    if 'completedat' in person_data.columns:
        completed_items = person_data[person_data['status'] == 'Done'].copy()
        if not completed_items.empty:
            completed_items = completed_items.sort_values('completedat', ascending=False).head(10)
            
            timeline_data = completed_items[['title', 'completedat', 'estimate']].copy()
            timeline_data['completedat'] = timeline_data['completedat'].dt.strftime('%Y-%m-%d')
            
            st.dataframe(
                timeline_data,
                column_config={
                    'title': 'Task Title',
                    'completedat': 'Completed Date',
                    'estimate': 'Story Points'
                },
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No completed items found")
    else:
        st.info("No completion date information available")

if __name__ == "__main__":
    main() 