import os

from dotenv import load_dotenv

from phalanx.scrapers.lead_scraper import get_leads_from_gelbeseiten, save_leads_to_database
from phalanx.database.database import Session, create_tables
from phalanx.email_sender.email_generator import OpenAPIEmailGenerator, GeminiEmailGenerator
from phalanx.email_sender.email_sender import BrevoEmailClient

from phalanx.models.lead import Lead
from phalanx.models.email import Email

load_dotenv()

db_path = os.path.join(os.path.dirname(__file__), 'phalanx.db')

def main():
    
    create_tables()
    
    session = Session()
    
    # Scrape leads from GelbeSeiten and save them to the database
    # print("[+] Scraping leads from GelbeSeiten...")
    # _leads = get_leads_from_gelbeseiten()
    # print("[+] Saving leads to database...")
    # save_leads_to_database(_leads)

    leads = session.query(Lead).all()
    
    first_lead = leads[0]
    email_generator = GeminiEmailGenerator()
    print("Generating email content...")
    email_content = email_generator.generate_email(first_lead.to_dict())
    print(email_content)
    print("Generating email subject...")
    email_subject = email_generator.generate_email_subject(email_content, first_lead.name)
    
    print(email_subject)
    email_record = Email(
        lead=first_lead,
        source="google",
        subject=email_subject,
        content=email_content
    )
    session.add(email_record)
    session.commit()
    
    email_client = BrevoEmailClient()
    email_client.send_email(email_record)
    
    
    # for lead in leads:
        # print(f"Name: {lead.name}, Email: {lead.email}")

if __name__ == "__main__":
    main()
