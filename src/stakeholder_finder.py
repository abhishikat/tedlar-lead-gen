"""
Stakeholder Finder Module for DuPont Tedlar Lead Generation

This module handles identifying key decision-makers at qualified companies.
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

class StakeholderFinder:
    """Identifies key decision-makers at qualified companies."""
    
    def __init__(self, config: Dict, qualified_leads: List[Dict]):
        self.config = config
        self.qualified_leads = qualified_leads
        self.target_titles = config['icp_criteria']['decision_makers']['titles']
        self.companies_with_stakeholders = []
        
    def find_stakeholders(self) -> List[Dict]:
        """
        Find stakeholders for qualified companies.
        In a production system, this would query LinkedIn Sales Navigator or similar.
        
        Returns:
            List[Dict]: Companies with stakeholder information
        """
        logger.info("Finding stakeholders for qualified companies")
        
        companies_with_stakeholders = []
        
        for company in tqdm(self.qualified_leads, desc="Finding stakeholders"):
            # In a real system, this would call LinkedIn Sales Navigator API
            # or similar service to find actual stakeholders
            # For the prototype, we'll generate mock stakeholders
            
            company_with_stakeholders = company.copy()
            stakeholders = self._mock_find_stakeholders(company['name'])
            company_with_stakeholders['stakeholders'] = stakeholders
            
            companies_with_stakeholders.append(company_with_stakeholders)
        
        self.companies_with_stakeholders = companies_with_stakeholders
        logger.info(f"Found stakeholders for {len(companies_with_stakeholders)} companies")
        
        return companies_with_stakeholders
    
    def _mock_find_stakeholders(self, company_name: str) -> List[Dict]:
        """
        Generate mock stakeholders for a company.
        In a production system, this would be real data from LinkedIn Sales Navigator.
        
        Args:
            company_name: Name of the company
            
        Returns:
            List[Dict]: Mock stakeholder data
        """
        # Seed random with company name for consistent results
        random.seed(hash(company_name) % 1000)
        
        # Sample first and last names for generating stakeholders
        first_names = [
            "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", 
            "Linda", "William", "Elizabeth", "David", "Susan", "Richard", "Jessica", 
            "Joseph", "Sarah", "Thomas", "Karen", "Charles", "Nancy", "Christopher", 
            "Lisa", "Daniel", "Margaret", "Matthew", "Betty", "Anthony", "Sandra", 
            "Mark", "Ashley", "Donald", "Dorothy", "Steven", "Kimberly", "Andrew", 
            "Emily", "Paul", "Donna", "Joshua", "Michelle", "Kenneth", "Carol"
        ]
        
        last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", 
            "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", 
            "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", 
            "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", 
            "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", 
            "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green", 
            "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell"
        ]
        
        # Generate 2-3 stakeholders per company
        num_stakeholders = random.randint(2, 3)
        stakeholders = []
        
        # Get a sample of target titles
        selected_titles = random.sample(self.target_titles, min(num_stakeholders, len(self.target_titles)))
        
        for i in range(num_stakeholders):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            title = selected_titles[i] if i < len(selected_titles) else random.choice(self.target_titles)
            
            # Generate a LinkedIn-style URL
            linkedin_url = f"https://www.linkedin.com/in/{first_name.lower()}-{last_name.lower()}-{random.randint(100000, 999999)}"
            
            # Generate seniority and department
            departments = ["Product Development", "R&D", "Innovation", "Procurement", "Technical", "Marketing"]
            department = random.choice(departments)
            
            # Generate years at company
            years_at_company = random.randint(1, 15)
            
            # Generate location
            locations = ["New York, NY", "San Francisco, CA", "Chicago, IL", "Boston, MA", 
                         "Austin, TX", "Seattle, WA", "Denver, CO", "Atlanta, GA", 
                         "Dallas, TX", "Los Angeles, CA", "Miami, FL", "Philadelphia, PA"]
            location = random.choice(locations)
            
            # Create stakeholder entry
            stakeholder = {
                "name": f"{first_name} {last_name}",
                "title": title,
                "department": department,
                "years_at_company": years_at_company,
                "location": location,
                "linkedin_url": linkedin_url,
                "email": f"{first_name.lower()}.{last_name.lower()}@{company_name.lower().replace(' ', '')}.com",
                "relevance_score": round(random.uniform(7.5, 9.8), 1)  # Only high relevance stakeholders
            }
            
            stakeholders.append(stakeholder)
        
        # Sort by relevance score
        stakeholders.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return stakeholders
    
    def evaluate_stakeholders(self) -> List[Dict]:
        """
        Evaluate stakeholders based on their potential value to DuPont Tedlar.
        
        Returns:
            List[Dict]: Companies with evaluated stakeholders
        """
        logger.info("Evaluating stakeholders for alignment with DuPont Tedlar's ICP")
        
        companies_with_evaluated_stakeholders = []
        
        for company in tqdm(self.companies_with_stakeholders, desc="Evaluating stakeholders"):
            company_with_evaluated = company.copy()
            evaluated_stakeholders = []
            
            for stakeholder in company['stakeholders']:
                evaluated = stakeholder.copy()
                
                # Evaluate title match
                title_match_score = self._score_title_match(stakeholder['title'])
                evaluated['title_match_score'] = round(title_match_score, 2)
                
                # Evaluate stakeholder seniority
                seniority_score = self._score_seniority(stakeholder['title'])
                evaluated['seniority_score'] = round(seniority_score, 2)
                
                # Calculate overall score
                overall_score = (title_match_score * 0.7) + (seniority_score * 0.3)
                evaluated['overall_score'] = round(overall_score, 2)
                
                # Generate interest areas based on title and department
                evaluated['interest_areas'] = self._generate_stakeholder_interests(
                    stakeholder['title'], stakeholder['department']
                )
                
                evaluated_stakeholders.append(evaluated)
            
            # Sort stakeholders by overall score
            evaluated_stakeholders.sort(key=lambda x: x['overall_score'], reverse=True)
            company_with_evaluated['stakeholders'] = evaluated_stakeholders
            
            companies_with_evaluated_stakeholders.append(company_with_evaluated)
        
        self.companies_with_stakeholders = companies_with_evaluated_stakeholders
        return companies_with_evaluated_stakeholders
    
    def _score_title_match(self, title: str) -> float:
        """
        Score how well a stakeholder's title matches the target titles.
        
        Args:
            title: Stakeholder's title
            
        Returns:
            float: Title match score (0-10)
        """
        # Convert title and target titles to lowercase for comparison
        title_lower = title.lower()
        
        # Check for exact matches
        for target_title in self.target_titles:
            if target_title.lower() == title_lower:
                return 10.0
        
        # Check for partial matches
        for target_title in self.target_titles:
            target_lower = target_title.lower()
            
            # Check for key terms in both directions
            key_terms = target_lower.split()
            title_terms = title_lower.split()
            
            matches = sum(1 for term in key_terms if term in title_lower)
            
            if matches / len(key_terms) >= 0.5:
                return 8.0 + (matches / len(key_terms)) * 2.0
        
        # Check for role-related keywords
        keywords = [
            "product", "innovation", "r&d", "research", "development",
            "procurement", "purchasing", "technical", "technology",
            "graphics", "signage", "materials", "production"
        ]
        
        keyword_matches = sum(1 for kw in keywords if kw in title_lower)
        if keyword_matches > 0:
            return 5.0 + (keyword_matches / len(keywords)) * 3.0
        
        # Default score
        return 5.0
    
    def _score_seniority(self, title: str) -> float:
        """
        Score a stakeholder's seniority level.
        
        Args:
            title: Stakeholder's title
            
        Returns:
            float: Seniority score (0-10)
        """
        title_lower = title.lower()
        
        # Executive level
        if any(term in title_lower for term in ["ceo", "cto", "cio", "cfo", "president", "chief"]):
            return 10.0
        
        # VP level
        if "vp" in title_lower or "vice president" in title_lower:
            return 9.0
        
        # Director level
        if "director" in title_lower:
            return 8.0
        
        # Manager level
        if "manager" in title_lower or "head of" in title_lower:
            return 7.0
        
        # Default score
        return 6.0
    
    def _generate_stakeholder_interests(self, title: str, department: str) -> List[str]:
        """
        Generate likely interest areas for a stakeholder based on title and department.
        
        Args:
            title: Stakeholder's title
            department: Stakeholder's department
            
        Returns:
            List[str]: Likely interest areas
        """
        # Seed random with title and department for consistent results
        random.seed(hash(title + department) % 1000)
        
        # Potential interest areas
        potential_interests = {
            "Product Development": [
                "new material technologies", 
                "product performance improvements",
                "sustainability features",
                "protective film applications",
                "extended product lifecycle"
            ],
            "R&D": [
                "material innovation", 
                "UV resistance technologies",
                "weatherproofing advances",
                "durability testing",
                "advanced polymers"
            ],
            "Innovation": [
                "next-generation materials", 
                "sustainable solutions",
                "material science breakthroughs",
                "advanced coatings",
                "environmental protection"
            ],
            "Procurement": [
                "cost reduction", 
                "supplier reliability",
                "long-term partnerships",
                "material consistency",
                "simplified supply chain"
            ],
            "Technical": [
                "technical specifications", 
                "application methods",
                "integration with existing systems",
                "testing protocols",
                "performance metrics"
            ],
            "Marketing": [
                "market differentiation", 
                "product positioning",
                "competitive advantages",
                "customer satisfaction",
                "value propositions"
            ]
        }
        
        # Get interests based on department
        department_interests = potential_interests.get(department, [])
        
        # Add title-based interests
        title_lower = title.lower()
        title_interests = []
        
        if "product" in title_lower:
            title_interests.extend(["product innovation", "material performance"])
        
        if "innovation" in title_lower or "r&d" in title_lower:
            title_interests.extend(["cutting-edge materials", "research collaboration"])
        
        if "technical" in title_lower:
            title_interests.extend(["technical specifications", "implementation support"])
        
        if "procurement" in title_lower or "purchasing" in title_lower:
            title_interests.extend(["vendor consolidation", "quality consistency"])
        
        # Combine and select random subset of interests
        all_interests = list(set(department_interests + title_interests))
        num_interests = min(4, len(all_interests))
        
        return random.sample(all_interests, num_interests)
    
    def save_stakeholders(self, output_file: str = 'data/stakeholders.json') -> str:
        """
        Save stakeholder data to a JSON file.
        
        Args:
            output_file: Path to save the stakeholder data
            
        Returns:
            str: Path to the saved file
        """
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        save_json(self.companies_with_stakeholders, output_file)
        
        logger.info(f"Saved stakeholder data for {len(self.companies_with_stakeholders)} companies to {output_file}")
        
        return output_file


def run_stakeholder_finder(qualified_leads_file: str, config_path: str = 'config.yaml') -> str:
    """
    Run the stakeholder finder process.
    
    Args:
        qualified_leads_file: Path to the qualified leads data file
        config_path: Path to the configuration file
        
    Returns:
        str: Path to the saved stakeholder data file
    """
    config = load_config(config_path)
    qualified_leads = load_json(qualified_leads_file)
    
    finder = StakeholderFinder(config, qualified_leads)
    
    # Find stakeholders
    finder.find_stakeholders()
    
    # Evaluate stakeholders
    finder.evaluate_stakeholders()
    
    # Save stakeholder data
    return finder.save_stakeholders()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        qualified_leads_file = sys.argv[1]
    else:
        qualified_leads_file = 'data/qualified_leads.json'
    
    run_stakeholder_finder(qualified_leads_file)