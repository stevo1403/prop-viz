import re
from typing import Dict

import requests
import openai
from openai import OpenAI
from google import genai
from google.genai import types

from phalanx.config import Config
from phalanx.email_sender.config import EmailConfig

def is_website_reachable(website_url: str) -> bool:
    """Checks if a website is reachable."""
    try:
        response = requests.head(website_url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False
class OpenAPIEmailGenerator:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        self.client = OpenAI()

    def generate_email(self, lead_data: Dict[str, str]):
        
        """Generates a personalized cold email for a real estate lead using OpenAI API."""
        
        lead_website = lead_data.get('website', 'Nicht verfügbar')
        if lead_website == 'Nicht verfügbar' or not is_website_reachable(lead_website):
            prompt = f"""
            Erstelle eine personalisierte Cold-Email auf Deutsch für {lead_data.get('name', 'Ihr Unternehmen')}.

            - Adresse: {lead_data.get('address', 'Nicht verfügbar')}
            - Telefonnummer: {lead_data.get('phone', 'Nicht verfügbar')}
            - Website: {lead_website}
            - Zusätzliche Infos: {lead_data.get('further_info', 'Nicht verfügbar')}

            **E-Mail-Anforderungen:**  
            - Begrüßung mit Firmenname  
            - Erwähne relevante Informationen wie Adresse oder Dienstleistungen, falls verfügbar  
            - Zeige auf, wie die Dienstleistungen von {Config.PRIMARY_WEBSITE} ihnen helfen können  
            - Füge einen Call-to-Action hinzu (z. B. Terminvereinbarung)  
            - Schließe mit einer professionellen Signatur  

            **Hinweis:** Die Nachricht soll freundlich, professionell und überzeugend sein.
            """
        else:
            prompt = f"""
            Erstelle eine personalisierte Cold-Email auf Deutsch für {lead_data.get('name', 'Ihr Unternehmen')}.

            - Adresse: {lead_data.get('address', 'Nicht verfügbar')}
            - Telefonnummer: {lead_data.get('phone', 'Nicht verfügbar')}
            - Website: {lead_website}
            - Zusätzliche Infos: {lead_data.get('further_info', 'Nicht verfügbar')}

            **E-Mail-Anforderungen:**  
            - Begrüßung mit Firmenname  
            - Erwähne relevante Informationen wie Adresse oder Dienstleistungen, falls verfügbar  
            - Zeige auf, wie die Dienstleistungen von {Config.PRIMARY_WEBSITE} speziell für Unternehmen wie {lead_website} hilfreich sein können  
            - Füge einen Call-to-Action hinzu (z. B. Terminvereinbarung)  
            - Schließe mit einer professionellen Signatur  

            **Hinweis:** Die Nachricht soll freundlich, professionell und überzeugend sein.
            """

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "Du bist ein professioneller deutscher Vertriebsassistent."},
                {"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        return response["choices"][0]["message"]["content"]

    def generate_email_subject(self, email_content, business_name):
        """Generates a subject line for a cold email using OpenAI API."""
        
        prompt = f"""
        Erstelle eine Betreffzeile für eine Cold-Email für {business_name}.
        
        **Anforderungen:**  
        - Betreffzeile sollte auf den Inhalt der E-Mail hinweisen
        - Betreffzeile sollte Interesse wecken und zum Öffnen der E-Mail anregen
        - Betreffzeile sollte kurz und prägnant sein
        
        **E-Mail-Inhalt:**
        {email_content}
        """

        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": "Du bist ein professioneller deutscher Vertriebsassistent."},
                    {"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        return response["choices"][0]["message"]["content"]
    
class GeminiEmailGenerator:
    def __init__(self):
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)

    def is_website_reachable(self, website_url: str) -> bool:
        """Checks if a website is reachable."""
        try:
            response = requests.head(website_url, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def __clean_email(self, email: str) -> str:
        email = re.sub(r"(?i)^Subject:\s*", "", email).strip()
        email = re.sub(r"\[.*?\]", "", email).strip()
        email = email.replace("`", "").strip()
        return email.strip()
    
    def generate_email(self, lead_data: Dict[str, str]):
        """Generates a personalized cold email for a real estate lead using Gemini API."""
        
        lead_website = lead_data.get('website', 'Nicht verfügbar')
        prompt = f"""
        Create a straightforward personalized cold email in German to be sent to {lead_data.get('name', 'your company')}.
        
        Format: You can html format the email
        
        Language: Email should be in German
        **Instruction:** The message should be friendly, professional, and persuasive. Don't add empty placeholders like "[Your Name]" or "[Your XXXXX]"
        
        Language: Email should be in German
        Format: You can html format the email
        - The company is located at: `{lead_data.get('address', 'Not available')}`
        - the company's phone number is : `{lead_data.get('phone', 'Not available')}`
        - You can retrieve information about the company's products from its website: `{lead_website}`
        - You can also get additional info about the company from: `{lead_data.get('further_info', 'Not available')}`
        
        **Email Requirements:**  
        - Greeting with company name  
        - Mention relevant information such as address or services, if available  
        - Highlight how the services of my company(`{Config.PRIMARY_WEBSITE}`) can help them  
        - Include a call-to-action (e.g., schedule an appointment)
        - End with: 
            `Kind regards,
            {EmailConfig.TEST_SENDER_NAME}
            {EmailConfig.TEST_SENDER_TITLE}
            {EmailConfig.TEST_SENDER_COMPANY}
            {EmailConfig.TEST_SENDER_WEBSITE}`
        
        Language: Email should be in German
        Format: You can html format the email
        """
    
        response = self.client.models.generate_content(
            model='gemini-2.0-flash-thinking-exp-01-21', contents=prompt,
        )
        
        return self.__clean_email(response.text)

    def generate_email_subject(self, email_content, business_name):
        """Generates a subject line for a cold email using Gemini API."""
        
        prompt = f"""
        Create a subject line for a cold email for `{business_name}`. Return only one line
        
        Language: Email subject should be in German
        
        **Requirements:**  
        - The subject line should reflect the content of the email
        - The subject line should spark interest and encourage opening the email
        - The subject line should be short and concise
        
        Language: Email subject should be in German
        
        **Email Content:**
        `{email_content}`
        """

        response = self.client.models.generate_content(
            model='gemini-2.0-flash', contents=prompt,
        )
        
        return response.text