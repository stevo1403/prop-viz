import os

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    BREVO_API_KEY = os.getenv("BREVO_API_KEY")

    if not OPENAI_API_KEY:
        raise EnvironmentError("Environment variable 'OPENAI_API_KEY' is not set.")
    if not GEMINI_API_KEY:
        raise EnvironmentError("Environment variable 'GEMINI_API_KEY' is not set.")
    if not BREVO_API_KEY:
        raise EnvironmentError("Environment variable 'BREVO_API_KEY' is not set.")

    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    PRIMARY_WEBSITE = os.getenv("PRIMARY_WEBSITE", "http://exposeprofi.de/")
    
    @classmethod
    def __repr__(cls):
        return f"Config(OPENAI_API_KEY='{cls.OPENAI_API_KEY}', GEMINI_API_KEY='{cls.GEMINI_API_KEY}', BREVO_API_KEY='{cls.BREVO_API_KEY}')"