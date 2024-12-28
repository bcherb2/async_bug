import pytest
import asyncio
from loguru import logger
from api_client import DemoAPIClient

async def ensure_task_context():
    """Helper to ensure we're in a task context."""
    if asyncio.current_task() is None:
        task = asyncio.create_task(asyncio.sleep(0))
        await task


@pytest.mark.asyncio
async def test_client_setup(api_client):
    """Test basic client setup."""
    logger.debug("Testing client setup")
    assert api_client._session_token is not None
    assert api_client._session is not None
    logger.debug("Client setup verified")


@pytest.mark.asyncio
async def test_get_post(api_client):
    """Test retrieving a post."""
    await ensure_task_context()  # Try to ensure task context
    
    try:
        response = await api_client.rest("/posts/1", "GET")
        assert response is not None
        assert "id" in response
        assert response["id"] == 1
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise


@pytest.mark.asyncio
async def test_create_post(api_client):
    """Test creating a new post."""
    await ensure_task_context()  # Try to ensure task context
    
    try:
        new_post = {
            "title": "Test Post",
            "body": "Test Content",
            "userId": 1
        }
        response = await api_client.rest("/posts", "POST", new_post)
        assert response is not None
        assert "id" in response
        assert response["title"] == "Test Post"
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise


async def main():
    """Main function to run tests directly without pytest."""
    logger.info("Starting direct test execution")

    client = DemoAPIClient()
    
    try:
        await client.login()
        logger.info("Client logged in")
        
        logger.info("Running test_client_setup")
        await test_client_setup(client)
        logger.info("Client setup test passed")
        
        logger.info("Running test_get_post")
        await test_get_post(client)
        logger.info("Get post test passed")
        
        logger.info("Running test_create_post")
        await test_create_post(client)
        logger.info("Create post test passed")
        
    except Exception as e:
        logger.error(f"Test execution failed: {str(e)}")
        raise
    finally:
        logger.info("Cleaning up client")
        await client.close()
        logger.info("Client closed")


if __name__ == "__main__":
    asyncio.run(main())