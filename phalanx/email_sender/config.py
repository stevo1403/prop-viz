import os

class EmailConfig:
    SMTP_SERVER = os.getenv("SMTP_SERVER", "localhost")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "your_username")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your_password")

    SMTP_SENDER_EMAIL = os.getenv("SMTP_SENDER_EMAIL", "outreach@example.com")
    SMTP_SENDER_NAME = os.getenv("SMTP_SENDER_NAME", "Outreach Team")
    
    TEST_EMAIL_ADDR = os.getenv("TEST_EMAIL_ADDR", "team@propertyvisualizer.com")
    TEST_EMAIL_ADDR = os.getenv("TEST_EMAIL_ADDR", "ruslan.yeltsin@thefluent.org")
    TEST_EMAIL_NAME = os.getenv("TEST_EMAIL_NAME", "Property Visualizer Team")
    TEST_SENDER_NAME = os.getenv("TEST_SENDER_NAME", "Stephan Förtsch")
    TEST_SENDER_TITLE = os.getenv("TEST_SENDER_TITLE", "Managing Director")
    TEST_SENDER_COMPANY = os.getenv("TEST_SENDER_COMPANY", "Exposeprofi")
    TEST_SENDER_WEBSITE = os.getenv("TEST_SENDER_WEBSITE", "www.exposeprofi.de")
    
    @staticmethod
    def get_smtp_credentials():
        return {
            "server": EmailConfig.SMTP_SERVER,
            "port": EmailConfig.SMTP_PORT,
            "username": EmailConfig.SMTP_USERNAME,
            "password": EmailConfig.SMTP_PASSWORD,
            "email": EmailConfig.SMTP_SENDER_EMAIL,
            "name": EmailConfig.SMTP_SENDER_NAME,
        }
