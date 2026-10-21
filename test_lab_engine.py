from lab_engine import build_result

def test_healthy_panel():
    r = build_result({"sex": "M", "age": 30, "glucose": 85, "hb": 15, "creatinine": 1.0})
    assert r["abnormal_count"] == 0
    assert r["conclusion"]["level"] == "routine"

def test_diabetes_detected():
    r = build_result({"sex": "M", "age": 55, "glucose": 180, "hba1c": 8.0, "hb": 14, "creatinine": 1.0})
    names = [p[0] for p in r["patterns"]]
    assert "Diabetes mellitus" in names
    assert r["conclusion"]["level"] == "soon"

def test_critical_low_hb():
    r = build_result({"sex": "F", "age": 40, "hb": 6.5})
    assert r["critical_warnings"]
    assert r["conclusion"]["level"] == "immediate"

def test_one_sided_flags():
    r = build_result({"sex": "M", "age": 40, "hdl": 30, "ldl": 160})
    flags = {row["key"]: row["flag"] for row in r["results"]}
    assert flags["hdl"] == "Low"
    assert flags["ldl"] == "High"

def test_egfr_present():
    r = build_result({"sex": "M", "age": 58, "creatinine": 1.9})
    assert r["egfr"] is not None
    assert 30 <= r["egfr"] <= 50
