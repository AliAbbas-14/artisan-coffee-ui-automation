import os
from typing import Dict, Any, List
from config.config import Config
from data.excel_reader import ExcelReader
from data.db_reader import DatabaseReader
from data.redis_reader import RedisReader

class DataManager:
    """Unified Facade pattern for fetching test data across Excel, Database, and Redis."""

    def __init__(self):
        self.excel_file = Config.EXCEL_FILE
        self.db_file = Config.DB_FILE
        self.excel = ExcelReader(self.excel_file) if os.path.exists(self.excel_file) else None
        self.db = DatabaseReader(self.db_file)
        self.redis = RedisReader(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            password=Config.REDIS_PASSWORD
        )

    def get_login_data(self, source: str = "excel") -> List[Dict[str, Any]]:
        """Fetch login test datasets from specified data source."""
        source = source.lower()
        if source == "excel":
            if not self.excel:
                raise FileNotFoundError("Excel test data file not initialized.")
            return self.excel.read_sheet_as_dicts("LoginData")
        elif source == "db" or source == "database":
            users = self.db.execute_query("SELECT email, role FROM User")
            return [{"username": u["email"], "password": "customer123" if u["role"] == "CUSTOMER" else "admin123", "expected": "success"} for u in users]
        elif source == "redis":
            cached = self.redis.get_json("test_data:login")
            return cached if cached else []
        else:
            raise ValueError(f"Unsupported data source: {source}")

    def get_search_data(self, source: str = "excel") -> List[Dict[str, Any]]:
        """Fetch search test scenarios from specified data source."""
        source = source.lower()
        if source == "excel":
            if not self.excel:
                raise FileNotFoundError("Excel test data file not initialized.")
            return self.excel.read_sheet_as_dicts("SearchData")
        elif source == "redis":
            cached = self.redis.get_json("test_data:search")
            return cached if cached else []
        elif source == "db" or source == "database":
            products = self.db.get_products(limit=5)
            return [{"keyword": p["name"], "category": p["category"], "min_results": "1"} for p in products]
        else:
            raise ValueError(f"Unsupported data source: {source}")

    def cache_session_token(self, token: str, user_email: str) -> None:
        """Stores session in Redis cache for data-driven sessions."""
        self.redis.set(f"session:{user_email}", token, expire_seconds=3600)
