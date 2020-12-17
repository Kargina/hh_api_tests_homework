import pytest
import requests
import os
import logging

API_ENDPOINT = "https://api.hh.ru"

class ApiClient:
    def __init__(self, base_address):
        self.base_address = base_address
        self.api_key = os.getenv("HH_API_TOKEN", "")

    def get(self, path="/", params=None):
        url = f"{self.base_address}{path}"
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        return requests.get(url=url, params=params, headers=headers)

@pytest.fixture
def hh_api():
    return ApiClient(base_address=API_ENDPOINT)