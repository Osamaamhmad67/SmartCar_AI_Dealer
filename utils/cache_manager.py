"""
utils/cache_manager.py - Simple Cache Management
SmartCar AI-Dealer
"""

class CacheManager:
    """
    A simple cache manager class to handle temporary data storage.
    """
    def __init__(self):
        self._cache = {}

    def get(self, key, default=None):
        return self._cache.get(key, default)

    def set(self, key, value):
        self._cache[key] = value

    def clear(self):
        self._cache.clear()