"""
Main entry point for DuPont Tedlar Lead Generation.

This script orchestrates the entire lead generation process.
"""

import logging
import os
import sys
import time
from typing import Dict, List, Optional, Tuple

from src.data_collection import run_data_collection
from src.lead_qualification import run_lead_qualification
from src.stakeholder_finder import run_stakeholder_finder
from src.personalization import run_personalization_engine
from src.utils import load_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("tedlar_lead_gen.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def run_lead_generation_pipeline(config_path: str = 'config.yaml') -> str:
    """
    Run the complete lead generation pipeline.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        str: Path to the final output file
    """
    start_time = time.time()
    logger.info("Starting DuPont Tedlar lead generation pipeline")
    
    # Step 1: Data Collection
    logger.info("Step 1: Data Collection")
    events_file, companies_file = run_data_collection(config_path)
    logger.info(f"Data collection complete. Events: {events_file}, Companies: {companies_file}")
    
    # Step 2: Lead Qualification
    logger.info("Step 2: Lead Qualification")
    qualified_leads_file = run_lead_qualification(companies_file, config_path)
    logger.info(f"Lead qualification complete. Qualified leads: {qualified_leads_file}")
    
    # Step 3: Stakeholder Identification
    logger.info("Step 3: Stakeholder Identification")
    stakeholders_file = run_stakeholder_finder(qualified_leads_file, config_path)
    logger.info(f"Stakeholder identification complete. Stakeholders: {stakeholders_file}")
    
    # Step 4: Personalization
    logger.info("Step 4: Personalization")
    final_output_file = run_personalization_engine(stakeholders_file, config_path)
    logger.info(f"Personalization complete. Final output: {final_output_file}")
    
    # Pipeline complete
    elapsed_time = time.time() - start_time
    logger.info(f"Lead generation pipeline completed in {elapsed_time:.2f} seconds")
    
    return final_output_file

def main():
    """Main entry point."""
    # Parse command line arguments
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = 'config.yaml'
    
    # Run the pipeline
    output_file = run_lead_generation_pipeline(config_path)
    
    # Print success message
    print(f"\nDuPont Tedlar lead generation complete!")
    print(f"Final output file: {output_file}")
    print(f"To view the results, run the dashboard with: python -m dashboard.app")

if __name__ == "__main__":
    main()