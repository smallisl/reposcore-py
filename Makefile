.PHONY: test lint readme check-readme pre-commit clean

PYTHON_MODULES := reposcore

VENV := .venv
VIRTUALENV := -m venv

DEFAULT_PYTHON := $(shell which python3)
PYTHON := env PYTHONPATH=$(PYTHONPATH) $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest

VERSION := $(shell grep '__version__' reposcore/__init__.py |cut -d'"' -f 2)

version:
	@echo $(VERSION)

venv:
	test -d $(VENV) || $(DEFAULT_PYTHON) $(VIRTUALENV) $(VENV)

requirements: venv
	$(PIP) install -r requirements.txt -r requirements-dev.txt

test: requirements
	$(PYTEST) tests

# README 동기화
readme:
	python scripts/generate_readme.py

# README 상태 검사
check-readme:
	@echo "🔍 README.md 최신 상태 여부를 검사합니다..."
	@cp README.md .README.bak
	@python scripts/generate_readme.py
	@if ! diff -q .README.bak README.md >/dev/null; then \
		echo "❌ README.md가 template_README.md 기반 최신 상태가 아닙니다."; \
		echo "👉 'make readme'를 실행해 주세요."; \
		rm .README.bak; \
		exit 1; \
	else \
		echo "✅ README.md는 최신 상태입니다."; \
		rm .README.bak; \
	fi

# PR 전에 자동으로 README 검증
pre-commit: check-readme

# 불필요한 파일 정리
clean:
	@if [ -d "$(VENV)" ]; then \
		echo ".venv 가상 환경을 삭제합니다..."; \
		rm -rf $(VENV); \
	fi
	@if [ -d "results" ]; then \
		echo "results 디렉토리를 삭제합니다..."; \
		rm -rf results; \
	fi
