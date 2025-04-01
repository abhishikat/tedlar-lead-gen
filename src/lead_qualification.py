"""
Lead Qualification Module for DuPont Tedlar Lead Generation

This module handles evaluating and prioritizing companies based on ICP criteria.
"""

import json
import logging
import os
import random
from typing import Dict, List, Optional, Tuple

import pandas as pd
from tqdm import tqdm

from src.utils import load_config, load_json, save_json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LeadQualifier:
    """Qualifies and prioritizes leads based on DuPont Tedlar's ICP."""
    
    def __init__(self, config: Dict, companies_data: List[Dict]):
        self.config = config
        self.companies_data = companies_data
        self.icp_criteria = config['icp_criteria']
        self.qualified_leads = []
        
    def enrich_company_data(self) -> List[Dict]:
        """
        Enrich company data with additional information like revenue and employee count.
        In a production system, this would query external APIs or databases.
        
        Returns:
            List[Dict]: Enriched company data
        """
        logger.info("Enriching company data with size and revenue information")
        
        enriched_companies = []
        
        for company in tqdm(self.companies_data, desc="Enriching companies"):
            # In a real system, this would call APIs like:
            # - LinkedIn Sales Navigator
            # - ZoomInfo
            # - Crunchbase
            # - D&B Hoovers
            # For the prototype, we'll simulate this data
            
            enriched_company = company.copy()
            
            # Simulated revenue and employee data
            # In a real system, this would be fetched from external sources
            revenue_range, employee_count = self._get_company_size_data(company['name'])
            
            # Add enrichment data
            enriched_company['estimated_revenue'] = revenue_range
            enriched_company['employee_count'] = employee_count
            
            # Add keywords detected from company website/description
            enriched_company['keywords'] = self._detect_keywords(company['name'], company.get('industry', ''))
            
            enriched_companies.append(enriched_company)
        
        self.companies_data = enriched_companies
        logger.info(f"Enriched {len(enriched_companies)} companies with additional data")
        
        return enriched_companies
    
    def _get_company_size_data(self, company_name: str) -> Tuple[str, int]:
        """
        Get estimated revenue and employee count for a company.
        This is a mock function for the prototype.
        
        Args:
            company_name: Name of the company
            
        Returns:
            Tuple[str, int]: Revenue range and employee count
        """
        # Seed random with company name for consistent results
        random.seed(hash(company_name) % 1000)
        
        # Major companies in the industry - give them larger values
        major_companies = [
            "Avery Dennison Graphics Solutions",
            "3M Commercial Graphics",
            "HP Large Format Printing",
            "Mimaki",
            "Epson Professional Imaging",
            "Roland DGA"
        ]
        
        if company_name in major_companies:
            # Large companies
            revenue_options = [
                "$500M - $1B",
                "$1B - $5B",
                "$5B - $10B",
                "$10B+"
            ]
            revenue = random.choice(revenue_options)
            employees = random.randint(5000, 50000)
        else:
            # Smaller companies
            revenue_options = [
                "$10M - $50M",
                "$50M - $100M", 
                "$100M - $500M"
            ]
            revenue = random.choice(revenue_options)
            employees = random.randint(200, 5000)
        
        return revenue, employees
    
    def _detect_keywords(self, company_name: str, industry: str) -> List[str]:
        """
        Detect relevant keywords for a company.
        This is a mock function for the prototype.
        
        Args:
            company_name: Name of the company
            industry: Industry of the company
            
        Returns:
            List[str]: Detected keywords
        """
        # Seed random with company name for consistent results
        random.seed(hash(company_name) % 1000)
        
        # ICP keywords from config
        all_keywords = self.icp_criteria['keywords']
        
        # Industry-specific keywords
        industry_keyword_map = {
            "Signage and Graphics": ["outdoor signage", "digital printing", "graphics protection"],
            "Large Format Printing": ["large format", "high-quality prints", "UV protection"],
            "Vehicle Wraps": ["vehicle wraps", "fleet graphics", "weather-resistant"],
            "Architectural Graphics": ["building graphics", "durable graphics", "weather-resistant"],
            "Protective Films": ["protective films", "UV protection", "high-performance materials"],
            "Graphic Arts": ["graphic design", "printing solutions", "color management"],
            "Fleet Graphics": ["fleet branding", "vehicle graphics", "durable signage"],
            "Outdoor Advertising": ["billboards", "outdoor displays", "long-lasting signage"]
        }
        
        # Get industry-specific keywords
        industry_keywords = industry_keyword_map.get(industry, [])
        
        # Randomly select 3-6 keywords
        num_keywords = random.randint(3, 6)
        all_possible_keywords = all_keywords + industry_keywords
        
        # Make sure we don't try to sample more than we have
        num_keywords = min(num_keywords, len(all_possible_keywords))
        
        selected_keywords = random.sample(all_possible_keywords, num_keywords)
        
        return selected_keywords
    
    def score_and_qualify_leads(self) -> List[Dict]:
        """
        Score and qualify leads based on ICP criteria.
        
        Returns:
            List[Dict]: Qualified and scored leads
        """
        logger.info("Scoring and qualifying leads based on ICP criteria")
        
        qualified_leads = []
        
        for company in tqdm(self.companies_data, desc="Scoring companies"):
            # Calculate scores for different criteria
            industry_score = self._score_industry(company)
            size_score = self._score_company_size(company)
            keyword_score = self._score_keywords(company)
            engagement_score = self._score_engagement(company)
            
            # Calculate overall score (weighted average)
            overall_score = (
                industry_score * 0.35 +
                size_score * 0.25 +
                keyword_score * 0.20 +
                engagement_score * 0.20
            )
            
            # Determine if the lead is qualified (score >= 7.0)
            is_qualified = overall_score >= 7.0
            
            # Generate qualification rationale
            rationale = self._generate_qualification_rationale(
                company, 
                is_qualified,
                {
                    'industry_score': industry_score,
                    'size_score': size_score,
                    'keyword_score': keyword_score,
                    'engagement_score': engagement_score,
                    'overall_score': overall_score
                }
            )
            
            # Add scores and qualification status to company data
            scored_company = company.copy()
            scored_company.update({
                'industry_score': round(industry_score, 2),
                'size_score': round(size_score, 2),
                'keyword_score': round(keyword_score, 2),
                'engagement_score': round(engagement_score, 2),
                'overall_score': round(overall_score, 2),
                'is_qualified': is_qualified,
                'qualification_rationale': rationale
            })
            
            if is_qualified:
                qualified_leads.append(scored_company)
            
        # Sort leads by overall score
        qualified_leads.sort(key=lambda x: x['overall_score'], reverse=True)
        
        self.qualified_leads = qualified_leads
        logger.info(f"Identified {len(qualified_leads)} qualified leads out of {len(self.companies_data)} companies")
        
        return qualified_leads
    
    def _score_industry(self, company: Dict) -> float:
        """
        Score a company based on industry fit.
        
        Args:
            company: Company data
            
        Returns:
            float: Industry fit score (0-10)
        """
        target_industries = self.icp_criteria['industries']
        company_industry = company.get('industry', '')
        
        # Exact match
        if company_industry in target_industries:
            return 10.0
        
        # Partial match (check if any target industry is part of the company industry)
        for target in target_industries:
            if target.lower() in company_industry.lower():
                return 8.0
        
        # No match
        return 4.0
    
    def _score_company_size(self, company: Dict) -> float:
        """
        Score a company based on size (revenue and employees).
        
        Args:
            company: Company data with revenue and employee information
            
        Returns:
            float: Company size score (0-10)
        """
        # Extract employee count
        employee_count = company.get('employee_count', 0)
        
        # Extract revenue (for the prototype, we're using revenue ranges)
        revenue_str = company.get('estimated_revenue', '')
        
        # Convert revenue string to approximate value in millions
        revenue_value = 0
        if "$10B+" in revenue_str:
            revenue_value = 10000
        elif "$5B - $10B" in revenue_str:
            revenue_value = 7500
        elif "$1B - $5B" in revenue_str:
            revenue_value = 3000
        elif "$500M - $1B" in revenue_str:
            revenue_value = 750
        elif "$100M - $500M" in revenue_str:
            revenue_value = 300
        elif "$50M - $100M" in revenue_str:
            revenue_value = 75
        elif "$10M - $50M" in revenue_str:
            revenue_value = 30
        
        # Score based on employee count
        min_employees = self.icp_criteria['company_size']['min_employees']
        preferred_employees = self.icp_criteria['company_size']['preferred_employees']
        
        if employee_count >= preferred_employees:
            employee_score = 10.0
        elif employee_count >= min_employees:
            # Scale between 6.0 and 9.9 based on how close to preferred
            employee_score = 6.0 + 3.9 * (employee_count - min_employees) / (preferred_employees - min_employees)
        else:
            # Below minimum but not zero
            employee_score = max(3.0, 6.0 * employee_count / min_employees)
        
        # Score based on revenue
        min_revenue = self.icp_criteria['company_size']['min_revenue_usd'] / 1_000_000  # Convert to millions
        preferred_revenue = self.icp_criteria['company_size']['preferred_revenue_usd'] / 1_000_000  # Convert to millions
        
        if revenue_value >= preferred_revenue:
            revenue_score = 10.0
        elif revenue_value >= min_revenue:
            # Scale between 6.0 and 9.9 based on how close to preferred
            revenue_score = 6.0 + 3.9 * (revenue_value - min_revenue) / (preferred_revenue - min_revenue)
        else:
            # Below minimum but not zero
            revenue_score = max(3.0, 6.0 * revenue_value / min_revenue)
        
        # Combined score (weighted average)
        combined_score = (employee_score * 0.4) + (revenue_score * 0.6)
        
        return combined_score
    
    def _score_keywords(self, company: Dict) -> float:
        """
        Score a company based on keyword relevance.
        
        Args:
            company: Company data with detected keywords
            
        Returns:
            float: Keyword relevance score (0-10)
        """
        target_keywords = set(k.lower() for k in self.icp_criteria['keywords'])
        company_keywords = set(k.lower() for k in company.get('keywords', []))
        
        # Count matches
        matches = target_keywords.intersection(company_keywords)
        match_count = len(matches)
        
        # Calculate score based on number of matches
        if match_count >= 5:
            return 10.0
        elif match_count >= 3:
            return 8.0
        elif match_count >= 1:
            return 6.0
        else:
            return 4.0
    
    def _score_engagement(self, company: Dict) -> float:
        """
        Score a company based on event and association engagement.
        
        Args:
            company: Company data with event and association information
            
        Returns:
            float: Engagement score (0-10)
        """
        events = company.get('events', [])
        associations = company.get('associations', [])
        
        # Count events and association memberships
        event_count = len(events)
        association_count = len(associations)
        
        # Check for premium engagement
        premium_engagement = False
        for event in events:
            if event.get('sponsorship', False):
                premium_engagement = True
                break
                
        for assoc in associations:
            if assoc.get('membership_level', '').lower() in ['platinum', 'gold']:
                premium_engagement = True
                break
            
            if assoc.get('committee_participation', False):
                premium_engagement = True
                break
        
        # Calculate score
        if premium_engagement and event_count >= 2 and association_count >= 1:
            return 10.0
        elif premium_engagement and (event_count >= 1 or association_count >= 1):
            return 9.0
        elif event_count >= 2 and association_count >= 1:
            return 8.0
        elif event_count >= 2 or association_count >= 1:
            return 7.0
        elif event_count >= 1 or association_count >= 1:
            return 6.0
        else:
            return 4.0
    
    def _generate_qualification_rationale(self, company: Dict, is_qualified: bool, scores: Dict) -> str:
        """
        Generate qualification rationale based on scores.
        
        Args:
            company: Company data
            is_qualified: Whether the company is qualified
            scores: Score components
            
        Returns:
            str: Qualification rationale
        """
        company_name = company['name']
        
        if not is_qualified:
            return f"{company_name} does not meet DuPont Tedlar's ICP criteria (overall score: {scores['overall_score']:.1f}/10)."
        
        # Build rationale
        rationale_parts = []
        
        # Industry fit
        if scores['industry_score'] >= 9.0:
            rationale_parts.append(f"Strong industry alignment ({company.get('industry', 'Unknown industry')}).")
        elif scores['industry_score'] >= 7.0:
            rationale_parts.append(f"Good industry fit ({company.get('industry', 'Unknown industry')}).")
        
        # Company size
        revenue_str = company.get('estimated_revenue', 'Unknown revenue')
        employee_count = company.get('employee_count', 'Unknown')
        
        if scores['size_score'] >= 9.0:
            rationale_parts.append(f"Ideal company size ({revenue_str}, ~{employee_count} employees).")
        elif scores['size_score'] >= 7.0:
            rationale_parts.append(f"Suitable company size ({revenue_str}, ~{employee_count} employees).")
        
        # Keywords
        if scores['keyword_score'] >= 7.0:
            keywords = company.get('keywords', [])
            if keywords:
                keyword_str = ', '.join(keywords[:3])
                rationale_parts.append(f"Uses relevant technologies/approaches ({keyword_str}).")
        
        # Engagement
        events = company.get('events', [])
        associations = company.get('associations', [])
        
        engagement_points = []
        
        if events:
            event_names = [e['event_name'] for e in events[:2]]
            engagement_points.append(f"Attends key events ({', '.join(event_names)})")
            
            # Check for sponsorships
            sponsorships = [e['event_name'] for e in events if e.get('sponsorship', False)]
            if sponsorships:
                engagement_points.append(f"Sponsors {sponsorships[0]}")
        
        if associations:
            assoc_names = [a['association_name'] for a in associations[:1]]
            engagement_points.append(f"Member of {assoc_names[0]}")
            
            # Check for premium memberships
            premium = [a['association_name'] for a in associations 
                      if a.get('membership_level', '').lower() in ['platinum', 'gold']]
            if premium:
                engagement_points.append(f"{premium[0]} {next((a['membership_level'] for a in associations if a['association_name'] == premium[0]), '')} member")
        
        if engagement_points:
            rationale_parts.append(" and ".join(engagement_points) + ".")
        
        # Combine rationale
        full_rationale = " ".join(rationale_parts)
        
        return full_rationale
    
    def save_qualified_leads(self, output_file: str = 'data/qualified_leads.json') -> str:
        """
        Save qualified leads to a JSON file.
        
        Args:
            output_file: Path to save the qualified leads
            
        Returns:
            str: Path to the saved file
        """
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        save_json(self.qualified_leads, output_file)
        
        logger.info(f"Saved {len(self.qualified_leads)} qualified leads to {output_file}")
        
        return output_file


def run_lead_qualification(companies_file: str, config_path: str = 'config.yaml') -> str:
    """
    Run the lead qualification process.
    
    Args:
        companies_file: Path to the companies data file
        config_path: Path to the configuration file
        
    Returns:
        str: Path to the saved qualified leads file
    """
    config = load_config(config_path)
    companies_data = load_json(companies_file)
    
    qualifier = LeadQualifier(config, companies_data)
    
    # Enrich company data
    qualifier.enrich_company_data()
    
    # Score and qualify leads
    qualifier.score_and_qualify_leads()
    
    # Save qualified leads
    return qualifier.save_qualified_leads()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        companies_file = sys.argv[1]
    else:
        companies_file = 'data/companies.json'
    
    run_lead_qualification(companies_file)