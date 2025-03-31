# Configuration settings for the scraper

# Base URL of the website to scrape
BASE_URLS = {
    "gelbeseiten": "https://www.gelbeseiten.de",
}

# Headers to mimic a browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Timeout settings for requests (in seconds)
REQUEST_TIMEOUT = 10

# Maximum number of retries for failed requests
MAX_RETRIES = 3

# Delay between requests to avoid being blocked (in seconds)
REQUEST_DELAY = 2

# Logging configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(levelname)s - %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S",
}

# Proxy settings (if needed)
USE_PROXY = False
PROXY = {
    "http": "http://localhost:8080",
    "https": "https://localhost:8090",
}