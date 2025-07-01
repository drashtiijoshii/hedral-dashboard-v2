"""
OKR (Objectives and Key Results) Dashboard
Shows progress bars, color-coded status, and filtering by objective or owner
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from connect_google_sheet import GoogleSheetConnector, get_sample_okr_data

def main():
    st.set_page_config(
        page_title="🎯 OKR Dashboard",
        page_icon="🎯",
        layout="wide"
    )
    
    st.title("🎯 OKR (Objectives & Key Results) Dashboard")
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
        df = get_sample_okr_data()
        st.info("Using sample OKR data for demonstration")
    else:
        if 'connector' in st.session_state:
            df = st.session_state.connector.load_okr_data()
            if df is None or df.empty:
                st.error("Failed to load OKR data from Google Sheet")
                return
        else:
            st.warning("Please connect to a Google Sheet first")
            return
    
    if df.empty:
        st.error("No OKR data available to display")
        return
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        available_objectives = ['All'] + sorted(list(df['objective'].unique())) if 'objective' in df.columns else ['All']
        selected_objective = st.selectbox("Select Objective:", available_objectives)
    
    with col2:
        available_owners = ['All'] + sorted(list(df['owner'].unique())) if 'owner' in df.columns else ['All']
        selected_owner = st.selectbox("Select Owner:", available_owners)
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_objective != 'All':
        filtered_df = filtered_df[filtered_df['objective'] == selected_objective]
    
    if selected_owner != 'All':
        filtered_df = filtered_df[filtered_df['owner'] == selected_owner]
    
    if filtered_df.empty:
        st.warning("No data available for selected filters")
        return
    
    # Overview metrics
    st.subheader("📊 OKR Overview")
    
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
    st.subheader("📈 Key Results Progress")
    create_progress_visualization(filtered_df)
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Status Distribution")
        create_status_distribution_chart(filtered_df)
        
        st.subheader("👥 Progress by Owner")
        create_progress_by_owner_chart(filtered_df)
    
    with col2:
        st.subheader("🎯 Progress by Objective")
        create_progress_by_objective_chart(filtered_df)
        
        st.subheader("📉 Overall Progress Gauge")
        create_overall_progress_gauge(filtered_df)
    
    # Detailed OKR table
    st.markdown("---")
    st.subheader("📋 Detailed OKR Table")
    create_detailed_okr_table(filtered_df)
    
    # Action items section
    st.markdown("---")
    st.subheader("🚀 Action Items & Notes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_area(
            "At Risk Items - Action Plan 📝",
            placeholder="Enter action plans for at-risk OKRs...",
            height=120,
            key="at_risk_actions"
        )
    
    with col2:
        st.text_area(
            "Next Quarter Planning 🗓️",
            placeholder="Enter notes for next quarter OKR planning...",
            height=120,
            key="next_quarter_notes"
        )
    
    if st.button("💾 Save OKR Notes"):
        save_okr_notes()

def create_progress_visualization(df):
    """Create progress bars for each key result"""
    for idx, row in df.iterrows():
        # Status color mapping
        status_colors = {
            'On Track': '#28a745',    # Green
            'At Risk': '#ffc107',     # Yellow  
            'Behind': '#dc3545'       # Red
        }
        
        color = status_colors.get(row['status'], '#6c757d')
        progress = row.get('progress', 0)
        
        # Create columns for layout
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.write(f"**{row['key_result']}**")
            st.write(f"*{row['objective']} - {row['owner']}*")
        
        with col2:
            st.metric("Progress", f"{progress:.1f}%")
        
        with col3:
            st.markdown(f"<span style='color: {color}; font-weight: bold;'>{row['status']}</span>", 
                       unsafe_allow_html=True)
        
        # Progress bar
        st.progress(min(progress / 100, 1.0))
        st.markdown("---")

def create_status_distribution_chart(df):
    """Create status distribution pie chart"""
    status_counts = df['status'].value_counts()
    
    colors = ['#28a745', '#ffc107', '#dc3545', '#6c757d']
    
    fig = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="OKR Status Distribution",
        color_discrete_sequence=colors
    )
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

def create_progress_by_owner_chart(df):
    """Create average progress by owner chart"""
    if 'owner' not in df.columns or 'progress' not in df.columns:
        st.warning("Missing data for progress by owner")
        return
    
    progress_by_owner = df.groupby('owner')['progress'].mean().reset_index()
    
    fig = px.bar(
        progress_by_owner,
        x='owner',
        y='progress',
        title="Average Progress by Owner",
        labels={'progress': 'Average Progress (%)', 'owner': 'Owner'},
        color='progress',
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

def create_progress_by_objective_chart(df):
    """Create progress by objective chart"""
    if 'objective' not in df.columns or 'progress' not in df.columns:
        st.warning("Missing data for progress by objective")
        return
    
    progress_by_objective = df.groupby('objective')['progress'].mean().reset_index()
    
    fig = px.bar(
        progress_by_objective,
        x='objective',
        y='progress',
        title="Average Progress by Objective",
        labels={'progress': 'Average Progress (%)', 'objective': 'Objective'},
        color='progress',
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_xaxes(tickangle=45)
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

def create_overall_progress_gauge(df):
    """Create overall progress gauge"""
    if 'progress' not in df.columns:
        st.warning("No progress data available")
        return
    
    overall_progress = df['progress'].mean()
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = overall_progress,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Overall OKR Progress"},
        delta = {'reference': 75},  # Target reference
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
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

def create_detailed_okr_table(df):
    """Create detailed OKR table with styling"""
    
    # Function to color-code status
    def color_status(status):
        if status == 'On Track':
            return 'background-color: #d4edda; color: #155724'
        elif status == 'At Risk':
            return 'background-color: #fff3cd; color: #856404'
        elif status == 'Behind':
            return 'background-color: #f8d7da; color: #721c24'
        else:
            return ''
    
    # Prepare display dataframe
    display_df = df.copy()
    
    # Format progress column
    if 'progress' in display_df.columns:
        display_df['progress'] = display_df['progress'].round(1).astype(str) + '%'
    
    # Reorder columns for better display
    column_order = ['objective', 'key_result', 'owner', 'target', 'current', 'progress', 'status']
    available_columns = [col for col in column_order if col in display_df.columns]
    display_df = display_df[available_columns]
    
    # Rename columns for better display
    column_names = {
        'objective': 'Objective',
        'key_result': 'Key Result',
        'owner': 'Owner',
        'target': 'Target',
        'current': 'Current',
        'progress': 'Progress',
        'status': 'Status'
    }
    
    display_df = display_df.rename(columns=column_names)
    
    # Display the styled dataframe
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

def save_okr_notes():
    """Save OKR notes (placeholder function)"""
    from datetime import datetime
    
    notes = {
        'at_risk_actions': st.session_state.get('at_risk_actions', ''),
        'next_quarter_notes': st.session_state.get('next_quarter_notes', ''),
        'timestamp': datetime.now().isoformat()
    }
    
    # In a real implementation, you would save this to a database or file
    st.success("📝 OKR notes saved successfully!")
    st.json(notes)

if __name__ == "__main__":
    main() 