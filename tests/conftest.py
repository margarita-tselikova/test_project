import pytest


@pytest.fixture(scope="session")
def base_url():
    """Test URL"""
    return 'http://127.0.0.1:5000/'
