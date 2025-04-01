"""
Data Collection Module for DuPont Tedlar Lead Generation

This module handles collecting information about relevant industry events,
associations, and companies for lead generation.
"""

import json
import logging
import os
import re
import time
from typing import Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

from src.utils import load_config, save_json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EventScraper:
    """Scraper for industry events and attendee companies."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.events_data = []
        self.companies_data = []
        
    def scrape_events(self) -> List[Dict]:
        """
        Scrape information about industry events from the config.
        In a production system, this would perform actual web scraping.
        
        Returns:
            List[Dict]: Information about relevant events
        """
        logger.info("Starting event data collection")
        
        # For the prototype, we're using pre-configured event data
        # In a production system, this would involve actual web scraping
        events_data = self.config['target_events']
        
        # Enrich event data with exhibitor information
        enriched_events = []
        for event in tqdm(events_data, desc="Processing events"):
            event_info = {
                'name': event['name'],
                'url': event['url'],
                'date': event['date'],
                'location': event['location'],
                'relevance_score': event['relevance_score'],
                'exhibitors': self._mock_get_exhibitors(event['name'], 
                                                       self.config['icp_criteria']['industries'])
            }
            enriched_events.append(event_info)
            
        self.events_data = enriched_events
        logger.info(f"Collected data for {len(enriched_events)} events")
        return enriched_events
    
    def _mock_get_exhibitors(self, event_name: str, target_industries: List[str]) -> List[Dict]:
        """
        Mock function to generate exhibitor data for an event.
        In a production system, this would scrape actual exhibitor lists.
        
        Args:
            event_name: Name of the event
            target_industries: List of target industries to filter by
            
        Returns:
            List[Dict]: Mock exhibitor data
        """
        # This is simulated data for the prototype
        # A real implementation would scrape exhibitor lists from event websites
        
        # Sample companies in the graphics and signage industry
        sample_companies = [
            {"name": "Avery Dennison Graphics Solutions", "website": "https://graphics.averydennison.com", "industry": "Signage and Graphics"},
            {"name": "3M Commercial Graphics", "website": "https://www.3m.com/3M/en_US/graphics-signage-us", "industry": "Signage and Graphics"},
            {"name": "HP Large Format Printing", "website": "https://www.hp.com/us-en/large-format-printers", "industry": "Large Format Printing"},
            {"name": "Roland DGA", "website": "https://www.rolanddga.com", "industry": "Large Format Printing"},
            {"name": "Hexis Graphics", "website": "https://www.hexis-graphics.com", "industry": "Vehicle Wraps"},
            {"name": "Arlon Graphics", "website": "https://www.arlon.com", "industry": "Vehicle Wraps"},
            {"name": "Mimaki", "website": "https://www.mimaki.com", "industry": "Graphic Arts"},
            {"name": "Epson Professional Imaging", "website": "https://epson.com/professional-imaging", "industry": "Graphic Arts"},
            {"name": "Ritrama", "website": "https://www.ritrama.com", "industry": "Protective Films"},
            {"name": "Orafol", "website": "https://www.orafol.com", "industry": "Protective Films"},
            {"name": "Drytac", "website": "https://www.drytac.com", "industry": "Architectural Graphics"},
            {"name": "FLEXcon", "website": "https://www.flexcon.com", "industry": "Architectural Graphics"},
            {"name": "Mactac", "website": "https://www.mactac.com", "industry": "Fleet Graphics"},
            {"name": "LG Ad Solutions", "website": "https://www.lgadsolutions.com", "industry": "Outdoor Advertising"},
            {"name": "Agfa Graphics", "website": "https://www.agfa.com/printing", "industry": "Graphic Arts"},
            {"name": "Fujifilm Graphic Systems", "website": "https://www.fujifilm.com/us/en/business/graphic-arts", "industry": "Graphic Arts"},
            {"name": "Graphic Solutions Group", "website": "https://www.gogsg.com", "industry": "Signage and Graphics"},
        ]
        
        # Randomly select some companies for each event, with different sets for different events
        import random
        random.seed(hash(event_name) % 100)  # Use event name as seed for consistent but different selections
        
        # Select between 8-15 companies for the event
        num_companies = random.randint(8, 15)
        selected_companies = random.sample(sample_companies, min(num_companies, len(sample_companies)))
        
        # Add some random attributes to make each company entry unique
        for company in selected_companies:
            company["booth_number"] = f"#{random.randint(100, 999)}"
            company["years_attending"] = random.randint(1, 10)
            company["has_sponsorship"] = random.choice([True, False])
        
        return selected_companies
        
    def extract_companies(self) -> List[Dict]:
        """
        Extract unique companies from event exhibitor data.
        
        Returns:
            List[Dict]: Unique companies with basic information
        """
        if not self.events_data:
            logger.warning("No event data available. Run scrape_events() first.")
            return []
        
        all_companies = {}
        
        for event in self.events_data:
            for exhibitor in event['exhibitors']:
                company_name = exhibitor['name']
                
                if company_name not in all_companies:
                    all_companies[company_name] = {
                        'name': company_name,
                        'website': exhibitor['website'],
                        'industry': exhibitor['industry'],
                        'events': []
                    }
                
                # Add this event to the company's list of events
                all_companies[company_name]['events'].append({
                    'event_name': event['name'],
                    'event_date': event['date'],
                    'booth_number': exhibitor.get('booth_number', 'N/A'),
                    'sponsorship': exhibitor.get('has_sponsorship', False)
                })
        
        # Convert dictionary to list
        companies_list = list(all_companies.values())
        self.companies_data = companies_list
        
        logger.info(f"Extracted {len(companies_list)} unique companies from events")
        return companies_list
    
    def scrape_associations(self) -> List[Dict]:
        """
        Scrape information about industry associations from the config.
        In a production system, this would perform actual web scraping.
        
        Returns:
            List[Dict]: Information about relevant associations
        """
        logger.info("Starting association data collection")
        
        # For the prototype, we're using pre-configured association data
        associations_data = self.config['target_associations']
        
        # Enrich association data with member information
        enriched_associations = []
        for association in tqdm(associations_data, desc="Processing associations"):
            association_info = {
                'name': association['name'],
                'url': association['url'],
                'relevance_score': association['relevance_score'],
                'members': self._mock_get_members(association['name'])
            }
            enriched_associations.append(association_info)
        
        logger.info(f"Collected data for {len(enriched_associations)} associations")
        return enriched_associations
    
    def _mock_get_members(self, association_name: str) -> List[Dict]:
        """
        Mock function to generate member data for an association.
        In a production system, this would scrape actual member lists.
        
        Args:
            association_name: Name of the association
            
        Returns:
            List[Dict]: Mock member data
        """
        # This is simulated data for the prototype
        # A real implementation would scrape member lists from association websites
        
        # Sample companies in the graphics and signage industry
        sample_companies = [
            {"name": "Avery Dennison Graphics Solutions", "website": "https://graphics.averydennison.com", "membership_level": "Platinum"},
            {"name": "3M Commercial Graphics", "website": "https://www.3m.com/3M/en_US/graphics-signage-us", "membership_level": "Gold"},
            {"name": "HP Large Format Printing", "website": "https://www.hp.com/us-en/large-format-printers", "membership_level": "Silver"},
            {"name": "Roland DGA", "website": "https://www.rolanddga.com", "membership_level": "Gold"},
            {"name": "Hexis Graphics", "website": "https://www.hexis-graphics.com", "membership_level": "Silver"},
            {"name": "Arlon Graphics", "website": "https://www.arlon.com", "membership_level": "Gold"},
            {"name": "Mimaki", "website": "https://www.mimaki.com", "membership_level": "Platinum"},
            {"name": "Epson Professional Imaging", "website": "https://epson.com/professional-imaging", "membership_level": "Gold"},
            {"name": "Ritrama", "website": "https://www.ritrama.com", "membership_level": "Silver"},
            {"name": "Orafol", "website": "https://www.orafol.com", "membership_level": "Bronze"},
            {"name": "Drytac", "website": "https://www.drytac.com", "membership_level": "Bronze"},
            {"name": "FLEXcon", "website": "https://www.flexcon.com", "membership_level": "Silver"},
            {"name": "Mactac", "website": "https://www.mactac.com", "membership_level": "Bronze"},
            {"name": "LG Ad Solutions", "website": "https://www.lgadsolutions.com", "membership_level": "Silver"},
            {"name": "Agfa Graphics", "website": "https://www.agfa.com/printing", "membership_level": "Gold"},
        ]
        
        # Randomly select some companies for each association, with different sets for different associations
        import random
        random.seed(hash(association_name) % 100)  # Use association name as seed for consistent but different selections
        
        # Select between 7-12 companies for the association
        num_companies = random.randint(7, 12)
        selected_companies = random.sample(sample_companies, min(num_companies, len(sample_companies)))
        
        # Add some random attributes to make each company entry unique
        for company in selected_companies:
            company["years_member"] = random.randint(1, 15)
            company["committee_participation"] = random.choice([True, False])
        
        return selected_companies
    
    def merge_event_and_association_data(self) -> List[Dict]:
        """
        Merge company data from events and associations.
        
        Returns:
            List[Dict]: Enriched company data
        """
        if not self.companies_data:
            logger.warning("No company data available. Run extract_companies() first.")
            return []
        
        # Get association data
        associations_data = self.scrape_associations()
        
        # Create a lookup for existing companies
        companies_by_name = {company['name']: company for company in self.companies_data}
        
        # Add association data to companies
        for association in associations_data:
            for member in association['members']:
                company_name = member['name']
                
                if company_name in companies_by_name:
                    # Company exists, add association data
                    if 'associations' not in companies_by_name[company_name]:
                        companies_by_name[company_name]['associations'] = []
                    
                    companies_by_name[company_name]['associations'].append({
                        'association_name': association['name'],
                        'membership_level': member['membership_level'],
                        'years_member': member['years_member'],
                        'committee_participation': member['committee_participation']
                    })
                else:
                    # New company from association
                    companies_by_name[company_name] = {
                        'name': company_name,
                        'website': member['website'],
                        'industry': 'Unknown',  # We don't have industry data from associations
                        'events': [],
                        'associations': [{
                            'association_name': association['name'],
                            'membership_level': member['membership_level'],
                            'years_member': member['years_member'],
                            'committee_participation': member['committee_participation']
                        }]
                    }
        
        # Update the companies data
        merged_companies = list(companies_by_name.values())
        self.companies_data = merged_companies
        
        logger.info(f"Merged data for {len(merged_companies)} companies from events and associations")
        return merged_companies
    
    def save_data(self, output_dir: str = 'data') -> Tuple[str, str]:
        """
        Save collected data to JSON files.
        
        Args:
            output_dir: Directory to save data files
            
        Returns:
            Tuple[str, str]: Paths to the saved events and companies files
        """
        os.makedirs(output_dir, exist_ok=True)
        
        events_file = os.path.join(output_dir, 'events.json')
        companies_file = os.path.join(output_dir, 'companies.json')
        
        save_json(self.events_data, events_file)
        save_json(self.companies_data, companies_file)
        
        logger.info(f"Saved events data to {events_file}")
        logger.info(f"Saved companies data to {companies_file}")
        
        return events_file, companies_file


def run_data_collection(config_path: str = 'config.yaml') -> Tuple[str, str]:
    """
    Run the data collection process.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Tuple[str, str]: Paths to the saved events and companies files
    """
    config = load_config(config_path)
    scraper = EventScraper(config)
    
    # Scrape events and extract companies
    scraper.scrape_events()
    scraper.extract_companies()
    
    # Merge event and association data
    scraper.merge_event_and_association_data()
    
    # Save data
    return scraper.save_data()


if __name__ == "__main__":
    run_data_collection()