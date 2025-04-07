import subprocess
import sys
import os

def test_main_help_runs():
    """--help 옵션이 정상 작동하는지 확인"""
    result = subprocess.run(
        [sys.executable, "-m", "reposcore", "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "도움말 표시 후 종료" in result.stdout

def test_main_repo_runs():
    """--repo 옵션이 최소한 실행되고 종료되지 않는지 확인"""
    result = subprocess.run(
        [sys.executable, "-m", "reposcore", "--repo", "oss2025hnu/reposcore-py"],
        capture_output=True,
        text=True
    )
    # 비정상적인 종료 (예: AttributeError) 가 없어야 함
    assert result.returncode == 0
    assert "저장소 분석 시작" in result.stdout or "Participation Scores Table" in result.stdout
