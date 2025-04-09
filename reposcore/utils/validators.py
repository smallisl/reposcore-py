import re

# requests 설치 확인 및 자동 설치
try:
    import requests
except ImportError:
    import subprocess
    import sys
    print("requests 패키지가 설치되지 않아 설치를 시도합니다...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

def validate_repo_format(repo: str) -> bool:
    pattern = r'^[\w\-]+/[\w\-]+$'
    if re.fullmatch(pattern, repo):
        return True
    else:
        print("저장소 형식이 올바르지 않습니다. 'owner/repo' 형식으로 입력해주세요.")
        return False

def check_github_repo_exists(repo: str) -> bool:
     url = f"https://api.github.com/repos/{repo}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            print(f"GitHub 저장소 '{repo}'를 찾을 수 없습니다. (응답 코드: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"GitHub API 요청 중 오류가 발생했습니다: {e}")
        return False