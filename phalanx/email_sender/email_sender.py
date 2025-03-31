from datetime import datetime

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from phalanx.database.database import Session
from phalanx.email_sender.config import EmailConfig
from phalanx.models.email import Email
from phalanx.config import Config

class BrevoEmailClient:
    def __init__(self): 
        self.api_key = Config.BREVO_API_KEY
        
        if not self.api_key:
            raise ValueError("Brevo API key is missing.")
        
        # Configure API client
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = self.api_key
        
        # Create an instance of the API class
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    
    def send_email(self, email: Email):
        
        session = Session()
        
        html_content = email.content
        subject = email.subject
        
        lead = email.lead
        if not lead:
            raise ValueError(f"Email with ID {email.id} does not have a valid lead.")
        
        to_email = lead.email
        to_name = lead.name
        
        if Config.ENVIRONMENT == "development":
            to_email = EmailConfig.TEST_EMAIL_ADDR
            to_name = EmailConfig.TEST_EMAIL_NAME
                
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[
                {
                    "email": to_email, "name": to_name
                }
            ],
            sender={
                "email": EmailConfig.SMTP_SENDER_EMAIL, "name": EmailConfig.SMTP_SENDER_NAME
            },
            subject=subject,
            html_content=html_content
        )
        
        try:
            response = self.api_instance.send_transac_email(send_smtp_email)
            
            email.is_sent = True
            email.sent_with = "Brevo"
            email.sent_at = datetime.now()
            email.sent_successfully = True
            
            session.add(email)
            session.commit()
            print(f"✅ Email sent! Message ID: {response['messageId']}")
            return response
        except ApiException as e:
            print(f"❌ Error sending email: {e}")
            
            email.is_sent = False
            email.sent_with = "Brevo"
            email.sent_at = datetime.now()
            email.sent_successfully = False
            email.sent_error = str(e)
            
            session.add(email)
            session.commit()
            return None
