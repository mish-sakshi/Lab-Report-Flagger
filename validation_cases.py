"""
validation_cases.py - a labelled 'gold standard' set of realistic panels.

Each case has: inputs, the disease patterns a clinician would expect the tool to
raise, and the expected urgency level. This is the ground truth we measure against.
Ranges/values are illustrative teaching cases, not real patients.
"""
CASES = [
    {"name": "Healthy young adult",
     "panel": {"sex": "M", "age": 28, "glucose": 88, "hba1c": 5.2, "hb": 15.0, "creatinine": 1.0},
     "expect_patterns": [], "expect_level": "routine"},

    {"name": "Classic type-2 diabetes",
     "panel": {"sex": "M", "age": 55, "glucose": 182, "hba1c": 8.4, "hb": 14.5, "creatinine": 1.0},
     "expect_patterns": ["Diabetes mellitus"], "expect_level": "soon"},

    {"name": "Prediabetes",
     "panel": {"sex": "F", "age": 46, "glucose": 112, "hba1c": 6.0, "hb": 13.5, "creatinine": 0.8},
     "expect_patterns": ["Prediabetes"], "expect_level": "soon"},

    {"name": "Iron-deficiency anaemia",
     "panel": {"sex": "F", "age": 32, "hb": 9.5, "ferritin": 8, "iron": 30},
     "expect_patterns": ["Anaemia", "Iron deficiency", "Iron-deficiency anaemia (combined)"],
     "expect_level": "soon"},

    {"name": "Chronic kidney disease",
     "panel": {"sex": "M", "age": 65, "creatinine": 2.1, "hb": 13.0},
     "expect_patterns": ["Chronic kidney disease"], "expect_level": "soon"},

    {"name": "Diabetic kidney disease (combined)",
     "panel": {"sex": "M", "age": 60, "glucose": 190, "hba1c": 9.0, "creatinine": 2.0, "hb": 12.0},
     "expect_patterns": ["Diabetes mellitus", "Chronic kidney disease", "Diabetic kidney disease (combined)"],
     "expect_level": "soon"},

    {"name": "Dyslipidaemia",
     "panel": {"sex": "M", "age": 50, "total_chol": 250, "ldl": 170, "hdl": 32, "triglycerides": 220},
     "expect_patterns": ["Dyslipidaemia (abnormal lipids)"], "expect_level": "soon"},

    {"name": "Liver injury",
     "panel": {"sex": "M", "age": 40, "alt": 240, "ast": 180, "bilirubin_total": 2.0},
     "expect_patterns": ["Liver injury"], "expect_level": "soon"},

    {"name": "Vitamin D deficiency",
     "panel": {"sex": "F", "age": 35, "vitamin_d": 12, "hb": 13.0},
     "expect_patterns": ["Vitamin D deficiency"], "expect_level": "soon"},

    {"name": "Vitamin B12 deficiency",
     "panel": {"sex": "F", "age": 50, "vitamin_b12": 150, "hb": 12.5},
     "expect_patterns": ["Vitamin B12 deficiency"], "expect_level": "soon"},

    {"name": "Severe anaemia (critical)",
     "panel": {"sex": "F", "age": 70, "hb": 6.2, "creatinine": 1.0},
     "expect_patterns": ["Anaemia"], "expect_level": "immediate"},

    {"name": "Severe hyperglycaemia (critical)",
     "panel": {"sex": "M", "age": 58, "glucose": 420, "hba1c": 11.0},
     "expect_patterns": ["Diabetes mellitus"], "expect_level": "immediate"},

    {"name": "Kidney failure (critical eGFR)",
     "panel": {"sex": "M", "age": 68, "creatinine": 6.5},
     "expect_patterns": ["Chronic kidney disease"], "expect_level": "immediate"},

    {"name": "All-normal full panel",
     "panel": {"sex": "F", "age": 40, "glucose": 90, "hba1c": 5.3, "hb": 13.5, "creatinine": 0.8,
               "total_chol": 180, "ldl": 90, "hdl": 60, "triglycerides": 120, "alt": 25},
     "expect_patterns": [], "expect_level": "routine"},

    {"name": "Real Sterling report (41 M)",
     "panel": {"sex": "M", "age": 41, "glucose": 141, "hba1c": 7.1, "hb": 14.5, "creatinine": 0.83,
               "total_chol": 189, "ldl": 100.39, "hdl": 60, "triglycerides": 168, "alt": 48,
               "ast": 27, "vitamin_d": 8.98, "vitamin_b12": 148, "iron": 103},
     "expect_patterns": ["Diabetes mellitus", "Dyslipidaemia (abnormal lipids)",
                         "Vitamin D deficiency", "Vitamin B12 deficiency"],
     "expect_level": "soon"},
]
