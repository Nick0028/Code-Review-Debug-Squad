from tools.code_analyzer import analyze_python
def test_valid_python():
    assert analyze_python("x = 1")["syntax_valid"] is True
def test_invalid_python():
    assert analyze_python("def broken(:")["syntax_valid"] is False
