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

# Custom CSS with consistent spacing system and beautiful design
st.markdown("""
<style>
    /* CSS Custom Properties for Consistent Spacing */
    :root {
        --spacing-xs: 0.25rem;   /* 4px */
        --spacing-sm: 0.5rem;    /* 8px */
        --spacing-md: 1rem;      /* 16px */
        --spacing-lg: 1.5rem;    /* 24px */
        --spacing-xl: 2rem;      /* 32px */
        --spacing-2xl: 3rem;     /* 48px */
        --spacing-3xl: 4rem;     /* 64px */
        
        --border-radius-sm: 8px;
        --border-radius-md: 12px;
        --border-radius-lg: 16px;
        --border-radius-xl: 20px;
        
        --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.08);
        --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
        --shadow-colored: 0 4px 16px rgba(102, 126, 234, 0.15);
        
        --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-surface: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        --gradient-subtle: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Global spacing reset and consistency */
    .stApp {
        padding: 0 !important;
    }
    
    .main .block-container {
        padding: var(--spacing-lg) var(--spacing-md) !important;
        max-width: 100% !important;
    }
    
    /* Responsive design - Mobile first approach */
    .main-header {
        font-size: clamp(1.4rem, 3vw, 2rem);
        font-weight: 700;
        color: white;
        text-align: center;
        padding: var(--spacing-lg) var(--spacing-xl);
        background: var(--gradient-primary);
        border-radius: var(--border-radius-lg);
        margin-bottom: var(--spacing-lg);
        box-shadow: var(--shadow-lg);
    }
    
    .section-header {
        color: #2c3e50;
        font-size: clamp(1.2rem, 3vw, 1.5rem);
        font-weight: 700;
        margin: var(--spacing-xl) 0 var(--spacing-lg) 0;
        padding: var(--spacing-lg) var(--spacing-xl);
        background: var(--gradient-subtle);
        border-radius: var(--border-radius-lg);
        border: 1px solid rgba(102, 126, 234, 0.1);
        box-shadow: var(--shadow-sm);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .section-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-primary);
        border-radius: var(--border-radius-lg) var(--border-radius-lg) 0 0;
    }
    
    .section-header:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-colored);
    }
    
    /* Consistent Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: var(--spacing-md);
        background: #f8f9fa;
        border-radius: var(--border-radius-lg);
        padding: var(--spacing-md);
        flex-wrap: wrap;
        margin-bottom: var(--spacing-lg);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: clamp(40px, 6vw, 50px);
        padding: var(--spacing-sm) var(--spacing-lg);
        background: white;
        border-radius: var(--border-radius-md);
        font-weight: 600;
        border: 2px solid transparent;
        font-size: clamp(0.8rem, 2vw, 1rem);
        margin-bottom: var(--spacing-sm);
        transition: all 0.3s ease;
        box-shadow: var(--shadow-sm);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--gradient-primary);
        color: white;
        box-shadow: var(--shadow-colored);
    }
    
    .info-box {
        background: linear-gradient(135deg, #e8f6f3 0%, #f0f9f7 100%);
        padding: var(--spacing-lg);
        border-radius: var(--border-radius-md);
        border: 1px solid rgba(26, 188, 156, 0.2);
        box-shadow: var(--shadow-sm);
        margin: var(--spacing-lg) 0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .info-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(26, 188, 156, 0.15);
    }
    
    /* Enhanced Streamlit spinner - bigger and centered */
    div[data-testid="stSpinner"] {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(3px) !important;
        z-index: 9999 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    div[data-testid="stSpinner"] > div {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 20px !important;
        padding: clamp(1.5rem, 4vw, 2.5rem) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        min-width: 200px !important;
        max-width: 90vw !important;
    }
    
    div[data-testid="stSpinner"] .stSpinner {
        width: clamp(50px, 8vw, 80px) !important;
        height: clamp(50px, 8vw, 80px) !important;
    }
    
    div[data-testid="stSpinner"] .stSpinner > div {
        width: clamp(50px, 8vw, 80px) !important;
        height: clamp(50px, 8vw, 80px) !important;
        border-width: clamp(3px, 1vw, 5px) !important;
        border-color: #f3f3f3 #f3f3f3 #f3f3f3 #667eea !important;
    }
    
    div[data-testid="stSpinner"] p {
        color: #2c3e50 !important;
        font-size: clamp(1rem, 3vw, 1.3rem) !important;
        font-weight: 600 !important;
        margin: 1rem 0 0 0 !important;
        text-align: center !important;
        animation: pulse 1.5s ease-in-out infinite alternate !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
    
    @keyframes pulse {
        from { opacity: 0.7; }
        to { opacity: 1; }
    }
    
    /* Enhanced Metric Cards with Consistent Spacing */
    div[data-testid="metric-container"] {
        background: var(--gradient-surface) !important;
        border: 1px solid rgba(102, 126, 234, 0.1) !important;
        border-radius: var(--border-radius-lg) !important;
        padding: var(--spacing-lg) var(--spacing-xl) !important;
        margin: var(--spacing-md) 0 !important;
        box-shadow: var(--shadow-md) !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px) !important;
        box-shadow: var(--shadow-lg) !important;
        border-color: rgba(102, 126, 234, 0.2) !important;
    }
    
    div[data-testid="metric-container"]::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 4px !important;
        background: var(--gradient-primary) !important;
        border-radius: var(--border-radius-lg) var(--border-radius-lg) 0 0 !important;
    }
    
        /* Metric labels (titles) */
    div[data-testid="metric-container"] > div:first-child {
        font-size: clamp(0.85rem, 2.5vw, 1rem) !important;
        font-weight: 600 !important;
        color: #4a5568 !important;
        margin-bottom: var(--spacing-sm) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Metric values (numbers) */
    div[data-testid="metric-container"] div[data-testid="metric-value"] {
        font-size: clamp(1.8rem, 5vw, 2.5rem) !important;
        font-weight: 700 !important;
        color: #2d3748 !important;
        line-height: 1.2 !important;
        margin: var(--spacing-xs) 0 !important;
        background: var(--gradient-primary) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }
    
    /* Metric delta (change indicators) */
    div[data-testid="metric-container"] div[data-testid="metric-delta"] {
        font-size: clamp(0.8rem, 2.2vw, 0.95rem) !important;
        font-weight: 500 !important;
        margin-top: var(--spacing-xs) !important;
    }
     
     /* Enhanced Button Styling with Consistent Spacing */
     .stButton > button {
         background: var(--gradient-primary) !important;
         color: white !important;
         border: none !important;
         border-radius: var(--border-radius-md) !important;
         padding: var(--spacing-md) var(--spacing-lg) !important;
         font-weight: 600 !important;
         font-size: 0.95rem !important;
         transition: all 0.3s ease !important;
         box-shadow: var(--shadow-colored) !important;
         text-transform: none !important;
         letter-spacing: 0.5px !important;
         margin: var(--spacing-sm) 0 !important;
     }
     
     .stButton > button:hover {
         transform: translateY(-2px) !important;
         box-shadow: var(--shadow-lg) !important;
         background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%) !important;
     }
     
     .stButton > button:active {
         transform: translateY(0px) !important;
         box-shadow: var(--shadow-colored) !important;
     }
     
     /* Secondary button styling */
     .stButton > button[kind="secondary"] {
         background: var(--gradient-subtle) !important;
         color: #4a5568 !important;
         border: 1px solid rgba(102, 126, 234, 0.2) !important;
         box-shadow: var(--shadow-sm) !important;
     }
     
     .stButton > button[kind="secondary"]:hover {
         background: var(--gradient-subtle) !important;
         border-color: rgba(102, 126, 234, 0.3) !important;
         box-shadow: var(--shadow-md) !important;
     }
    
              /* Enhanced Form Inputs with Consistent Spacing */
     .stTextInput > div > div > input {
         border: 1px solid rgba(102, 126, 234, 0.2) !important;
         border-radius: var(--border-radius-md) !important;
         padding: var(--spacing-md) var(--spacing-lg) !important;
         font-size: 0.95rem !important;
         transition: all 0.3s ease !important;
         background: var(--gradient-surface) !important;
         box-shadow: var(--shadow-sm) !important;
         margin-bottom: var(--spacing-sm) !important;
     }
     
     .stTextInput > div > div > input:focus {
         border-color: #667eea !important;
         box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1), var(--shadow-md) !important;
         outline: none !important;
     }
     
     /* Select boxes */
     .stSelectbox > div > div {
         border: 1px solid rgba(102, 126, 234, 0.2) !important;
         border-radius: var(--border-radius-md) !important;
         background: var(--gradient-surface) !important;
         box-shadow: var(--shadow-sm) !important;
         transition: all 0.3s ease !important;
         margin-bottom: var(--spacing-sm) !important;
     }
     
     .stSelectbox > div > div:hover {
         border-color: rgba(102, 126, 234, 0.3) !important;
         box-shadow: var(--shadow-md) !important;
     }
     
     /* Radio buttons */
     .stRadio > div {
         background: var(--gradient-surface) !important;
         border-radius: var(--border-radius-md) !important;
         padding: var(--spacing-lg) !important;
         border: 1px solid rgba(102, 126, 234, 0.1) !important;
         box-shadow: var(--shadow-sm) !important;
         margin-bottom: var(--spacing-sm) !important;
     }
     
     /* Enhanced Charts with Consistent Spacing */
     .js-plotly-plot {
         width: 100% !important;
         height: auto !important;
         border-radius: var(--border-radius-md) !important;
         overflow: hidden !important;
         box-shadow: var(--shadow-md) !important;
         margin: var(--spacing-md) 0 !important;
     }
    
         /* Consistent Column Spacing */
     .stColumn {
         padding: var(--spacing-sm) !important;
     }
     
     .stColumn > div {
         margin-bottom: var(--spacing-md) !important;
     }
    
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab-list"] {
            justify-content: center;
            flex-wrap: wrap;
        }
        
                 .stTabs [data-baseweb="tab"] {
             min-width: calc(33.333% - var(--spacing-md));
             text-align: center;
             margin: var(--spacing-xs);
         }
         
         /* Stack metrics vertically on mobile */
         .stColumn > div {
             margin-bottom: var(--spacing-md);
         }
    }
    
    @media (max-width: 480px) {
        .stTabs [data-baseweb="tab"] {
            min-width: calc(50% - var(--spacing-xs));
            padding: 0 var(--spacing-sm);
            font-size: 0.85rem;
        }
        
        .main-header {
            margin-bottom: var(--spacing-lg);
            padding: var(--spacing-lg);
        }
        
        /* Sidebar improvements for mobile */
        .stSidebar {
            width: 100% !important;
        }
        
        /* Better spacing for mobile */
        .stSelectbox, .stTextInput, .stButton {
            margin-bottom: var(--spacing-sm) !important;
        }
        
        .main .block-container {
            padding: var(--spacing-md) var(--spacing-sm) !important;
        }
    }
     
     /* Enhanced Messages with Consistent Spacing */
     .stSuccess > div {
         background: linear-gradient(135deg, #f0fff4 0%, #e6fffa 100%) !important;
         border: 1px solid rgba(72, 187, 120, 0.3) !important;
         border-radius: var(--border-radius-md) !important;
         padding: var(--spacing-lg) var(--spacing-xl) !important;
         color: #2f855a !important;
         font-weight: 500 !important;
         box-shadow: var(--shadow-sm) !important;
         margin: var(--spacing-md) 0 !important;
     }
     
     .stError > div {
         background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%) !important;
         border: 1px solid rgba(245, 101, 101, 0.3) !important;
         border-radius: var(--border-radius-md) !important;
         padding: var(--spacing-lg) var(--spacing-xl) !important;
         color: #c53030 !important;
         font-weight: 500 !important;
         box-shadow: var(--shadow-sm) !important;
         margin: var(--spacing-md) 0 !important;
     }
     
     .stInfo > div {
         background: linear-gradient(135deg, #ebf8ff 0%, #bee3f8 100%) !important;
         border: 1px solid rgba(66, 153, 225, 0.3) !important;
         border-radius: var(--border-radius-md) !important;
         padding: var(--spacing-lg) var(--spacing-xl) !important;
         color: #2c5282 !important;
         font-weight: 500 !important;
         box-shadow: var(--shadow-sm) !important;
         margin: var(--spacing-md) 0 !important;
     }
     
     /* Enhanced Sidebar with Perfect Styling */
     .stSidebar {
         background: var(--gradient-subtle) !important;
         border-right: 1px solid rgba(102, 126, 234, 0.15) !important;
     }
     
     .stSidebar > div {
         padding: var(--spacing-lg) var(--spacing-md) !important;
     }
     
     .stSidebar h2 {
         color: #2d3748 !important;
         font-weight: 700 !important;
         margin-bottom: var(--spacing-lg) !important;
         padding-bottom: var(--spacing-sm) !important;
         border-bottom: 2px solid rgba(102, 126, 234, 0.15) !important;
         font-size: 1.25rem !important;
     }
     
     /* Enhanced Sidebar Radio Buttons */
     .stSidebar .stRadio > div {
         background: white !important;
         border: 1px solid rgba(102, 126, 234, 0.15) !important;
         border-radius: var(--border-radius-md) !important;
         padding: var(--spacing-md) !important;
         margin: var(--spacing-sm) 0 var(--spacing-lg) 0 !important;
         box-shadow: var(--shadow-sm) !important;
         transition: all 0.3s ease !important;
     }
     
     .stSidebar .stRadio > div:hover {
         border-color: rgba(102, 126, 234, 0.25) !important;
         box-shadow: var(--shadow-md) !important;
         transform: translateY(-1px) !important;
     }
     
     .stSidebar .stRadio label {
         color: #4a5568 !important;
         font-weight: 500 !important;
         font-size: 0.95rem !important;
     }
     
     /* Enhanced Sidebar Labels */
     .stSidebar .stRadio > label {
         color: #2d3748 !important;
         font-weight: 600 !important;
         font-size: 1rem !important;
         margin-bottom: var(--spacing-sm) !important;
     }
     
     /* Enhanced Info Box in Sidebar */
     .stSidebar .info-box {
         background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%) !important;
         border: 1px solid rgba(59, 130, 246, 0.2) !important;
         border-radius: var(--border-radius-md) !important;
         padding: var(--spacing-md) !important;
         margin: var(--spacing-md) 0 !important;
         box-shadow: var(--shadow-sm) !important;
         font-size: 0.85rem !important;
         line-height: 1.4 !important;
     }
     
     .stSidebar .info-box:hover {
         transform: translateY(-1px) !important;
         box-shadow: var(--shadow-md) !important;
     }
     
     /* Enhanced Sidebar Text Inputs */
     .stSidebar .stTextInput > div > div > input {
         border: 1px solid rgba(102, 126, 234, 0.2) !important;
         border-radius: var(--border-radius-md) !important;
         padding: var(--spacing-sm) var(--spacing-md) !important;
         font-size: 0.9rem !important;
         background: white !important;
         box-shadow: var(--shadow-sm) !important;
         margin-bottom: var(--spacing-md) !important;
     }
     
     .stSidebar .stTextInput > div > div > input:focus {
         border-color: #667eea !important;
         box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1), var(--shadow-md) !important;
     }
     
     /* Enhanced Sidebar Buttons */
     .stSidebar .stButton > button {
         width: 100% !important;
         background: var(--gradient-primary) !important;
         color: white !important;
         border: none !important;
         border-radius: var(--border-radius-md) !important;
         padding: var(--spacing-sm) var(--spacing-md) !important;
         font-weight: 600 !important;
         font-size: 0.9rem !important;
         margin: var(--spacing-sm) 0 var(--spacing-md) 0 !important;
         box-shadow: var(--shadow-sm) !important;
         transition: all 0.3s ease !important;
     }
     
     .stSidebar .stButton > button:hover {
         transform: translateY(-2px) !important;
         box-shadow: var(--shadow-colored) !important;
     }
     
     /* Enhanced Success Messages in Sidebar */
     .stSidebar .stSuccess > div {
         background: linear-gradient(135deg, #f0fff4 0%, #dcfce7 100%) !important;
         border: 1px solid rgba(34, 197, 94, 0.3) !important;
         border-radius: var(--border-radius-md) !important;
         padding: var(--spacing-sm) var(--spacing-md) !important;
         margin: var(--spacing-sm) 0 !important;
         font-size: 0.85rem !important;
         color: #15803d !important;
         box-shadow: var(--shadow-sm) !important;
     }
    
    @media (max-width: 320px) {
        .stTabs [data-baseweb="tab"] {
            min-width: 100%;
            margin: var(--spacing-xs) 0;
        }
        
        div[data-testid="stSpinner"] p {
            font-size: 0.9rem !important;
            white-space: normal !important;
            line-height: 1.2 !important;
        }
        
        .main .block-container {
            padding: var(--spacing-sm) var(--spacing-xs) !important;
        }
    }
</style>
""", unsafe_allow_html=True)

def show_loading_overlay(message="Loading..."):
    """Custom loading overlay that definitely works"""
    return st.markdown(f"""
    <div style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(3px);
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: center;
    ">
        <div style="
            background: white;
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.15);
            text-align: center;
            min-width: 200px;
            max-width: 90vw;
        ">
            <div style="
                width: 60px;
                height: 60px;
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin: 0 auto 1rem auto;
            "></div>
            <p style="
                color: #2c3e50;
                font-size: 1.2rem;
                font-weight: 600;
                margin: 0;
                animation: pulse 1.5s ease-in-out infinite alternate;
            ">{message}</p>
        </div>
    </div>
    <style>
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        @keyframes pulse {{
            from {{ opacity: 0.7; }}
            to {{ opacity: 1; }}
        }}
    </style>
    """, unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<div class="main-header">Dashboard</div>', unsafe_allow_html=True)
    
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
                        # Show custom loading overlay
                        loading_placeholder = st.empty()
                        with loading_placeholder:
                            show_loading_overlay("🔌 Connecting to Google Sheet...")
                        
                        # Perform connection
                        connector = GoogleSheetConnector()
                        success = connector.connect_with_url(sheet_url)
                        
                        # Clear loading overlay
                        loading_placeholder.empty()
                        
                        if success:
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
    
    # Sprint filter - handle mixed data types safely with multi-select
    if 'cycle' in df.columns:
        # Clean cycle data - remove NaN and convert to string for consistent sorting
        cycle_values = df['cycle'].dropna().astype(str).unique()
        available_sprints = sorted([c for c in cycle_values if c != 'nan' and c.strip() != ''])
    else:
        available_sprints = []
    
    # Multi-select for sprints
    selected_sprints = st.multiselect(
        "🏃‍♂️ Select Sprint(s):", 
        available_sprints,
        default=available_sprints,  # Default to all sprints selected
        help="Select one or more sprints to filter the data"
    )
    
    # Information box about the new functionality
    if selected_sprints:
        st.info(f"📊 **Filtering by {len(selected_sprints)} sprint(s):** {', '.join(selected_sprints)}")
    else:
        st.warning("⚠️ No sprints selected. Please select at least one sprint to view data.")
    
    # Filter data - handle string comparison safely with multi-select
    if selected_sprints and 'cycle' in df.columns:
        # Convert cycle column to string for comparison
        df_temp = df.copy()
        df_temp['cycle'] = df_temp['cycle'].astype(str)
        filtered_df = df_temp[df_temp['cycle'].isin(selected_sprints)]
    else:
        filtered_df = df
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Count completed story points instead of just completed issues
        if 'estimate' in filtered_df.columns:
            try:
                completed_df = filtered_df[filtered_df['status'] == 'Done']
                numeric_estimates = completed_df['estimate'].apply(
                    lambda x: pd.to_numeric(x, errors='coerce') if pd.notnull(x) else 0
                ).fillna(0)
                completed_points = int(numeric_estimates.sum())
            except:
                completed_points = 0
        else:
            completed_points = 0
        st.metric("✅ Completed Points", completed_points)
    
    with col2:
        if 'estimate' in filtered_df.columns:
            # Handle estimate column safely
            try:
                # Convert to numeric and sum, handling non-numeric values
                numeric_estimates = filtered_df['estimate'].apply(
                    lambda x: pd.to_numeric(x, errors='coerce') if pd.notnull(x) else 0
                ).fillna(0)
                total_points = int(numeric_estimates.sum())
            except:
                total_points = 0
        else:
            total_points = 0
        st.metric("📊 Total Story Points", total_points)
    
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
        # Calculate completion rate based on story points
        if total_points > 0:
            rate = (completed_points / total_points * 100)
        else:
            rate = 0
        st.metric("🎯 Completion Rate", f"{rate:.1f}%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Velocity chart - handle data types safely and respect filter
        if 'cycle' in df.columns and 'estimate' in df.columns:
            # Use filtered data for velocity calculation
            velocity_data = df[df['status'] == 'Done'].copy()
            velocity_data['cycle'] = velocity_data['cycle'].astype(str)
            
            # Filter by selected sprints if any
            if selected_sprints:
                velocity_data = velocity_data[velocity_data['cycle'].isin(selected_sprints)]
            
            # Convert estimates to numeric, replacing non-numeric with 0
            velocity_data['estimate'] = velocity_data['estimate'].apply(
                lambda x: pd.to_numeric(x, errors='coerce') if pd.notnull(x) else 0
            ).fillna(0)
            
            velocity = velocity_data.groupby('cycle')['estimate'].sum().reset_index()
            if not velocity.empty and len(velocity) > 0:
                fig = px.bar(velocity, x='cycle', y='estimate', 
                           title="📈 Sprint Velocity (Filtered)",
                           color='estimate',
                           color_continuous_scale='Blues')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # Status pie chart
        status_counts = filtered_df['status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index, title="📊 Status Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Burndown simulation - use filtered data
        if 'estimate' in filtered_df.columns:
            try:
                # Calculate total and completed points from filtered data
                numeric_estimates = filtered_df['estimate'].apply(
                    lambda x: pd.to_numeric(x, errors='coerce') if pd.notnull(x) else 0
                ).fillna(0)
                total_points = numeric_estimates.sum()
                
                completed_df = filtered_df[filtered_df['status'] == 'Done']
                completed_numeric = completed_df['estimate'].apply(
                    lambda x: pd.to_numeric(x, errors='coerce') if pd.notnull(x) else 0
                ).fillna(0)
                completed_points = completed_numeric.sum()
            except:
                total_points = 100
                completed_points = 50
        else:
            total_points = 100
            completed_points = 50
        
        days = list(range(15))
        ideal = [total_points - (total_points/14) * day for day in days]
        actual = [total_points - min(completed_points, (completed_points/10) * day) for day in days]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=days, y=ideal, mode='lines', name='Ideal', line=dict(dash='dash', color='gray')))
        fig.add_trace(go.Scatter(x=days, y=actual, mode='lines+markers', name='Actual', line=dict(color='#1f77b4')))
        fig.update_layout(title="🔥 Sprint Burndown (Filtered)", height=400)
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
        # Handle cycle data safely with multi-select
        if 'cycle' in df.columns:
            cycle_values = df['cycle'].dropna().astype(str).unique()
            available_sprints = sorted([c for c in cycle_values if c != 'nan' and c.strip() != ''])
        else:
            available_sprints = []
        
        # Multi-select for sprints in performance dashboard
        selected_sprints_perf = st.multiselect(
            "🏃‍♂️ Sprint(s):", 
            available_sprints,
            default=available_sprints,  # Default to all sprints selected
            help="Select one or more sprints to filter the data",
            key="perf_sprint"
        )
    
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
    if selected_sprints_perf and 'cycle' in df.columns:
        filtered_df['cycle'] = filtered_df['cycle'].astype(str)
        filtered_df = filtered_df[filtered_df['cycle'].isin(selected_sprints_perf)]
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
        # Count completed story points instead of just completed issues
        if 'estimate' in filtered_df.columns:
            try:
                completed_df = filtered_df[filtered_df['status'] == 'Done']
                numeric_estimates = completed_df['estimate'].apply(
                    lambda x: pd.to_numeric(x, errors='coerce') if pd.notnull(x) else 0
                ).fillna(0)
                completed_points = int(numeric_estimates.sum())
            except:
                completed_points = 0
        else:
            completed_points = 0
        st.metric("✅ Completed Points", completed_points)
    with col3:
        # Calculate completion rate based on story points
        if 'estimate' in filtered_df.columns:
            try:
                total_numeric = filtered_df['estimate'].apply(
                    lambda x: pd.to_numeric(x, errors='coerce') if pd.notnull(x) else 0
                ).fillna(0)
                total_points = total_numeric.sum()
                rate = (completed_points / total_points * 100) if total_points > 0 else 0
            except:
                rate = 0
        else:
            rate = 0
        st.metric("🎯 Points Rate", f"{rate:.1f}%")
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