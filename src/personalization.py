"""
Personalization Module for DuPont Tedlar Lead Generation

This module handles generating personalized outreach messages for stakeholders.
"""

import json
import logging
import os
import random
from typing import Dict, List, Optional, Tuple, Any

import pandas as pd
from tqdm import tqdm

from src.utils import load_config, load_json, save_json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PersonalizationEngine:
    """Generates personalized outreach messages for stakeholders."""
    
    def __init__(self, config: Dict, leads_with_stakeholders: List[Dict]):
        self.config = config
        self.leads_with_stakeholders = leads_with_stakeholders
        
        # In a production environment, this would use the OpenAI API
        # For the prototype, we'll use templates with variable substitution
        self.llm_config = config.get('llm', {})
        self.leads_with_outreach = []
    
    def generate_outreach_messages(self) -> List[Dict]:
        """
        Generate personalized outreach messages for stakeholders.
        
        Returns:
            List[Dict]: Leads with personalized outreach messages
        """
        logger.info("Generating personalized outreach messages for stakeholders")
        
        leads_with_outreach = []
        
        for lead in tqdm(self.leads_with_stakeholders, desc="Generating outreach messages"):
            lead_with_outreach = lead.copy()
            stakeholders_with_outreach = []
            
            for stakeholder in lead['stakeholders']:
                stakeholder_with_outreach = stakeholder.copy()
                
                # Generate personalized outreach message
                outreach_message = self._generate_message(lead, stakeholder)
                stakeholder_with_outreach['outreach_message'] = outreach_message
                
                # Generate subject line
                subject_line = self._generate_subject_line(lead, stakeholder)
                stakeholder_with_outreach['subject_line'] = subject_line
                
                stakeholders_with_outreach.append(stakeholder_with_outreach)
            
            lead_with_outreach['stakeholders'] = stakeholders_with_outreach
            leads_with_outreach.append(lead_with_outreach)
        
        self.leads_with_outreach = leads_with_outreach
        logger.info(f"Generated outreach messages for stakeholders at {len(leads_with_outreach)} companies")
        
        return leads_with_outreach
    
    def _generate_message(self, lead: Dict, stakeholder: Dict) -> str:
        """
        Generate a personalized outreach message for a stakeholder.
        In a production system, this would use the OpenAI API.
        
        Args:
            lead: Company data
            stakeholder: Stakeholder data
            
        Returns:
            str: Personalized outreach message
        """
        # In a production system, we would use a prompt like this with OpenAI:
        """
        prompt = f'''
        Generate a personalized email outreach message from a DuPont Tedlar sales representative to a potential lead.
        
        Company: {lead['name']}
        Industry: {lead['industry']}
        Recipient: {stakeholder['name']}
        Title: {stakeholder['title']}
        Interest areas: {', '.join(stakeholder.get('interest_areas', []))}
        
        Qualification rationale:
        {lead.get('qualification_rationale', '')}
        
        Keep the message brief (3-4 paragraphs), personalized, and focused on how DuPont Tedlar's protective films
        can benefit their signage and graphics applications with superior weather resistance, UV protection, and durability.
        
        Mention any relevant events or associations they're part of. Be conversational, not pushy.
        '''
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model=self.llm_config.get('model', 'gpt-4'),
            messages=[{'role': 'user', 'content': prompt}],
            temperature=self.llm_config.get('temperature', 0.7),
            max_tokens=self.llm_config.get('max_tokens', 500)
        )
        
        return response.choices[0].message.content
        """
        
        # For the prototype, we'll use a template-based approach
        company_name = lead['name']
        stakeholder_name = stakeholder['name']
        stakeholder_title = stakeholder['title']
        company_industry = lead.get('industry', 'signage and graphics')
        
        # Get interests if available
        interests = stakeholder.get('interest_areas', [])
        interest_text = ""
        if interests:
            interest_text = f"Your focus on {interests[0]}"
            if len(interests) > 1:
                interest_text += f" and {interests[1]}"
            interest_text += " aligns with our mission."
        
        # Get events information
        events = lead.get('events', [])
        events_text = ""
        if events:
            event_name = events[0]['event_name']
            events_text = f"I noticed that {company_name} will be at {event_name} this year."
        
        # Get association information
        associations = lead.get('associations', [])
        associations_text = ""
        if associations:
            association_name = associations[0]['association_name']
            associations_text = f"I see we're both members of {association_name}."
        
        # Generate engagement context
        engagement_context = ""
        if events_text and associations_text:
            engagement_context = f"{events_text} {associations_text}"
        elif events_text:
            engagement_context = events_text
        elif associations_text:
            engagement_context = associations_text
        
        # Rationale text
        rationale = lead.get('qualification_rationale', '')
        
        # Generate message templates
        templates = [
            f"""Hi {stakeholder_name},

I hope this email finds you well. My name is Sarah from DuPont Tedlar, and I'm reaching out because we've developed protective film solutions that have been helping companies like {company_name} improve durability and weather resistance in their {company_industry} applications.

{engagement_context} {interest_text} Our Tedlar® protective films offer superior UV protection and weather resistance that can extend the life of your graphics products by up to 7 years compared to unprotected materials.

Would you be available for a 15-minute call next week to discuss how our solutions might benefit your specific applications? I'm happy to share some case studies from companies with similar requirements.

Best regards,
Sarah Miller
Senior Account Manager
DuPont Tedlar
sarah.miller@dupont.com
(302) 555-1234""",

            f"""Hello {stakeholder_name},

I'm Michael from DuPont Tedlar's Graphics & Signage team. I've been following {company_name}'s innovative work in the {company_industry} space and wanted to connect.

{engagement_context} Given your role as {stakeholder_title}, I thought you might be interested in our latest Tedlar® protective film technology that has been helping industry leaders achieve 5x longer outdoor durability with enhanced color stability.

Our team has recently completed testing showing significant performance improvements over traditional laminates in harsh weather conditions. I'd be happy to share these results and discuss how they might apply to your specific products.

Do you have 15 minutes for a quick call next Tuesday or Wednesday?

Regards,
Michael Johnson
Technical Solutions Manager
DuPont Tedlar
m.johnson@dupont.com
(302) 555-4321"""
        ]
        
        # Select a template
        template_index = hash(stakeholder_name) % len(templates)
        message = templates[template_index]
        
        return message
    
    def _generate_subject_line(self, lead: Dict, stakeholder: Dict) -> str:
        """
        Generate a subject line for the outreach message.
        
        Args:
            lead: Company data
            stakeholder: Stakeholder data
            
        Returns:
            str: Email subject line
        """
        company_name = lead['name']
        industry = lead.get('industry', 'Graphics & Signage')
        
        # Subject line templates
        templates = [
            f"DuPont Tedlar solutions for {company_name}'s {industry} applications",
            f"Enhanced durability for {company_name}'s {industry} products",
            f"Protective film technology for {company_name} | DuPont Tedlar",
            f"Improving {industry} longevity with DuPont Tedlar",
            f"Weather-resistant solutions for {company_name} | Quick discussion?",
            f"DuPont Tedlar: Extending the life of {industry} applications"
        ]
        
        # Select a template
        template_index = hash(stakeholder['name']) % len(templates)
        subject_line = templates[template_index]
        
        return subject_line
    
    def save_outreach_data(self, output_file: str = 'data/leads_with_outreach.json') -> str:
        """
        Save leads with outreach data to a JSON file.
        
        Args:
            output_file: Path to save the outreach data
            
        Returns:
            str: Path to the saved file
        """
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        save_json(self.leads_with_outreach, output_file)
        
        logger.info(f"Saved outreach data for {len(self.leads_with_outreach)} leads to {output_file}")
        
        return output_file


def run_personalization_engine(leads_with_stakeholders_file: str, config_path: str = 'config.yaml') -> str:
    """
    Run the personalization engine.
    
    Args:
        leads_with_stakeholders_file: Path to the leads with stakeholders data file
        config_path: Path to the configuration file
        
    Returns:
        str: Path to the saved outreach data file
    """
    config = load_config(config_path)
    leads_with_stakeholders = load_json(leads_with_stakeholders_file)
    
    engine = PersonalizationEngine(config, leads_with_stakeholders)
    
    # Generate outreach messages
    engine.generate_outreach_messages()
    
    # Save outreach data
    return engine.save_outreach_data()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        leads_with_stakeholders_file = sys.argv[1]
    else:
        leads_with_stakeholders_file = 'data/stakeholders.json'
    
    run_personalization_engine(leads_with_stakeholders_file)