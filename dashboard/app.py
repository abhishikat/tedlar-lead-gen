"""
Dashboard for DuPont Tedlar Lead Generation.

This module provides a Streamlit dashboard to visualize lead generation results.
"""

import json
import logging
import os
from typing import Dict, List, Optional, Tuple

import pandas as pd
import streamlit as st

from src.utils import load_json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set page configuration
st.set_page_config(
    page_title="DuPont Tedlar Lead Generation Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_lead_data(data_path: str = 'data/leads_with_outreach.json') -> List[Dict]:
    """
    Load lead data from JSON file.
    
    Args:
        data_path: Path to the lead data file
        
    Returns:
        List[Dict]: Lead data
    """
    if not os.path.exists(data_path):
        st.error(f"Data file not found: {data_path}")
        st.info("Please run the lead generation pipeline first with: python main.py")
        return []
    
    return load_json(data_path)

def dashboard():
    """Main dashboard function."""
    # Title and header
    st.title("DuPont Tedlar Lead Generation Dashboard")
    st.markdown("### Automated Lead Generation & Outreach for Graphics & Signage Team")
    
    # Sidebar
    st.sidebar.header("Filters")
    
    # Load data
    leads_data = load_lead_data()
    
    if not leads_data:
        st.warning("No lead data available. Please run the lead generation pipeline first.")
        return
    
    # Extract company names for filter
    company_names = [lead['name'] for lead in leads_data]
    company_names.sort()
    
    # Filter by company
    selected_companies = st.sidebar.multiselect(
        "Filter by Company:",
        options=company_names,
        default=[]
    )
    
    # Event filter
    all_events = set()
    for lead in leads_data:
        for event in lead.get('events', []):
            all_events.add(event['event_name'])
    
    selected_events = st.sidebar.multiselect(
        "Filter by Event:",
        options=sorted(list(all_events)),
        default=[]
    )
    
    # Association filter
    all_associations = set()
    for lead in leads_data:
        for assoc in lead.get('associations', []):
            all_associations.add(assoc['association_name'])
    
    selected_associations = st.sidebar.multiselect(
        "Filter by Association:",
        options=sorted(list(all_associations)),
        default=[]
    )
    
    # Score threshold filter
    min_score = st.sidebar.slider(
        "Minimum Lead Score:",
        min_value=7.0,
        max_value=10.0,
        value=7.0,
        step=0.1
    )
    
    # Apply filters
    filtered_leads = leads_data.copy()
    
    if selected_companies:
        filtered_leads = [lead for lead in filtered_leads if lead['name'] in selected_companies]
    
    if selected_events:
        filtered_leads = [
            lead for lead in filtered_leads 
            if any(event['event_name'] in selected_events for event in lead.get('events', []))
        ]
    
    if selected_associations:
        filtered_leads = [
            lead for lead in filtered_leads 
            if any(assoc['association_name'] in selected_associations for assoc in lead.get('associations', []))
        ]
    
    filtered_leads = [lead for lead in filtered_leads if lead.get('overall_score', 0) >= min_score]
    
    # Sort leads by overall score
    filtered_leads.sort(key=lambda x: x.get('overall_score', 0), reverse=True)
    
    # Dashboard metrics
    st.markdown("## Lead Generation Overview")
    
    # Create metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Qualified Leads", len(leads_data))
    with col2:
        st.metric("Filtered Leads", len(filtered_leads))
    with col3:
        total_stakeholders = sum(len(lead.get('stakeholders', [])) for lead in filtered_leads)
        st.metric("Decision Makers", total_stakeholders)
    with col4:
        avg_score = sum(lead.get('overall_score', 0) for lead in filtered_leads) / max(1, len(filtered_leads))
        st.metric("Average Lead Score", f"{avg_score:.1f}/10")
    
    # Lead table
    st.markdown("## Qualified Leads")
    
    if not filtered_leads:
        st.warning("No leads match the selected filters.")
        return
    
    # Create a table for lead overview
    lead_table_data = []
    for lead in filtered_leads:
        lead_table_data.append({
            "Company": lead['name'],
            "Industry": lead.get('industry', 'N/A'),
            "Revenue": lead.get('estimated_revenue', 'N/A'),
            "Lead Score": f"{lead.get('overall_score', 0):.1f}/10",
            "Events": ", ".join(event['event_name'] for event in lead.get('events', [])[:2]),
            "Associations": ", ".join(assoc['association_name'] for assoc in lead.get('associations', [])[:2]),
            "Decision Makers": len(lead.get('stakeholders', []))
        })
    
    lead_df = pd.DataFrame(lead_table_data)
    st.dataframe(lead_df, hide_index=True)
    
    # Lead details
    st.markdown("## Lead Details")
    
    # Select a lead to view details
    selected_lead_name = st.selectbox(
        "Select a company to view details:",
        options=[lead['name'] for lead in filtered_leads]
    )
    
    if selected_lead_name:
        selected_lead = next((lead for lead in filtered_leads if lead['name'] == selected_lead_name), None)
        
        if selected_lead:
            st.markdown(f"### {selected_lead['name']}")
            
            # Company information
            with st.expander("Company Information", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Industry:** {selected_lead.get('industry', 'N/A')}")
                    st.markdown(f"**Revenue:** {selected_lead.get('estimated_revenue', 'N/A')}")
                    st.markdown(f"**Employees:** {selected_lead.get('employee_count', 'N/A')}")
                    
                with col2:
                    st.markdown(f"**Website:** {selected_lead.get('website', 'N/A')}")
                    st.markdown(f"**Overall Score:** {selected_lead.get('overall_score', 0):.1f}/10")
                    st.markdown(f"**Keywords:** {', '.join(selected_lead.get('keywords', []))}")
            
            # Qualification rationale
            with st.expander("Qualification Rationale", expanded=True):
                st.markdown(selected_lead.get('qualification_rationale', 'No rationale available.'))
            
            # Events and associations
            col1, col2 = st.columns(2)
            
            with col1:
                with st.expander("Events", expanded=True):
                    if selected_lead.get('events'):
                        for event in selected_lead['events']:
                            st.markdown(f"**{event['event_name']}**")
                            st.markdown(f"Date: {event.get('event_date', 'N/A')}")
                            st.markdown(f"Booth: {event.get('booth_number', 'N/A')}")
                            st.markdown(f"Sponsorship: {'Yes' if event.get('sponsorship') else 'No'}")
                            st.markdown("---")
                    else:
                        st.markdown("No event information available.")
            
            with col2:
                with st.expander("Associations", expanded=True):
                    if selected_lead.get('associations'):
                        for assoc in selected_lead['associations']:
                            st.markdown(f"**{assoc['association_name']}**")
                            st.markdown(f"Membership Level: {assoc.get('membership_level', 'N/A')}")
                            st.markdown(f"Years Member: {assoc.get('years_member', 'N/A')}")
                            st.markdown(f"Committee Participation: {'Yes' if assoc.get('committee_participation') else 'No'}")
                            st.markdown("---")
                    else:
                        st.markdown("No association information available.")
            
            # Stakeholders and outreach
            st.markdown("### Key Decision Makers")
            
            if selected_lead.get('stakeholders'):
                # Create tabs for each stakeholder
                stakeholder_tabs = st.tabs([f"{s['name']} ({s['title']})" for s in selected_lead['stakeholders']])
                
                for i, tab in enumerate(stakeholder_tabs):
                    stakeholder = selected_lead['stakeholders'][i]
                    
                    with tab:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Name:** {stakeholder['name']}")
                            st.markdown(f"**Title:** {stakeholder['title']}")
                            st.markdown(f"**Department:** {stakeholder.get('department', 'N/A')}")
                            st.markdown(f"**Location:** {stakeholder.get('location', 'N/A')}")
                            st.markdown(f"**Years at Company:** {stakeholder.get('years_at_company', 'N/A')}")
                            st.markdown(f"**LinkedIn:** [Profile]({stakeholder.get('linkedin_url', '#')})")
                            st.markdown(f"**Email:** {stakeholder.get('email', 'N/A')}")
                        
                        with col2:
                            st.markdown(f"**Relevance Score:** {stakeholder.get('relevance_score', 0):.1f}/10")
                            st.markdown(f"**Title Match Score:** {stakeholder.get('title_match_score', 0):.1f}/10")
                            st.markdown(f"**Seniority Score:** {stakeholder.get('seniority_score', 0):.1f}/10")
                            st.markdown(f"**Interest Areas:**")
                            for interest in stakeholder.get('interest_areas', []):
                                st.markdown(f"- {interest}")
                        
                        # Outreach message
                        st.markdown("#### Personalized Outreach")
                        st.markdown(f"**Subject Line:** {stakeholder.get('subject_line', 'N/A')}")
                        
                        # Format email message with proper line breaks
                        email_message = stakeholder.get('outreach_message', 'No outreach message available.')
                        st.text_area("Email Message", email_message, height=300)
                        
                        # Add a button to "send" the email (mock functionality)
                        col1, col2, col3 = st.columns([1, 1, 2])
                        with col1:
                            if st.button(f"Send Email", key=f"send_{stakeholder['name']}"):
                                st.success(f"Email sent to {stakeholder['name']}!")
                        with col2:
                            if st.button(f"Edit Message", key=f"edit_{stakeholder['name']}"):
                                st.info("Message editor would open here.")
            else:
                st.markdown("No stakeholder information available.")

if __name__ == "__main__":
    dashboard()