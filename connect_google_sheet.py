"""
Google Sheets Connection Module
Connects to Linear-exported Google Sheets data and loads as DataFrame
"""

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
from typing import Optional
import json
import requests
from io import StringIO

class GoogleSheetConnector:
    def __init__(self):
        self.gc = None
        self.sheet = None
        
    def connect_with_url(self, sheet_url: str) -> bool:
        """
        Connect to Google Sheet using public URL (read-only)
        For Linear exports that are made public
        """
        try:
            # Extract sheet ID from URL
            if "/spreadsheets/d/" in sheet_url:
                sheet_id = sheet_url.split("/spreadsheets/d/")[1].split("/")[0]
                
                # Try public access first (no credentials needed)
                try:
                    import requests
                    import pandas as pd
                    
                    # Extract gid (sheet tab) from URL if present
                    gid = "0"  # default
                    if "gid=" in sheet_url:
                        gid = sheet_url.split("gid=")[1].split("&")[0].split("#")[0]
                    
                    # Try multiple gids to find the Linear data
                    gids_to_try = [gid, "0", "1413191165", "2", "1"]
                    
                    for try_gid in gids_to_try:
                        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={try_gid}"
                        
                        # Test if sheet is publicly accessible
                        response = requests.get(csv_url, timeout=10)
                        if response.status_code == 200:
                            # Check if we got Linear data (should have ID column)
                            lines = response.text.strip().split('\n')
                            if len(lines) > 1 and 'ID' in lines[0]:
                                # Successfully accessed public sheet with Linear data
                                self.sheet_id = sheet_id
                                self.csv_url = csv_url
                                st.success(f"✅ Found Linear data on sheet tab gid={try_gid}")
                                return True
                    
                    st.error("Could not find Linear data on any sheet tab. Make sure your Linear export is public.")
                    return False
                        
                except Exception as e:
                    st.error(f"Cannot access sheet publicly. Error: {str(e)}")
                    return False
                    
            else:
                st.error("Invalid Google Sheets URL format")
                return False
                
        except Exception as e:
            st.error(f"Failed to connect to Google Sheet: {str(e)}")
            return False
    
    def connect_with_credentials(self, credentials_json: dict, sheet_url: str) -> bool:
        """
        Connect using service account credentials
        """
        try:
            scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
            
            creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_json, scope)
            self.gc = gspread.authorize(creds)
            
            # Extract sheet ID from URL
            sheet_id = sheet_url.split("/spreadsheets/d/")[1].split("/")[0]
            self.sheet = self.gc.open_by_key(sheet_id)
            return True
            
        except Exception as e:
            st.error(f"Failed to connect with credentials: {str(e)}")
            return False
    
    def load_issues_data(self, worksheet_name: str = "Sheet1") -> Optional[pd.DataFrame]:
        """
        Load Linear issues data from the specified worksheet
        """
        try:
            # If using CSV URL (public access)
            if hasattr(self, 'csv_url'):
                import requests
                
                st.info(f"🔗 **Fetching data from:** {self.csv_url}")
                response = requests.get(self.csv_url)
                if response.status_code == 200:
                    from io import StringIO
                    df = pd.read_csv(StringIO(response.text))
                else:
                    st.error("Failed to fetch data from public sheet")
                    return None
            
            # If using gspread (service account)
            elif hasattr(self, 'sheet') and self.sheet:
                worksheet = self.sheet.worksheet(worksheet_name)
                data = worksheet.get_all_records()
                
                if not data:
                    st.warning("No data found in the worksheet")
                    return pd.DataFrame()
                
                df = pd.DataFrame(data)
            
            else:
                # No connection established
                return None
            
            if df.empty:
                st.warning("No data found in the sheet")
                return pd.DataFrame()
            
            # Auto-detect and map Linear's column names to standard names
            df = self._map_linear_columns(df)
            
            # Convert date columns (try multiple formats)
            date_columns = ['createdat', 'completedat', 'updatedat', 'startedat']
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
            
            # Convert numeric columns
            numeric_columns = ['estimate', 'story_points', 'points']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Calculate cycle time if dates are available
            if 'completedat' in df.columns and 'startedat' in df.columns:
                df['cycle_time_days'] = (df['completedat'] - df['startedat']).dt.days
            elif 'completedat' in df.columns and 'createdat' in df.columns:
                df['cycle_time_days'] = (df['completedat'] - df['createdat']).dt.days
            
            return df
            
        except Exception as e:
            st.error(f"Failed to load data: {str(e)}")
            return None
    
    def _map_linear_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Map Linear's column names to standard dashboard column names
        """
        # Linear's EXACT column names from your export and their mappings
        column_mapping = {
            # Issue identification (exactly as in your sheet)
            'ID': 'id',
            'id': 'id',
            
            # Issue details
            'Title': 'title',
            'title': 'title',
            'Description': 'description',
            'description': 'description',
            
            # Status (exactly as in your sheet)
            'Status': 'status',
            'status': 'status',
            
            # Assignment (exactly as in your sheet)
            'Assignee': 'assignee',
            'assignee': 'assignee',
            'Creator': 'creator',
            'creator': 'creator',
            
            # Estimates (exactly as in your sheet)
            'Estimate': 'estimate',
            'estimate': 'estimate',
            
            # Team/Sprint (exactly as in your sheet)
            'Team': 'team',
            'team': 'team',
            'Cycle Name': 'cycle',
            'cycle name': 'cycle',
            'Cycle Number': 'cycle_number',
            'cycle number': 'cycle_number',
            
            # Dates (exactly as in your sheet)
            'Created': 'createdat',
            'created': 'createdat',
            'Updated': 'updatedat',
            'updated': 'updatedat',
            'Completed': 'completedat',
            'completed': 'completedat',
            'Started': 'startedat',
            'started': 'startedat',
            'Canceled': 'cancelledat',
            'canceled': 'cancelledat',
            
            # Priority (exactly as in your sheet)
            'Priority': 'priority',
            'priority': 'priority',
            
            # Project info
            'Project': 'project',
            'project': 'project',
            'Project ID': 'project_id',
            'project id': 'project_id',
            
            # Additional fields
            'Labels': 'labels',
            'labels': 'labels',
            'Cycle Start': 'cycle_start',
            'cycle start': 'cycle_start',
            'Cycle End': 'cycle_end',
            'cycle end': 'cycle_end',
        }
        
        # Show original columns for debugging
        st.info(f"📊 **Original columns found:** {', '.join(df.columns.tolist())}")
        
        # Apply mapping
        df_mapped = df.copy()
        for old_col, new_col in column_mapping.items():
            if old_col in df.columns:
                df_mapped[new_col] = df[old_col]
                st.success(f"✅ Mapped '{old_col}' → '{new_col}'")
        
        # Clean column names (remove dots, lowercase, etc.)
        for col in df.columns:
            clean_col = col.lower().replace('.', '_').replace(' ', '_').replace('-', '_')
            if clean_col not in df_mapped.columns and col not in column_mapping:
                df_mapped[clean_col] = df[col]
        
        return df_mapped
    
    def load_okr_data(self, worksheet_name: str = "OKRs") -> Optional[pd.DataFrame]:
        """
        Load OKR data from the specified worksheet
        """
        # For OKR data, we'll use sample data since Linear doesn't typically export OKRs
        # This method is mainly for service account connections
        if not self.sheet:
            return get_sample_okr_data()
            
        try:
            worksheet = self.sheet.worksheet(worksheet_name)
            data = worksheet.get_all_records()
            
            if not data:
                st.warning("No OKR data found in the worksheet")
                return pd.DataFrame()
            
            df = pd.DataFrame(data)
            
            # Clean column names
            df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')
            
            # Convert numeric columns
            numeric_columns = ['target', 'current', 'progress']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Calculate progress percentage if not present
            if 'target' in df.columns and 'current' in df.columns and 'progress' not in df.columns:
                df['progress'] = (df['current'] / df['target'] * 100).round(1)
            
            return df
            
        except Exception as e:
            st.error(f"Failed to load OKR data: {str(e)}")
            return None

def get_sample_data() -> pd.DataFrame:
    """
    Generate sample data matching EXACTLY your Linear export structure
    Based on your actual columns: ID, Team, Title, Description, Status, etc.
    """
    import random
    from datetime import datetime, timedelta
    
    # Sample data that matches your exact Linear structure
    assignees = ['omkar.shidore@hedral.co', 'genki.kadomatsu@hedral.co', 'shubham.thakare@hedral.co', 'drashti.joshi@hedral.co']
    statuses = ['Triage', 'In Progress', 'Done', 'Canceled']  # From your actual data
    priorities = ['Low', 'Medium', 'High', 'Urgent']  # From your actual data
    cycles = ['Cycle 3', 'Cycle 4', 'Cycle 6']  # From your actual data
    cycle_numbers = [3, 4, 6]
    projects = ['SWE Process/Onboarding Improvements', 'Development', 'API Integration']
    
    data = []
    
    for i in range(50):
        created_date = datetime.now() - timedelta(days=random.randint(1, 90))
        updated_date = created_date + timedelta(days=random.randint(0, 30))
        
        # Some issues are completed
        is_completed = random.choice([True, False])
        completed_date = created_date + timedelta(days=random.randint(1, 14)) if is_completed else None
        started_date = created_date + timedelta(days=random.randint(0, 3)) if is_completed or random.choice([True, False]) else None
        
        cycle_idx = random.randint(0, 2)
        cycle_name = cycles[cycle_idx]
        cycle_number = cycle_numbers[cycle_idx]
        
        # Create sample issue with EXACT Linear column structure
        issue = {
            # Exact columns from your Linear export
            'ID': f'SWE-{100 + i}',
            'Team': 'Software',
            'Title': f'{random.choice(["Explore APIs for", "Implement", "JSON Parser for", "Documentation for", "Fix bug in", "Enhance"])} {random.choice(["zoning data", "chatbot demo", "JAXSSO integration", "onboarding", "user interface", "performance"])}',
            'Description': f'As a user, I want to {random.choice(["see setbacks", "build demo", "convert JSON", "streamline process", "fix issues"])} so that {random.choice(["restrictions are visible", "demo is functional", "parser works", "onboarding is efficient", "bugs are resolved"])}.',
            'Status': 'Done' if is_completed else random.choice(statuses),
            'Estimate': random.choice([1, 2, 3, 5]),
            'Priority': random.choice(priorities),
            'Project ID': f'd48fc7ec-c55e-4011-91a2-e4bde2d8{random.randint(100, 999)}',
            'Project': random.choice(projects),
            'Creator': random.choice(assignees),
            'Assignee': random.choice(assignees),
            'Labels': 'Task',
            'Cycle Number': cycle_number,
            'Cycle Name': cycle_name,
            'Cycle Start': (created_date - timedelta(days=7)).strftime('%m/%d/%Y %H:%M:%S'),
            'Cycle End': (created_date + timedelta(days=14)).strftime('%m/%d/%Y %H:%M:%S'),
            'Created': created_date.strftime('%m/%d/%Y %H:%M:%S'),
            'Updated': updated_date.strftime('%m/%d/%Y %H:%M:%S'),
            'Started': started_date.strftime('%m/%d/%Y %H:%M:%S') if started_date else '',
            'Triaged': '',
            'Completed': completed_date.strftime('%m/%d/%Y %H:%M:%S') if completed_date else '',
            'Canceled': '',
            'Archived': '',
            'Due Date': '',
            'Parent issue': '',
            'Initiatives': '',
            'Project Milestone ID': '',
            'Project Milestone': '',
            'SLA Status': '',
            'Roadmaps': '',
            
            # Also create the dashboard-friendly mapped columns
            'id': f'SWE-{100 + i}',
            'team': 'Software',
            'title': f'Sample Issue {i+1}',
            'description': f'Sample description for issue {i+1}',
            'status': 'Done' if is_completed else random.choice(statuses),
            'assignee': random.choice(assignees),
            'estimate': random.choice([1, 2, 3, 5]),
            'priority': random.choice(priorities),
            'cycle': cycle_name,
            'createdat': created_date,
            'updatedat': updated_date,
            'startedat': started_date,
            'completedat': completed_date,
            'cycle_time_days': (completed_date - started_date).days if completed_date and started_date else None
        }
        
        data.append(issue)
    
    return pd.DataFrame(data)

def get_sample_okr_data() -> pd.DataFrame:
    """
    Generate sample OKR data for testing
    """
    data = [
        {
            'objective': 'Improve Product Quality',
            'key_result': 'Reduce bug count by 50%',
            'owner': 'Alice Johnson',
            'target': 100,
            'current': 75,
            'status': 'On Track'
        },
        {
            'objective': 'Improve Product Quality',
            'key_result': 'Achieve 95% test coverage',
            'owner': 'Bob Chen',
            'target': 95,
            'current': 88,
            'status': 'At Risk'
        },
        {
            'objective': 'Increase User Engagement',
            'key_result': 'Grow daily active users by 30%',
            'owner': 'Carol Davis',
            'target': 10000,
            'current': 8500,
            'status': 'On Track'
        },
        {
            'objective': 'Increase User Engagement',
            'key_result': 'Reduce churn rate to under 5%',
            'owner': 'David Kim',
            'target': 5,
            'current': 7,
            'status': 'Behind'
        },
        {
            'objective': 'Team Efficiency',
            'key_result': 'Increase sprint velocity by 25%',
            'owner': 'Eva Rodriguez',
            'target': 50,
            'current': 45,
            'status': 'On Track'
        }
    ]
    
    df = pd.DataFrame(data)
    df['progress'] = (df['current'] / df['target'] * 100).round(1)
    
    return df 