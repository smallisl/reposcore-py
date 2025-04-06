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
        collect_PRs와 collect_issues의 기능을 통합한 함수.
        GitHub 이슈 목록을 한 번에 가져온 뒤,
        pull_request 필드로 PR 여부를 구분하고,
        병합된 PR이면 PR 카운트로,
        일반 이슈라면 이슈 카운트로 기록한다.
        """
        page = 1
        per_page = 100

        pages_remaining = True

        while pages_remaining:
            url = f'https://api.github.com/repos/{self.repo_path}/pulls'
            response = requests.get(url,
                                    params={
                                        'state': 'all',
                                        'per_page': per_page,
                                        'page': page
                                    })

            if response.status_code != 200:
                print(f"⚠️ GitHub API 요청 실패: {response.status_code}")
                return

            items = response.json()

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

                if len(item['labels']) != 0:
                    label_names = list(map(lambda x: x.get('name', ''), item['labels']))
                    # print(label_names)
                    for label in label_names:
                        self.participants[author][f'p_{label}'] += 1

            pages_remaining = True if 'rel="next"' in response.headers['link'] else False
            page += 1

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

            if response.status_code != 200:
                print(f'⚠️ GitHub API 요청 실패: {response.status_code}')
                return

            items = response.json()

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

                if len(item['labels']) != 0:
                    label_names = list(map(lambda x: x.get('name', ''), item['labels']))
                    for label in label_names:
                        self.participants[author][f'i_{label}'] += 1

            pages_remaining = True if 'rel="next"' in response.headers['link'] else False
            page += 1

    def calculate_scores(self) -> Dict:
        """Calculate participation scores for each contributor"""
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

        # participants 딕셔너리 출력
        print("\n참여자별 활동 내역 (participants 딕셔너리):")
        for user, info in self.participants.items():
            print(f"{user}: {info}")

        return scores

    def generate_table(self, scores: Dict, save_path: str = "results") -> None:
        """Generate a table of participation scores"""
        df = pd.DataFrame.from_dict(scores, orient='index', columns=['Score'])
        df.to_csv(save_path)

    def generate_chart(self, scores: Dict, save_path: str = "results") -> None:
        """Generate a visualization of participation scores"""
        # scores 딕셔너리의 항목들을 점수를 기준으로 내림차순 정렬
        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        
        # 정렬된 결과에서 참여자와 점수를 분리
        # 정렬된 결과가 없으면 빈 튜플을 사용
        participants, scores_sorted = zip(*sorted_scores) if sorted_scores else ([], [])
        
        # 참여자 수에 따라 차트의 세로 길이를 동적으로 결정
        # 최소 높이는 3인치로 설정하고, 참여자 수에 0.2인치를 곱해 높이를 정함
        num_participants = len(participants)
        height = max(3, num_participants * 0.2)
        
        # 가로 10인치, 세로 'height'인 그림 창을 생성
        plt.figure(figsize=(10, height))
        
        # 수평 막대그래프를 그리며, 막대의 두께를 0.5로 설정
        bars = plt.barh(participants, scores_sorted, height=0.5)
        
        # x축 레이블을 'Participation Score'로 설정
        plt.xlabel('Participation Score')
        
        # 차트 제목을 'Repository Participation Scores'로 설정
        plt.title('Repository Participation Scores')
        
        # y축의 순서를 반전시켜, 가장 높은 점수가 위쪽에 표시되도록 합니다.
        plt.gca().invert_yaxis()
        
        # 각 막대의 오른쪽에 해당 점수를 텍스트로 표시하는 파트
        for bar in bars:
            plt.text(
                bar.get_width() + 0.2,          # 막대의 길이에 0.2만큼 더해 오른쪽에 위치
                bar.get_y() + bar.get_height(), # 막대의 y위치에서 막대 높이만큼 내려가 텍스트 위치를 지정
                f'{bar.get_width():.1f}',       # 막대의 길이(점수)를 정수 형태의 문자열로 표시
                va='center',                    # 텍스트를 수직 중앙 정렬
                fontsize=9                      # 글씨 크기를 9로 설정
            )
        
        # 전체 레이아웃을 정리하고, 패딩을 2로 설정해 여백을 조정
        plt.tight_layout(pad=2)
        
        # 설정한 경로에 차트를 저장
        plt.savefig(save_path)
