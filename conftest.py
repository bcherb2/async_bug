
import pytest_asyncio
from loguru import logger
from api_client import DemoAPIClient

def pytest_configure(config):
    config.option.asyncio_mode = "auto"


@pytest_asyncio.fixture(scope="module")
async def api_client():
    """Fixture to provide an authenticated API client."""
    logger.info("Setting up API client")
    client = DemoAPIClient()
    
    try:
        await client.login()
        logger.info("API client logged in successfully")
        yield client
    finally:
        await client.close()
        logger.info("API client closed")


