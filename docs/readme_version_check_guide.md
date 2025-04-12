# README.md 최신 상태 여부 검사 가이드

이 프로젝트는 `README.md` 파일을 수동으로 수정하지 않고,
`template_README.md` 템플릿을 기반으로 자동으로 생성 및 관리합니다.

## ✅ 자동 생성 방식

`make readme` 명령어를 실행하면, `scripts/generate_readme.py` 가 실행되어:

1. `reposcore`의 CLI 사용법을 `--help`로 추출하고,
2. `template_README.md` 템플릿을 Jinja2 로 렌더링하며,
3. 최종 결과물을 `README.md`로 저장합니다.

```bash
make readme
```

## ✅ 최신 상태 검증 방식

`README.md`가 최신 상태인지 확인하려면 다음 명령어를 실행합니다:

```bash
make check-readme
```

이 명령어는 임시 파일로 README를 다시 생성하여 기존 파일과 비교하고,
차이가 있으면 다음과 같이 경고합니다:

```
❌ README.md가 template_README.md 기반 최신 상태가 아닙니다.
👉 'make readme'를 실행해 주세요.
```

## ✅ PR 전 자동 검사

`make pre-commit` 명령어는 `make readme`를 실행하여 PR 전에 항상 최신 README가 생성되도록 보장합니다.

```bash
make pre-commit
```

---

> 이 자동화 방식은 실수로 `README.md`를 갱신하지 않아 템플릿과 내용이 불일치하는 문제를 방지합니다.
> 템플릿만 수정한 뒤 `make readme`를 실행하면 항상 최신 상태가 유지됩니다.
