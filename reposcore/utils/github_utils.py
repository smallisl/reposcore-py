import requests
import logging

def check_github_repo_exists(repo: str, bypass: bool = False) -> bool:
    """
    GitHub 저장소 존재 여부를 확인하는 함수.

    - bypass=True인 경우: 무조건 True 반환 (테스트용).
    - bypass=False인 경우: 실제 GitHub API로 확인.
    """
    if bypass:
        logging.warning("⚠️ [TEST MODE] check_github_repo_exists()는 항상 True를 반환합니다. 실제 검사는 수행되지 않습니다.")
        return True

    url = f"https://api.github.com/repos/{repo}"
    response = requests.get(url)

    if response.status_code == 200:
        return True
    elif response.status_code == 403:
        logging.warning("⚠️ GitHub API 요청 실패: 403 (요청 횟수 초과 또는 인증 오류)")
        logging.info("ℹ️ 해결 방법: --token 옵션 또는 GITHUB_TOKEN 환경 변수 사용")
    elif response.status_code == 404:
        logging.warning(f"⚠️ 저장소 '{repo}'가 존재하지 않습니다.")
    else:
        logging.warning(f"⚠️ 요청 실패: HTTP 상태 코드 {response.status_code}")

    return False
