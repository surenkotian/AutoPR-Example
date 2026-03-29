from autopr import coverage_utils


def test_parse_coverage_summary_total():
    text = """
Name     Stmts   Miss  Cover
----------------------------
TOTAL     100     15    85%
"""
    res = coverage_utils.parse_coverage_enhanced(text)
    assert res.coverage_percent == 85.0


def test_compare_coverage():
    before = "TOTAL 100 20 80%"
    after = "TOTAL 100 15 85%"
    res = coverage_utils.compare_coverage(before, after)
    assert res["before"]["coverage_percent"] == 80.0
    assert res["after"]["coverage_percent"] == 85.0
    assert res["overall_change"] == 5.0
