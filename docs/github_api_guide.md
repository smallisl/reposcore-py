## 1. **GitHub API란?**

GitHub에서 제공하는 공식 API로, GitHub의 저장소, 이슈, PR(Pull Request), 커밋 등 다양한 정보를 코드로 가져오거나 조작할 수 있게 해줍니다.

- 공식 문서: https://docs.github.com/ko/rest

---

## 2. **지금 프로젝트에서 사용하는 방식 요약**

현재 프로젝트는 GitHub API를 활용해서 아래 데이터를 자동으로 수집해 **참여도 점수**를 계산하고 있어요:

| 수집 대상 | 방식 |
| --- | --- |
| PR (Pull Requests) | `GET /repos/{owner}/{repo}/issues` 호출 → `pull_request` 필드가 존재하면 PR로 간주 |
| 병합 여부 | `pull_request.merged_at` 필드가 `null`이 아니면 병합된 것으로 간주 |
| Issue | `pull_request` 필드가 없으면 일반 이슈로 처리 |
| 라벨 분석 | `enhancement`, `bug`, `documentation` 등의 label을 기준으로 활동 분류 |

사용된 API 예시:

```python
url = f"https://api.github.com/repos/{repo_path}/issues"
params = {
    'state': 'all',
    'per_page': 100,
    'page': page
}
```

- 이 `/issues` API는 PR과 Issue를 **한 번에 가져오는** 특징이 있어요. PR도 사실 내부적으로는 Issue 객체라서 가능한 방식입니다.

---

## 3. **API 인증과 제한 (Rate Limit)**

- 인증 없이: 시간당 60회 요청
- 인증 시 (Personal Access Token): 시간당 5,000회까지 가능
    
    → `Authorization: token <your_token>` 헤더로 추가해야 해요.
    

예:

```python
session.headers.update({"Authorization": f"token {your_token}"})

```

[토큰 생성 방법](docs/github-token-guide.md)

---

## 4. **직접 실습 가능한 튜토리얼 링크**

1. [GitHub REST API에 대한 빠른 시작](https://docs.github.com/ko/rest/quickstart?apiVersion=2022-11-28)
2. [Github REST API - Python | Pygithub 시작하기](https://waytocse.tistory.com/111)
3. [파이썬 requests로 API 호출 연습](https://realpython.com/api-integration-in-python/)

---

## 추천 학습 흐름

1. **Postman으로 API 테스트 해보기**
    
    → GitHub API 문서에서 `Try it` 기능 활용
    
2. **Python에서 `requests`로 호출해보기**
3. **Label과 merged 상태 확인하면서 PR/Issue 분석 코드 연습**