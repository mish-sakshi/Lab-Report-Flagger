RULESET_VERSION = "ranges v1.0 | eGFR CKD-EPI 2021"

# 1. Reference ranges.  "range" = same for all; "range_by_sex" = M/F specific.
#    One-sided tests: low=0 -> only HIGH flags; high very large -> only LOW flags.
REFERENCE = {
    "glucose": {"label": "Fasting Glucose", "loinc": ("1558-6", "Fasting glucose"), "unit": "mg/dL", "range": (70, 99)},
    "hba1c": {"label": "HbA1c", "loinc": ("4548-4", "Hemoglobin A1c/Hemoglobin.total in Blood"), "unit": "%", "range": (0, 5.7)},
    "hb": {"label": "Haemoglobin", "loinc": ("718-7", "Hemoglobin [Mass/volume] in Blood"), "unit": "g/dL",
           "range_by_sex": {"M": (13.0, 17.5), "F": (12.0, 15.5)}},
    "creatinine": {"label": "Creatinine", "loinc": ("2160-0", "Creatinine [Mass/volume] in Serum or Plasma"), "unit": "mg/dL",
                   "range_by_sex": {"M": (0.74, 1.35), "F": (0.59, 1.04)}},
    "total_chol": {"label": "Total Cholesterol", "loinc": ("2093-3", "Cholesterol [Mass/volume] in Serum or Plasma"), "unit": "mg/dL", "range": (0, 200)},
    "ldl": {"label": "LDL Cholesterol", "loinc": ("13457-7", "Cholesterol in LDL [Mass/volume] by calculation"), "unit": "mg/dL", "range": (0, 100)},
    "hdl": {"label": "HDL Cholesterol", "loinc": ("2085-9", "Cholesterol in HDL [Mass/volume]"), "unit": "mg/dL",
            "range_by_sex": {"M": (40, 200), "F": (50, 200)}},
    "triglycerides": {"label": "Triglycerides", "loinc": ("2571-8", "Triglyceride [Mass/volume]"), "unit": "mg/dL", "range": (0, 150)},
    "esr": {"label": "ESR", "loinc": ("4537-7", "Erythrocyte sedimentation rate"), "unit": "mm/hr", "range_by_sex": {"M": (0, 15), "F": (0, 20)}},
    "vitamin_d": {"label": "Vitamin D (25-OH)", "loinc": ("14635-7", "25-hydroxyvitamin D2+D3 [Mass/volume]"), "unit": "ng/mL", "range": (30, 100)},
    "vitamin_b12": {"label": "Vitamin B12", "loinc": ("2132-9", "Cobalamin (Vitamin B12) [Mass/volume]"), "unit": "pg/mL", "range": (200, 900)},
    "iron": {"label": "Serum Iron", "loinc": ("2498-4", "Iron [Mass/volume] in Serum or Plasma"), "unit": "ug/dL",
             "range_by_sex": {"M": (65, 175), "F": (50, 170)}},
    "ferritin": {"label": "Ferritin", "loinc": ("2276-4", "Ferritin [Mass/volume] in Serum or Plasma"), "unit": "ng/mL",
                 "range_by_sex": {"M": (24, 336), "F": (11, 307)}},
    "alt": {"label": "ALT (SGPT)", "loinc": ("1742-6", "Alanine aminotransferase"), "unit": "U/L", "range": (0, 55)},
    "ast": {"label": "AST (SGOT)", "loinc": ("1920-8", "Aspartate aminotransferase"), "unit": "U/L", "range": (0, 40)},
    "alp": {"label": "ALP", "loinc": ("6768-6", "Alkaline phosphatase"), "unit": "U/L", "range": (44, 147)},
    "bilirubin_total": {"label": "Total Bilirubin", "loinc": ("1975-2", "Bilirubin.total [Mass/volume]"), "unit": "mg/dL", "range": (0, 1.2)},
    "albumin": {"label": "Albumin", "loinc": ("1751-7", "Albumin [Mass/volume] in Serum or Plasma"), "unit": "g/dL", "range": (3.5, 5.0)},
    "total_protein": {"label": "Total Protein", "loinc": ("2885-2", "Protein [Mass/volume] in Serum or Plasma"), "unit": "g/dL", "range": (6.0, 8.3)},
    "urine_ph": {"label": "Urine pH", "loinc": ("5803-2", "pH of Urine by Test strip"), "unit": "", "range": (4.5, 8.0)},
    "urine_sg": {"label": "Urine Specific Gravity", "loinc": ("5811-5", "Specific gravity of Urine by Test strip"), "unit": "", "range": (1.005, 1.030)},
}

# 2. Plain-English meaning for each abnormal flag, keyed by (test, FLAG-UPPERCASE)
MEANINGS = {
    ("glucose", "HIGH"): "High fasting blood sugar. 100-125 suggests prediabetes; 126+ is in the diabetes range and should be confirmed.",
    ("glucose", "LOW"): "Low blood sugar (hypoglycaemia). Can cause shakiness or confusion; very low is an emergency.",
    ("hba1c", "HIGH"): "Raised average blood sugar. 5.7-6.4% suggests prediabetes; 6.5%+ is in the diabetes range.",
    ("hb", "LOW"): "Low haemoglobin (anaemia). May cause tiredness or breathlessness; severe anaemia needs prompt care.",
    ("hb", "HIGH"): "High haemoglobin. Can follow dehydration or smoking; sometimes needs investigation.",
    ("creatinine", "HIGH"): "High creatinine; the kidneys may be filtering less well. See the eGFR below.",
    ("creatinine", "LOW"): "Low creatinine; usually harmless (low muscle mass).",
    ("total_chol", "HIGH"): "High total cholesterol; raises cardiovascular risk.",
    ("ldl", "HIGH"): "High LDL ('bad') cholesterol; the main driver of heart-disease risk.",
    ("hdl", "LOW"): "Low HDL ('good') cholesterol; higher is protective, low raises risk.",
    ("triglycerides", "HIGH"): "High triglycerides; linked to diet and diabetes. Very high levels risk pancreatitis.",
    ("esr", "HIGH"): "Raised ESR; a non-specific marker of inflammation or infection.",
    ("vitamin_d", "LOW"): "Vitamin D deficiency; affects bones, muscles and immunity.",
    ("vitamin_d", "HIGH"): "Very high vitamin D; possible over-supplementation.",
    ("vitamin_b12", "LOW"): "B12 deficiency; can cause anaemia and nerve symptoms.",
    ("vitamin_b12", "HIGH"): "High B12; usually from supplements, rarely significant.",
    ("iron", "LOW"): "Low serum iron; may indicate iron deficiency.",
    ("iron", "HIGH"): "High iron; consider iron overload.",
    ("ferritin", "LOW"): "Low ferritin; often the earliest sign of iron deficiency.",
    ("ferritin", "HIGH"): "High ferritin; seen with inflammation or iron overload.",
    ("alt", "HIGH"): "Raised ALT (liver enzyme); liver cell stress or injury.",
    ("ast", "HIGH"): "Raised AST; from liver or sometimes muscle.",
    ("alp", "HIGH"): "Raised ALP; from liver/bile ducts or bone.",
    ("bilirubin_total", "HIGH"): "High bilirubin; can cause jaundice (liver or red-cell breakdown).",
    ("albumin", "LOW"): "Low albumin; poor nutrition, liver disease or kidney loss.",
    ("total_protein", "LOW"): "Low total protein; nutrition, liver or kidney causes.",
    ("total_protein", "HIGH"): "High total protein; dehydration or chronic inflammation.",
    ("urine_ph", "HIGH"): "Alkaline urine; diet, infection or kidney causes.",
    ("urine_ph", "LOW"): "Acidic urine; diet or metabolic causes.",
    ("urine_sg", "HIGH"): "Concentrated urine; often dehydration.",
    ("urine_sg", "LOW"): "Dilute urine; high fluid intake or kidney concentrating issues.",
}

# 3. Panic values -> "seek care now". Only list the dangerous side.
CRITICAL = {
    "glucose": {"low": 54, "high": 400},
    "hb": {"low": 7},
    "triglycerides": {"high": 1000},
}


def get_range(key, sex):
    meta = REFERENCE[key]
    if "range_by_sex" in meta:
        return meta["range_by_sex"][sex]
    return meta["range"]


def flag_label(value, low, high):
    if value < low:
        return "Low"
    elif value > high:
        return "High"
    return "Normal"


def describe(key, flag):
    if flag == "Normal":
        return "Within normal range."
    return MEANINGS.get((key, flag.upper()), "Discuss with the clinicians.")


def find_critical(values):
    warnings = []
    for key, limits in CRITICAL.items():
        if key not in values:
            continue
        v = float(values[key])
        if "low" in limits and v < limits["low"]:
            warnings.append(f"{REFERENCE[key]['label']} critically low ({v})")
        if "high" in limits and v > limits["high"]:
            warnings.append(f"{REFERENCE[key]['label']} critically high ({v})")
    return warnings


def egfr_ckdepi(creatinine, age, sex):
    """2021 CKD-EPI creatinine equation -> eGFR in mL/min/1.73m^2."""
    if sex == "F":
        k, a, factor = 0.7, -0.241, 1.012
    else:
        k, a, factor = 0.9, -0.302, 1.0
    r = creatinine / k
    return 142 * (min(r, 1) ** a) * (max(r, 1) ** -1.200) * (0.9938 ** age) * factor


def ckd_stage(egfr):
    if egfr >= 90: return "G1 (normal)"
    if egfr >= 60: return "G2 (mild)"
    if egfr >= 45: return "G3a (mild-moderate)"
    if egfr >= 30: return "G3b (moderate-severe)"
    if egfr >= 15: return "G4 (severe)"
    return "G5 (kidney failure)"


def detect_patterns(values, flags, egfr):
    patterns = []
    g, a1c = values.get("glucose"), values.get("hba1c")

    dm = []
    if g is not None and g >= 126: dm.append(f"glucose {g:.0f} >=126")
    if a1c is not None and a1c >= 6.5: dm.append(f"HbA1c {a1c:.1f}% >=6.5")
    if dm:
        patterns.append(("Diabetes mellitus", "likely" if len(dm) >= 2 else "possible", dm))
    else:
        pre = []
        if g is not None and 100 <= g < 126: pre.append(f"glucose {g:.0f} (100-125)")
        if a1c is not None and 5.7 <= a1c < 6.5: pre.append(f"HbA1c {a1c:.1f}% (5.7-6.4)")
        if pre: patterns.append(("Prediabetes", "possible", pre))

    if flags.get("hb") == "Low":
        patterns.append(("Anaemia", "likely", ["haemoglobin below range"]))
    if flags.get("ferritin") == "Low" or flags.get("iron") == "Low":
        patterns.append(("Iron deficiency", "likely", ["low iron stores"]))

    ckd = egfr is not None and egfr < 60
    if ckd or flags.get("creatinine") == "High":
        ev = []
        if egfr is not None: ev.append(f"eGFR {egfr:.0f}")
        if flags.get("creatinine") == "High": ev.append("creatinine high")
        patterns.append(("Chronic kidney disease", "likely" if ckd else "possible", ev))

    liver = [t for t in ("alt", "ast", "bilirubin_total") if flags.get(t) == "High"]
    if liver:
        patterns.append(("Liver injury", "possible", [f"{t} high" for t in liver]))

    lipids = [t for t in ("total_chol", "ldl", "triglycerides") if flags.get(t) == "High"]
    if flags.get("hdl") == "Low": lipids.append("HDL low")
    if lipids:
        patterns.append(("Dyslipidaemia (abnormal lipids)", "likely", lipids))

    if flags.get("vitamin_d") == "Low":
        patterns.append(("Vitamin D deficiency", "likely", ["vitamin D below range"]))
    if flags.get("vitamin_b12") == "Low":
        patterns.append(("Vitamin B12 deficiency", "likely", ["B12 below range"]))

    names = [p[0] for p in patterns]
    if "Diabetes mellitus" in names and "Chronic kidney disease" in names:
        patterns.append(("Diabetic kidney disease (combined)", "likely", ["diabetes + reduced kidney function"]))
    if "Anaemia" in names and "Iron deficiency" in names:
        patterns.append(("Iron-deficiency anaemia (combined)", "likely", ["anaemia + low iron stores"]))

    if not patterns:
        patterns.append(("No clear disease pattern", "healthy panel", []))
    return patterns


def conclude(abnormal, critical, patterns):
    if critical:
        return {"level": "immediate", "headline": "Seek medical care now",
                "advice": "Dangerous value(s): " + "; ".join(critical)
                          + ". Contact a doctor or emergency service immediately."}
    serious = [p for p in patterns if p[1] == "likely" and not p[0].startswith("No clear")]
    if serious:
        names = ", ".join(p[0] for p in serious)
        return {"level": "soon", "headline": "Book an appointment with a doctor soon",
                "advice": f"The results point to: {names}. Not an emergency, but see a "
                          "doctor in the next few days and bring this report."}
    if abnormal >= 1:
        return {"level": "soon", "headline": "Discuss these results with a doctor",
                "advice": f"{abnormal} value(s) are outside the usual range."}
    return {"level": "routine", "headline": "No urgent action indicated",
            "advice": "All values are within the usual ranges. Keep up routine check-ups."}


def build_result(panel):
    """panel = {'sex':'M','age':58,'glucose':180,...}. Returns a structured dict."""
    sex = panel["sex"].upper()
    age = int(panel["age"]) if "age" in panel and str(panel["age"]).strip() else None
    rows, values, flags = [], {}, {}
    for key, meta in REFERENCE.items():
        if key not in panel:
            continue
        low, high = get_range(key, sex)
        value = float(panel[key])
        flag = flag_label(value, low, high)
        values[key] = value
        flags[key] = flag
        rows.append({"key": key, "label": meta["label"], "value": value,
                     "unit": meta["unit"], "range": f"{low}-{high}", "low": low, "high": high,
                     "flag": flag, "meaning": describe(key, flag),
                     "loinc": meta.get("loinc", ("", ""))})

    abnormal = sum(row["flag"] != "Normal" for row in rows)
    critical = find_critical(values)

    egfr = None
    if "creatinine" in values and age is not None:
        egfr = egfr_ckdepi(values["creatinine"], age, sex)
        if egfr < 15:
            critical.append(f"very low kidney function (eGFR {egfr:.0f})")

    patterns = detect_patterns(values, flags, egfr)
    return {"sex": sex, "age": age, "results": rows, "abnormal_count": abnormal,
            "critical_warnings": critical, "egfr": egfr,
            "ckd_stage": ckd_stage(egfr) if egfr is not None else None,
            "patterns": patterns, "conclusion": conclude(abnormal, critical, patterns),
            "ruleset": RULESET_VERSION}
