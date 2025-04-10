# Test

이 저장소에서 기본적인 동작 이상 여부를 테스트하기 위한 자동화된 테스트 스위트를 사용할 수 있습니다.

### Install dependencies

테스트 과정을 진행하기 위해서 먼저 설치 후 실행.
```bash
make venv
make requirements
```

### 주의사항
- 의존성은 직접 설치합니다.
    테스트를 진행하거나 프로젝트를 로컬에서 동작시키려는 사용자는 `requirements.txt` 또는 `requirements-dev.txt`를 참고하여 필요한 의존성을 직접 설치해야 합니다. 테스트 코드나 기능 코드에서 **의존성을 자동 설치하는 코드는 구현하지 않습니다.**

- 새로운 라이브러리(의존성)은 반드시 .txt 파일에 추가합니다.
    기능 개발이나 테스트 작성 중 새로운 라이브러리가 필요해졌다면 반드시 requirements.txt 또는 requirements-dev.txt에 추가해 주세요. 그렇지 않으면 다른 사용자가 테스트 실행 시 오류가 발생할 수 있습니다.

- `requirements.txt`에는 실행에 꼭 필요한 라이브러리만 포함합니다.
    실제 코드 실행 및 테스트가 동작하는 데 꼭 필요한 의존성 목록입니다. 테스트나 개발용 도구는 이 파일에 포함하지 않습니다.

- `requirements-dev.txt`에는 개발/테스트 도구만 포함합니다.
    테스트 중 사용하는 보조 도구를 명시하는 개발용 의존성 목록입니다. 실제 기능 실행과는 관련 없는 개발/테스트 도구만 이 파일에 작성하며, `requirements.txt`와 혼동하지 않도록 구분해서 사용해 주세요

### Run Tests
다음 명령어를 수행하면 테스트가 진행됩니다.
```bash
make test
```

### How to Read Test Results

테스트 실행 결과는 다음과 같은 형식으로 출력됩니다.
```
=== test session starts ===
...
collected 3 items

tests/test_analyzer.py ..F [100%]

=== FAILURES ===
tests/test_analyzer.py::test_analyzer_initialization
```
- `.` : 테스트 성공
- `F` : 테스트 실패
- `[100%]` : 전체 테스트 실행 비율

자세한 실패 원인은 터미널 로그에서 확인할 수 있습니다.

### Writing New Tests

새로운 기능을 추가하면 `tests/` 디렉터리에 테스트 파일을 작성해야 합니다.

#### 예시 테스트 파일 (`tests/test_analyzer.py`)
```python
import pytest
from reposcore.analyzer import RepoAnalyzer

@pytest.fixture
def analyzer():
    return RepoAnalyzer("oss2025hnu/reposcore-py")

def test_initialization(analyzer):
    assert analyzer.repo == "oss2025hnu/reposcore-py"
    assert isinstance(analyzer.scores, dict)

def test_add_score(analyzer):
    analyzer.add_score("jass2345", 10)
    assert analyzer.scores["jass2345"] == 10
```
원하는 테스트를 추가한 후 `make test`를 실행하여 검증하세요.
