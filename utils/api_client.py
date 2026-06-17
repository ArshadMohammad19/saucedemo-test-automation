"""
Thin wrapper around `requests` for API tests.

Centralizing base_url, default headers, and logging here means API test
files only deal with endpoints and assertions, not HTTP plumbing.
"""
import requests

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class APIClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or settings.API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _full_url(self, endpoint: str) -> str:
        return f"{self.base_url}{endpoint}"

    def get(self, endpoint: str, params: dict | None = None, **kwargs) -> requests.Response:
        url = self._full_url(endpoint)
        logger.info("GET %s | params=%s", url, params)
        response = self.session.get(url, params=params, timeout=10, **kwargs)
        logger.info("Response %s | status=%s", url, response.status_code)
        return response

    def post(self, endpoint: str, json: dict | None = None, **kwargs) -> requests.Response:
        url = self._full_url(endpoint)
        logger.info("POST %s | body=%s", url, json)
        response = self.session.post(url, json=json, timeout=10, **kwargs)
        logger.info("Response %s | status=%s", url, response.status_code)
        return response

    def put(self, endpoint: str, json: dict | None = None, **kwargs) -> requests.Response:
        url = self._full_url(endpoint)
        logger.info("PUT %s | body=%s", url, json)
        response = self.session.put(url, json=json, timeout=10, **kwargs)
        logger.info("Response %s | status=%s", url, response.status_code)
        return response

    def patch(self, endpoint: str, json: dict | None = None, **kwargs) -> requests.Response:
        url = self._full_url(endpoint)
        logger.info("PATCH %s | body=%s", url, json)
        response = self.session.patch(url, json=json, timeout=10, **kwargs)
        logger.info("Response %s | status=%s", url, response.status_code)
        return response

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        url = self._full_url(endpoint)
        logger.info("DELETE %s", url)
        response = self.session.delete(url, timeout=10, **kwargs)
        logger.info("Response %s | status=%s", url, response.status_code)
        return response
