# README.md 자동 생성 및 최신 상태 유지 가이드

이 프로젝트에서는 `README.md`를 직접 수정하지 않고,  
`template_README.md` 템플릿을 기반으로 **자동 생성 및 관리**합니다.

## ✅ 자동 생성 방식

```bash
make readme
```

위 명령어는 다음 조건 중 **하나라도 변경**되었을 때 `README.md`를 자동 생성합니다:

- `template_README.md` 템플릿이 수정됨
- `scripts/generate_readme.py` 스크립트가 수정됨

실행 시에는 다음 동작이 이루어집니다:

1. `reposcore`의 CLI 사용법을 `--help`로 추출
2. `template_README.md`를 Jinja2로 렌더링
3. 최종 결과를 `README.md`로 저장

## ✅ 최신 상태 유지 방식

Make는 각 파일의 **최종 수정 시각**을 기준으로 `README.md`의 최신 여부를 자동 판별합니다.  
`README.md`보다 `template_README.md` 또는 `generate_readme.py`가 더 최근이면 자동으로 갱신됩니다.

## ✅ PR 전 자동 실행

```bash
make pre-commit
```

이 명령어는 `make readme`를 실행하여 PR 전 항상 최신 상태의 `README.md`가 생성되도록 합니다.

---

> 이 자동화 방식은 `README.md`의 수동 갱신 누락을 방지합니다.  
> 템플릿만 수정한 후 `make readme`를 실행하거나, PR 전에 `make pre-commit`을 실행하세요.
