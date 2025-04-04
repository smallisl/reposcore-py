#!/usr/bin/env python3
#테스트
import argparse
import sys
import requests
from .analyzer import RepoAnalyzer

# 깃허브 저장소 기본 URL
GITHUB_BASE_URL = "https://github.com/"

def validate_repo_format(repo: str) -> bool:
    """Check if the repo input follows 'owner/repo' format"""
    parts = repo.split("/") # '/'를 기준으로 분리 (예: 'oss2025hnu/reposcore-py' → ['oss2025hnu', 'reposcore-py'])
    return len(parts) == 2 and all(parts) # 두 개의 부분(owner, repo)이 존재해야 하고, 비어 있으면 안 됨

def check_github_repo_exists(repo: str) -> bool:
    """Check if the given GitHub repository exists"""
    url = f"https://api.github.com/repos/{repo}" # 예: 'oss2025hnu/reposcore-py' → 'https://api.github.com/repos/oss2025hnu/reposcore-py'
    response = requests.get(url) # API 요청 보내기
    return response.status_code == 200 # 응답코드가 정상이면 저장소가 존재함

def parse_arguments() -> argparse.Namespace:
    """커맨드라인 인자를 파싱하는 함수"""
    parser = argparse.ArgumentParser(
        prog="python -m reposcore",
        description="오픈 소스 수업용 레포지토리의 기여도를 분석하는 CLI 도구",
        add_help=False  # 기본 --help 옵션을 비활성화
    )
    
    parser.add_argument(
        "-h", "--help",
        action="help",
        help="도움말 표시 후 종료"
    )
    parser.add_argument(
        "--repo",
        type=str,
        required=True,
        help="분석할 GitHub 저장소 (형식: '소유자/저장소') 예: 'oss2025hnu/reposcore-py'"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="results",
        help="분석 결과를 저장할 출력 디렉토리 (기본값: 'results')"
    )
    parser.add_argument(
        "--format",
        choices=["table", "chart", "both"],
        default="both",
        help="결과 출력 형식 선택 (테이블: 'table', 차트: 'chart', 둘 다: 'both')"
    )
    return parser.parse_args()


def main():
    """Main execution function"""
    args = parse_arguments()

    # Validate repo format
    if not validate_repo_format(args.repo):
        print("오류 : --repo 옵션은 'owner/repo' 형식으로 입력해야 함. 예) 'oss2025hnu/reposcore-py'")
        sys.exit(1)

    # (Optional) Check if the repository exists on GitHub
    if not check_github_repo_exists(args.repo):
        print(f"입력한 저장소 '{args.repo}' 가 깃허브에 존재하지 않을 수 있음.")
    
    print(f"저장소 분석 시작 : {args.repo}")

    # Initialize analyzer
    analyzer = RepoAnalyzer(args.repo)
    
    try:
        # Collect participation data
        print("Collecting PR data...")
        analyzer.collect_PRs()
        
        print("Collecting issues data...")
        analyzer.collect_issues()
        
        # Calculate scores
        scores = analyzer.calculate_scores()
        
        print("\n📊 기여 요약 (PR + 이슈):")
        for user, stats in analyzer.participants.items():
            pr_count = stats.get("PRs", 0)
            issue_count = stats.get("issues_created", 0)
            print(f"- {user} : PR {pr_count}개 / 이슈 {issue_count}개")

        # Generate outputs based on format
        if args.format in ["table", "both"]:
            table = analyzer.generate_table(scores)
            table.to_csv(f"{args.output}_scores.csv")
            print("\nParticipation Scores Table:")
            print(table)
            
        if args.format in ["chart", "both"]:
            analyzer.generate_chart(scores)
            print(f"Chart saved as participation_chart.png")
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
