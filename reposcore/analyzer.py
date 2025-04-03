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

            page += 1  

    def collect_issues(self) -> None:
        """Collect issues and comments data"""
        pass

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
