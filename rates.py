# rates.py
import requests
import time

CACHE_TTL = 300

class RateFetcher:
    def __init__(self):
        self._cache = {}
        self._timestamp = {}

    def get_rates(self, base='USD'):
        now = time.time()
        if base in self._cache and now - self._timestamp.get(base, 0) < CACHE_TTL:
            return self._cache[base]
        url = f" https://v6.exchangerate-api.com/v6/742cfaf4804b5506d60b66dc/latest/USD"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        rates = data.get('rates', {}) or {}
        self._cache[base] = rates
        self._timestamp[base] = now
        return rates

    def get_symbols(self):
        try:
            resp = requests.get("https://api.exchangerate.host/symbols", timeout=10)
            resp.raise_for_status()
            data = resp.json()
            symbols = data.get("symbols", {})
            return sorted(symbols.keys())
        except Exception:
            return []