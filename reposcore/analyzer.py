#!/usr/bin/env python3

import requests
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict

class RepoAnalyzer:
    """Class to analyze repository participation for scoring"""
    
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.participants: Dict = {}
        self.score_weights = {
            'PRs': 1,              #이 부분은 merge된 PR의 갯수를 세기 위해 잠시 배점이 아닌 1로 갯수를 셀 수 있도록 바꿔두었습니다.
            'issues_created': 0.3, #향후 배점이 필요할 경우 PRs를 기존 수치였던 0.4로 바꿔주세요.
            'issue_comments': 0.3
        }
    
    def collect_PRs(self) -> None:
        """GitHub API를 사용하여 병합(Merged)된 Pull Request 개수를 수집"""
        page = 1  
        per_page = 100  

        merged_pr_count = 0
        
        while True:
            url = f"https://api.github.com/repos/{self.repo_path}/pulls?state=closed&page={page}&per_page={per_page}"
            response = requests.get(url)

            if response.status_code != 200:
                print(f"⚠️ GitHub API 요청 실패: {response.status_code}")
                return

            prs_data = response.json()  
            if not prs_data:
                break

            for pr in prs_data:
                if pr.get("merged_at"):  # 병합된 PR만 카운트
                    author = pr.get("user", {}).get("login", "Unknown")
                    
                    if author not in self.participants:
                        self.participants[author] = {"PRs": 0, "issues_created": 0, "issue_comments": 0}
                    
                    self.participants[author]["PRs"] += 1 

                    merged_pr_count += 1 

            page += 1  
        print(f"병합된 PR 총 개수: {merged_pr_count}")
        
    def collect_issues(self) -> None:
        """(pr이 아닌) github 이슈를 수집하고, 이슈 작성자"""

        issues_count = 0

        page = 1
        per_page = 100
        
        while True:
            url=f"https://api.github.com/repos/{self.repo_path}/issues?state=all&page={page}&per_page={per_page}"
            response = requests.get(url)

            if response.status_code != 200:
                print(f"⚠️ GitHub API 요청 실패: {response.status_code}")
                return

            issues_data = response.json()
            if not issues_data:  # 더 이상 가져올 이슈가 없으면 반복 종료료
                break

            for issue in issues_data:
                #pull_request라는 필드가 있으면 무시
                if "pull_request" in issue:
                    continue

                author = issue.get("user", {}).get("login", "Unknown")
                if author not in self.participants:
                    self.participants[author] = {
                        "PRs": 0,
                        "issues_created": 0
                    }

                #이슈 카운트
                self.participants[author]["issues_created"] += 1

                issues_count += 1 

            page += 1

        print(f"issues 총 개수: {issues_count}")
        

    def calculate_scores(self) -> Dict:
        """Calculate participation scores for each contributor"""
        scores = {}
        for participant, activities in self.participants.items():
            total_score = (
                activities.get('PRs', 0) * self.score_weights['PRs'] +
                activities.get('issues_created', 0) * self.score_weights['issues_created'] +
                activities.get('issue_comments', 0) * self.score_weights['issue_comments']
            )
            scores[participant] = total_score
        return scores


    def generate_table(self, scores: Dict) -> pd.DataFrame:
        """Generate a table of participation scores"""
        df = pd.DataFrame.from_dict(scores, orient='index', columns=['Score'])
        return df

    def generate_chart(self, scores: Dict) -> None:
        """Generate a visualization of participation scores"""
        plt.figure(figsize=(10, 6))
        plt.bar(scores.keys(), scores.values())
        plt.xticks(rotation=45)
        plt.ylabel('Participation Score')
        plt.title('Repository Participation Scores')
        plt.tight_layout()
        plt.savefig('participation_chart.png')

