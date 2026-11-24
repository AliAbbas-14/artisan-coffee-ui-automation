import os

class Config:
    """Central configuration for UI Test Automation Framework."""
    # Target Application URL (defaults to the deployed live Vercel website)
    BASE_URL = os.getenv("BASE_URL", "https://coffee-nu-jade.vercel.app")
    
    # Browser options: chromium, firefox, webkit
    BROWSER_TYPE = os.getenv("BROWSER", "chromium").lower()
    
    # Execution mode: True for headless, False to watch browser UI
    HEADLESS = os.getenv("HEADLESS", "true").lower() in ("true", "1", "yes")
    
    # Default timeouts in milliseconds
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "30000"))
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "45000"))
    
    # Viewport resolution
    VIEWPORT_WIDTH = int(os.getenv("VIEWPORT_WIDTH", "1280"))
    VIEWPORT_HEIGHT = int(os.getenv("VIEWPORT_HEIGHT", "800"))
    
    # Data paths
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(ROOT_DIR, "data")
    EXCEL_FILE = os.path.join(DATA_DIR, "test_data.xlsx")
    DB_FILE = os.path.join(ROOT_DIR, "..", "dev.db")
    
    # Redis configuration
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
