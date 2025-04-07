#!/usr/bin/env python3

from typing import Dict
import matplotlib.pyplot as plt
import pandas as pd
import requests


class RepoAnalyzer:
    """Class to analyze repository participation for scoring"""

    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.participants: Dict = {}
        self.score_weights = {
            'PRs': 1,  # 이 부분은 merge된 PR의 PR 갯수, issues 갯수만 세기 위해 임시로 1로 변경
            'issues_created': 1,  # 향후 배점이 필요할 경우 PRs: 0.4, issues: 0.3으로 바꿔주세요.
            'issue_comments': 1
        }

    def collect_PRs_and_issues(self) -> None:
        """
        하나의 API 호출로 GitHub 이슈 목록을 가져오고,
        pull_request 필드가 있으면 PR로, 없으면 issue로 간주.
        PR의 경우, 실제로 병합된 경우만 점수에 반영.
        """
        page = 1
        per_page = 100

        while True:
            url = f"https://api.github.com/repos/{self.repo_path}/issues"
            response = requests.get(url, params={
                'state': 'all',
                'per_page': per_page,
                'page': page
            })
            if response.status_code != 200:
                print(f"⚠️ GitHub API 요청 실패: {response.status_code}")
                return

            items = response.json()
            if not items:
                break

            for item in items:
                author = item.get('user', {}).get('login', 'Unknown')
                if author not in self.participants:
                    self.participants[author] = {
                        'p_enhancement': 0,
                        'p_bug': 0,
                        'p_documentation': 0,
                        'i_enhancement': 0,
                        'i_bug': 0,
                        'i_documentation': 0,
                    }

                labels = item.get('labels', [])
                label_names = [label.get('name', '') for label in labels if label.get('name')]

                if 'pull_request' in item:
                    pr_url = item.get('pull_request', {}).get('url')
                    if pr_url:
                        pr_response = requests.get(pr_url)
                        if pr_response.status_code == 200:
                            pr_data = pr_response.json()
                            if pr_data.get('merged_at') is not None:
                                for label in label_names:
                                    key = f'p_{label}'
                                    if key in self.participants[author]:
                                        self.participants[author][key] += 1
                else:
                    for label in label_names:
                        key = f'i_{label}'
                        if key in self.participants[author]:
                            self.participants[author][key] += 1

             # 'link'가 없으면 False 처리
            link_header = response.headers.get('link', '')
            if 'rel="next"' in link_header:
                page += 1
            else:
                break

        page = 1
        pages_remaining = True

        while pages_remaining:
            # GitHub Issues API (pull request 역시 issue로 취급)
            url = f'https://api.github.com/repos/{self.repo_path}/issues'
            response = requests.get(url,
                                    params={
                                        'state': 'all',
                                        'per_page': per_page,
                                        'page': page
                                    })

        print("\n참여자별 활동 내역 (participants 딕셔너리):")
        for user, info in self.participants.items():
            print(f"{user}: {info}")

    def calculate_scores(self) -> Dict:
        """Calculate participation scores for each contributor using the refactored formula"""
        scores = {}
        for participant, activities in self.participants.items():
            p_f = activities.get('p_enhancement', 0)
            p_b = activities.get('p_bug', 0)
            p_d = activities.get('p_documentation', 0)
            p_fb = p_f + p_b

            i_f = activities.get('i_enhancement', 0)
            i_b = activities.get('i_bug', 0)
            i_d = activities.get('i_documentation', 0)
            i_fb = i_f + i_b

            p_valid = p_fb + min(p_d, 3 * p_fb)
            i_valid = min(i_fb + i_d, 4 * p_valid)

            p_fb_at = min(p_fb, p_valid)
            p_d_at = p_valid - p_fb

            i_fb_at = min(i_fb, i_valid)
            i_d_at = i_valid - i_fb_at

            S = 3 * p_fb_at + 2 * p_d_at + 2 * i_fb_at + 1 * i_d_at
            scores[participant] = S

        return scores

    def generate_table(self, scores: Dict, save_path: str = "results") -> None:
        """Generate a table of participation scores"""
        df = pd.DataFrame.from_dict(scores, orient='index', columns=['Score'])
        df.to_csv(save_path)

    def generate_chart(self, scores: Dict, save_path: str = "results") -> None:
        """Generate a visualization of participation scores"""
        plt.figure(figsize=(10, 6))
        plt.bar(scores.keys(), scores.values())
        plt.xticks(rotation=45)
        plt.ylabel('Participation Score')
        plt.title('Repository Participation Scores')
        plt.tight_layout()
        plt.savefig(save_path)
