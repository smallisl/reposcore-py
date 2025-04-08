import requests
import time


def retry_request(session: requests.Session, url: str, max_retries: int = 3, retry_delay: float = 1, params=None, headers=None) -> requests.Response:
    """
    주어진 URL에 대해 최대 max_retries 횟수만큼 요청을 재시도합니다.
    """
    response = None
    for i in range(max_retries):
        response = session.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response
        elif i < max_retries - 1:
            time.sleep(retry_delay)

    return response
