import sqlite3
import os
from typing import List, Dict, Any, Optional

class DatabaseReader:
    """Fetches test data and validates database state using SQLite or relational DB."""

    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        if not os.path.exists(self.db_path):
            # Create or ensure directory exists
            os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Executes a SELECT query and returns rows as list of dicts."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def get_user_by_role(self, role: str) -> Optional[Dict[str, Any]]:
        """Fetches active test user credentials by role (e.g. 'ADMIN' or 'CUSTOMER')."""
        try:
            rows = self.execute_query(
                "SELECT email, name, role FROM User WHERE role = ? LIMIT 1",
                (role.upper(),)
            )
            return rows[0] if rows else None
        except Exception:
            # Fallback if table doesn't exist yet
            return None

    def get_products(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Fetches seeded products from Product table."""
        try:
            return self.execute_query("SELECT id, name, category, price FROM Product LIMIT ?", (limit,))
        except Exception:
            return []
