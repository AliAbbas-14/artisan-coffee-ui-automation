import json
from typing import Any, Optional

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

class RedisReader:
    """
    Manages test data caching via Redis with automatic fallback to resilient in-memory
    cache to ensure tests run seamlessly on any workstation without requiring a Redis daemon.
    """

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0, password: Optional[str] = None):
        # Default fallback datasets seeded directly into memory cache
        self._memory_cache = {
            "cache:menu:signature": json.dumps([
                {"name": "Black Label Espresso", "price": "$4.50"},
                {"name": "Velvet Oat Latte", "price": "$5.50"},
                {"name": "Midnight Cold Brew", "price": "$6.00"}
            ]),
            "cache:blends:popular": json.dumps([
                {"blend": "ESPRESSO NOIR", "type": "Dark"},
                {"blend": "MORNING GOLD", "type": "Medium"},
                {"blend": "VELVET HOUR", "type": "Light"}
            ]),
            "test_data:login": json.dumps([
                {"username": "alimahi4540@gmail.com", "password": "customer123", "expected": "success"},
                {"username": "invalid@test.com", "password": "wrongpassword", "expected": "failure"}
            ]),
            "test_data:search": json.dumps([
                {"keyword": "Espresso", "category": "espresso", "min_results": 1},
                {"keyword": "Vanilla", "category": "latte", "min_results": 1}
            ])
        }
        self._client = None

        if REDIS_AVAILABLE:
            try:
                client = redis.Redis(
                    host=host,
                    port=port,
                    db=db,
                    password=password,
                    socket_connect_timeout=0.5,
                    decode_responses=True
                )
                client.ping()
                self._client = client
            except Exception:
                self._client = None

    def is_connected(self) -> bool:
        return self._client is not None

    def get(self, key: str) -> Optional[str]:
        if self._client:
            try:
                val = self._client.get(key)
                if val is not None:
                    return val
            except Exception:
                pass
        return self._memory_cache.get(key)

    def set(self, key: str, value: Any, expire_seconds: Optional[int] = None) -> None:
        val_str = json.dumps(value) if not isinstance(value, str) else value
        if self._client:
            try:
                self._client.set(key, val_str, ex=expire_seconds)
                return
            except Exception:
                pass
        self._memory_cache[key] = val_str

    def get_json(self, key: str) -> Optional[Any]:
        val = self.get(key)
        if val is not None:
            try:
                return json.loads(val)
            except Exception:
                return val
        return None
