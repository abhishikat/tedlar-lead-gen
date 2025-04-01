"""
UI components for the DuPont Tedlar Lead Generation Dashboard.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def render_score_gauge(score: float, title: str = "Score") -> None:
    """
    Render a gauge chart for a score.
    
    Args:
        score: Score value (0-10)
        title: Title for the gauge
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [0, 10], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 5], 'color': '#FF9999'},
                {'range': [5, 7], 'color': '#FFCC99'},
                {'range': [7, 9], 'color': '#CCFF99'},
                {'range': [9, 10], 'color': '#99FF99'},
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 7
            }
        }
    ))
    
    fig.update_layout(
        height=200,
        margin=dict(l=20, r=20, t=30, b=20),
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_company_card(company: dict) -> None:
    """
    Render a company card with key information.
    
    Args:
        company: Company data dictionary
    """
    with st.container():
        st.markdown(f"### {company['name']}")
        st.markdown(f"**Industry:** {company.get('industry', 'N/A')}")
        st.markdown(f"**Score:** {company.get('overall_score', 0):.1f}/10")
        
        # Display qualification rationale
        st.markdown("**Qualification Rationale:**")
        st.markdown(company.get('qualification_rationale', 'No rationale available.'))
        
        # Display stakeholders
        st.markdown("**Key Stakeholders:**")
        for stakeholder in company.get('stakeholders', [])[:2]:  # Display top 2 stakeholders
            st.markdown(f"- {stakeholder['name']} ({stakeholder['title']})")
        
        # View details button
        if st.button("View Details", key=f"view_{company['name']}"):
            st.session_state.selected_company = company['name']

def render_score_breakdown(scores: dict) -> None:
    """
    Render a bar chart showing score breakdown.
    
    Args:
        scores: Dictionary of score components
    """
    score_data = {
        'Category': [
            'Industry Fit', 
            'Company Size', 
            'Keyword Relevance', 
            'Engagement'
        ],
        'Score': [
            scores.get('industry_score', 0),
            scores.get('size_score', 0),
            scores.get('keyword_score', 0),
            scores.get('engagement_score', 0)
        ]
    }
    
    df = pd.DataFrame(score_data)
    
    fig = px.bar(
        df, 
        x='Category', 
        y='Score',
        text='Score',
        color='Score',
        color_continuous_scale=px.colors.sequential.Blues,
        range_y=[0, 10],
        labels={'Score': 'Score (0-10)'}
    )
    
    fig.update_traces(texttemplate='%{text:.1f}', textposition='auto')
    fig.update_layout(
        title="Lead Score Breakdown",
        height=400,
        xaxis_title=None,
        coloraxis_showscale=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_stakeholders_table(stakeholders: list) -> None:
    """
    Render a table of stakeholders.
    
    Args:
        stakeholders: List of stakeholder dictionaries
    """
    if not stakeholders:
        st.warning("No stakeholders available.")
        return
    
    # Create a table for stakeholders
    stakeholder_data = []
    for s in stakeholders:
        stakeholder_data.append({
            "Name": s['name'],
            "Title": s['title'],
            "Department": s.get('department', 'N/A'),
            "Score": f"{s.get('overall_score', 0):.1f}/10",
            "Email": s.get('email', 'N/A')
        })
    
    stakeholder_df = pd.DataFrame(stakeholder_data)
    st.dataframe(stakeholder_df, hide_index=True)

def render_email_preview(stakeholder: dict) -> None:
    """
    Render an email preview for a stakeholder.
    
    Args:
        stakeholder: Stakeholder dictionary with outreach information
    """
    with st.container():
        st.markdown("### Email Preview")
        
        # Email header
        st.markdown(f"**To:** {stakeholder.get('name')} <{stakeholder.get('email', 'email@example.com')}>")
        st.markdown(f"**Subject:** {stakeholder.get('subject_line', 'No subject available')}")
        
        # Email body
        st.markdown("**Body:**")
        st.text_area(
            label="",
            value=stakeholder.get('outreach_message', 'No message available.'),
            height=300,
            key=f"email_body_{stakeholder['name']}"
        )
        
        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("Send", key=f"send_email_{stakeholder['name']}"):
                st.success("Email sent successfully!")
        with col2:
            if st.button("Save Draft", key=f"save_draft_{stakeholder['name']}"):
                st.info("Draft saved successfully!")

def render_company_events(events: list) -> None:
    """
    Render a timeline of company events.
    
    Args:
        events: List of event dictionaries
    """
    if not events:
        st.info("No events available for this company.")
        return
    
    # Create a DataFrame for events
    event_data = []
    for event in events:
        event_data.append({
            "Event": event['event_name'],
            "Date": event.get('event_date', 'Unknown'),
            "Sponsorship": "Yes" if event.get('sponsorship') else "No",
            "Booth": event.get('booth_number', 'N/A')
        })
    
    event_df = pd.DataFrame(event_data)
    
    # Sort by date if possible
    try:
        event_df['Date'] = pd.to_datetime(event_df['Date'])
        event_df = event_df.sort_values('Date')
    except:
        pass
    
    st.dataframe(event_df, hide_index=True)

def render_top_leads_chart(leads: list) -> None:
    """
    Render a horizontal bar chart of top leads by score.
    
    Args:
        leads: List of lead dictionaries
    """
    if not leads:
        st.warning("No leads available.")
        return
    
    # Get top 10 leads by score
    top_leads = sorted(leads, key=lambda x: x.get('overall_score', 0), reverse=True)[:10]
    
    # Create DataFrame
    lead_data = {
        'Company': [lead['name'] for lead in top_leads],
        'Score': [lead.get('overall_score', 0) for lead in top_leads]
    }
    
    df = pd.DataFrame(lead_data)
    
    # Create horizontal bar chart
    fig = px.bar(
        df, 
        y='Company', 
        x='Score',
        orientation='h',
        text='Score',
        color='Score',
        color_continuous_scale=px.colors.sequential.Blues,
        range_x=[0, 10],
        labels={'Score': 'Lead Score (0-10)'}
    )
    
    fig.update_traces(texttemplate='%{text:.1f}', textposition='auto')
    fig.update_layout(
        title="Top Qualified Leads",
        height=400,
        yaxis={'categoryorder': 'total ascending'},
        coloraxis_showscale=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_industry_distribution(leads: list) -> None:
    """
    Render a pie chart showing industry distribution of leads.
    
    Args:
        leads: List of lead dictionaries
    """
    if not leads:
        st.warning("No leads available.")
        return
    
    # Count leads by industry
    industries = {}
    for lead in leads:
        industry = lead.get('industry', 'Unknown')
        if industry in industries:
            industries[industry] += 1
        else:
            industries[industry] = 1
    
    # Create DataFrame
    industry_data = {
        'Industry': list(industries.keys()),
        'Count': list(industries.values())
    }
    
    df = pd.DataFrame(industry_data)
    
    # Create pie chart
    fig = px.pie(
        df,
        values='Count',
        names='Industry',
        title='Lead Distribution by Industry',
        color_discrete_sequence=px.colors.sequential.Blues,
        hole=0.3
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)