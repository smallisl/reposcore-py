from reposcore.analyzer import RepoAnalyzer

def test_analyzer_initialization():
    analyzer = RepoAnalyzer("oss2025hnu/reposcore-py")
    assert analyzer.repo_path == "oss2025hnu/reposcore-py"
    assert isinstance(analyzer.score_weights, dict)
