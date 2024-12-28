* Install Python 3.12 (I used uv, to be specific)
* install packages with `pip install .` or `uv sync`
* verify that tests can be passed by running `python test_api_client.py`

the results should look something like this:

```bash
2024-12-28 04:36:06.352 | INFO     | __main__:main:72 - Client setup test passed
2024-12-28 04:36:06.352 | INFO     | __main__:main:74 - Running test_get_post
2024-12-28 04:36:06.352 | DEBUG    | api_client:rest:102 - [108a1529] GET https://jsonplaceholder.typicode.com/posts/1
2024-12-28 04:36:06.412 | DEBUG    | api_client:rest:115 - [108a1529] Response: {
  "userId": 1,
  "id": 1,
  ...
  ```

  * now, run `pytest -s test_api_client.py`, which should fail like:

  ```bash
  2024-12-28 04:37:14.504 | INFO     | api_client:login:72 - Successfully logged in to API
2024-12-28 04:37:14.504 | INFO     | conftest:api_client:18 - API client logged in successfully
2024-12-28 04:37:14.505 | DEBUG    | test_api_client:test_client_setup:16 - Testing client setup
2024-12-28 04:37:14.505 | DEBUG    | test_api_client:test_client_setup:19 - Client setup verified
.2024-12-28 04:37:14.506 | DEBUG    | api_client:rest:102 - [6334b1a7] GET https://jsonplaceholder.typicode.com/posts/1
2024-12-28 04:37:14.506 | ERROR    | api_client:rest:128 - [6334b1a7] Request failed: Timeout context manager should be used inside a task
2024-12-28 04:37:14.506 | ERROR    | test_api_client:test_get_post:33 - Test failed: Timeout context manager should be used inside a task
F2024-12-28 04:37:14.536 | DEBUG    | api_client:rest:102 - [2e5424e3] POST https://jsonplaceholder.typicode.com/posts
2024-12-28 04:37:14.537 | DEBUG    | api_client:rest:104 - [2e5424e3] Request body: {'title': 'Test Post', 'body': 'Test Content', 'userId': 1}
2024-12-28 04:37:14.537 | ERROR    | api_client:rest:128 - [2e5424e3] Request failed: Timeout context manager should be used inside a task
2024-12-28 04:37:14.537 | ERROR    | test_api_client:test_create_post:53 - Test failed: Timeout context manager should be used inside a task
F2024-12-28 04:37:14.556 | DEBUG    | api_client:close:52 - Session closed
2024-12-28 04:37:14.556 | INFO     | conftest:api_client:22 - API client closed
```