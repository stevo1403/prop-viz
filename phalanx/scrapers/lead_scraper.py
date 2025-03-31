from typing import List, Dict

from phalanx.scrapers.gelbeseiten import GelbeSeitenScraper
from phalanx.database.database import Session
from phalanx.models.lead import Lead

def get_leads_from_gelbeseiten() -> List[Dict[str, str]]:
    """
    Scrapes leads for specific job categories from the GelbeSeiten website.
    This function uses the `GelbeSeitenScraper` class to scrape contact information
    for businesses in specified job categories across Germany ("bundesweit").
    The results are aggregated into a single list of leads.
    Returns:
        list: A list of leads scraped from the GelbeSeiten website. Each lead
        is expected to be a dictionary or object containing the scraped data.
    """
    jobs = ["bauunternehmen", "immobilien"]

    leads = []
    
    for job in jobs:
        scraper = GelbeSeitenScraper(job, "bundesweit")
        results = scraper.scrape()
        
        leads.extend(results)
    
    return leads

def save_leads_to_database(leads: List[Dict[str, str]]) -> None:
    """
    Save a list of leads to the database.
    Args:
        leads (list): A list of leads to save to the database. Each lead
        is expected to be a dictionary or object containing the lead data.
    """
    
    session = Session()
    
    for lead_data in leads:
        # Standardize the email
        email = lead_data.get("email")
        if email:
            email = email.strip().lower()
        
        # Check if a lead with the same email already exists
        existing_lead = session.query(Lead).filter_by(email=email).first()
        if existing_lead:
            continue  # Skip adding this lead if it already exists
        
        lead = Lead(
            name=lead_data.get("business_name"),
            email=email,
            phone=lead_data.get("phone"),
            website=lead_data.get("website"),
            address=lead_data.get("address"),
            source="GelbeSeiten",
        )
        session.add(lead)
    
    session.commit()

