import aiohttp
import uuid
import json
from enum import Enum
from typing import Optional, Dict, Any
from loguru import logger


class RetCode(Enum):
    NO_ERROR = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404


class DemoAPIClient:
    """Demo REST client that simulates behavior similar to ANTServerRESTClient."""
    
    def __init__(
        self,
        base_url: str = "https://jsonplaceholder.typicode.com",
        timeout: int = 30
    ):
        """Initialize the API client.
        
        Args:
            base_url: Base URL for the API
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.timeout = timeout
        
        # Session management
        self._session: Optional[aiohttp.ClientSession] = None
        self._session_token: Optional[str] = None

    async def _ensure_session(self) -> aiohttp.ClientSession:
        """Ensure we have an active session, creating one if necessary."""
        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector(force_close=True)  
            self._session = aiohttp.ClientSession(
                connector=connector,
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
        return self._session

    async def close(self) -> None:
        """Close the client session."""
        if self._session:
            await self._session.close()
            self._session = None
            logger.debug("Session closed")

    async def login(self) -> None:
        """Simulate login by making a test request."""
        try:

            test_url = f"{self.base_url}/posts/1"
            session = await self._ensure_session()
            
            async with session.get(test_url) as response:
                if response.status != 200:
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=f"Login failed with status {response.status}"
                    )
                
                # Simulate session token
                self._session_token = str(uuid.uuid4())
                logger.info("Successfully logged in to API")
                
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            raise

    async def rest(
        self,
        endpoint: str,
        method: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a REST request.
        
        Args:
            endpoint: The endpoint path (e.g., '/posts')
            method: HTTP method (GET, POST, etc.)
            data: Optional request body data
            
        Returns:
            Dict containing the parsed response data
        """
        if not self._session_token:
            raise RuntimeError("Not logged in. Call login() first")
            
        session = await self._ensure_session()
        request_id = str(uuid.uuid4())[:8]
        url = f"{self.base_url}{endpoint}"

        try:
            logger.debug(f"[{request_id}] {method} {url}")
            if data:
                logger.debug(f"[{request_id}] Request body: {data}")

            headers = {"Authorization": f"Bearer {self._session_token}"}
            
            async with session.request(
                method=method,
                url=url,
                json=data,
                headers=headers
            ) as response:
                response_text = await response.text()
                logger.debug(f"[{request_id}] Response: {response_text}")
                
                if response.status >= 400:
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=f"Request failed: {response_text}"
                    )
                    
                return json.loads(response_text)

        except Exception as e:
            logger.error(f"[{request_id}] Request failed: {str(e)}")
            raise

