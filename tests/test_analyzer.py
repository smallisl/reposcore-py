import os
import tempfile
from reposcore.analyzer import RepoAnalyzer


def test_example_calculate_scores():
    analyzer = RepoAnalyzer("oss2025hnu/reposcore-py")
    analyzer.participants = {
        "test_user1": {
            "p_enhancement": 2,
            "p_bug": 1,
            "p_typo": 1, 
            "p_documentation": 3,
            "i_enhancement": 2,
            "i_bug": 2,
            "i_documentation": 2,
        },
        "test_user2": {
            "p_enhancement": 0,
            "p_bug": 0,
            "p_typo": 1, 
            "p_documentation": 10,
            "i_enhancement": 0,
            "i_bug": 0,
            "i_documentation": 10,
        },
        "test_user3": {
            "p_enhancement": 3,
            "p_bug": 3,
            "p_typo": 1, 
            "p_documentation": 20,
            "i_enhancement": 5,
            "i_bug": 5,
            "i_documentation": 5,
        },
        "test_user4": {
            "p_enhancement": 1,
            "p_bug": 1,
            "p_typo": 1, 
            "p_documentation": 1,
            "i_enhancement": 0,
            "i_bug": 0,
            "i_documentation": 0,
        },
        "test_user5": {
            "p_enhancement": 2,
            "p_bug": 0,
            "p_typo": 1, 
            "p_documentation": 0,
            "i_enhancement": 0,
            "i_bug": 0,
            "i_documentation": 0,
        },
        "test_user6": {
            "p_enhancement": 0,
            "p_bug": 0,
            "p_typo": 1, 
            "p_documentation": 0,
            "i_enhancement": 3,
            "i_bug": 3,
            "i_documentation": 6,
        },
        "test_user7": {
            "p_enhancement": 2,
            "p_bug": 2,
            "p_typo": 1, 
            "p_documentation": 12,
            "i_enhancement": 4,
            "i_bug": 4,
            "i_documentation": 20,
        },
        "test_user8": {
            "p_enhancement": 0,
            "p_bug": 2,
            "p_typo": 1, 
            "p_documentation": 6,
            "i_enhancement": 1,
            "i_bug": 1,
            "i_documentation": 3,
        },
        "test_user9": {
            "p_enhancement": 0,
            "p_bug": 2,
            "p_typo": 1, 
            "p_documentation": 5,
            "i_enhancement": 2,
            "i_bug": 0,
            "i_documentation": 1,
        },
        "test_user10": {
            "p_enhancement": 3,
            "p_bug": 0,
            "p_typo": 1, 
            "p_documentation": 3,
            "i_enhancement": 3,
            "i_bug": 0,
            "i_documentation": 3,
        },
    }

    scores = analyzer.calculate_scores()
    assert scores["test_user1"]['total'] == 26, "test_user1 결과값이 일치하지 않습니다."
    assert scores["test_user2"]['total'] == 17, "test_user2 결과값이 일치하지 않습니다."
    assert scores["test_user3"]['total'] == 80, "test_user3 결과값이 일치하지 않습니다."
    assert scores["test_user4"]['total'] == 9, "test_user4 결과값이 일치하지 않습니다."
    assert scores["test_user5"]['total'] == 7, "test_user5 결과값이 일치하지 않습니다."
    assert scores["test_user6"]['total'] == 1, "test_user6 결과값이 일치하지 않습니다."
    assert scores["test_user7"]['total'] == 73, "test_user7 결과값이 일치하지 않습니다."
    assert scores["test_user8"]['total'] == 26, "test_user8 결과값이 일치하지 않습니다."
    assert scores["test_user9"]['total'] == 22, "test_user9 결과값이 일치하지 않습니다."
    assert scores["test_user10"]['total'] == 25, "test_user10 결과값이 일치하지 않습니다."

def test_generate_table_creates_file():
    analyzer = RepoAnalyzer("dummy/repo")
    scores = {
        "alice": {
            "feat/bug PR": 9,
            "document PR": 6,
            "typo PR": 1,
            "feat/bug issue": 6,
            "document issue": 3,
            "total": 25,
            "rate": 100
        },
        "bob": {
            "feat/bug PR": 9,
            "document PR": 6,
            "typo PR": 0,
            "feat/bug issue": 6,
            "document issue": 3,
            "total": 24,
            "rate": 96
        }
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test_table.csv")
        analyzer.generate_table(scores, save_path=filepath)
        assert os.path.isfile(filepath), "CSV 파일이 생성되지 않았습니다."
        # count.csv는 더 이상 generate_table에서 생성하지 않음
        count_path = os.path.join(os.path.dirname(filepath), "count.csv")
        assert not os.path.isfile(count_path), "count.csv 파일이 generate_table에서 생성되었습니다."

def test_generate_count_csv_creates_file():
    analyzer = RepoAnalyzer("dummy/repo")
    scores = {
        "alice": {
            "feat/bug PR": 9,
            "document PR": 6,
            "typo PR": 1,
            "feat/bug issue": 6,
            "document issue": 3,
            "total": 25,
            "rate": 100
        },
        "bob": {
            "feat/bug PR": 9,
            "document PR": 6,
            "typo PR": 0,
            "feat/bug issue": 6,
            "document issue": 3,
            "total": 24,
            "rate": 96
        }
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test_scores.csv")
        count_path = analyzer.generate_count_csv(scores, save_path=filepath)
        assert os.path.isfile(count_path), "count.csv 파일이 생성되지 않았습니다."
        
        # 생성된 파일 내용 확인
        with open(count_path, 'r') as f:
            content = f.read()
            assert "name,feat/bug PR,document PR,typo PR,feat/bug issue,document issue" in content
            assert "alice,3,3,1,3,3" in content
            assert "bob,3,3,0,3,3" in content

def test_generate_chart_creates_file():
    analyzer = RepoAnalyzer("dummy/repo")
    scores = {
        "alice": {
            "feat/bug PR": 9,
            "document PR": 6,
            "typo PR": 0,
            "feat/bug issue": 6,
            "document issue": 3,
            "total": 24,
            "rate": 100
        },
        "bob": {
            "feat/bug PR": 9,
            "document PR": 6,
            "typo PR": 0,
            "feat/bug issue": 6,
            "document issue": 3,
            "total": 24,
            "rate": 100
        }
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test_chart.png")
        analyzer.generate_chart(scores, save_path=filepath)
        assert os.path.isfile(filepath), "차트 이미지 파일이 생성되지 않았습니다."
