"""fhir_export.py - turn a build_result() output into a FHIR R4 Bundle."""
import datetime

# FHIR value sets
INTERP = {"High": ("H", "High"), "Low": ("L", "Low"), "Normal": ("N", "Normal")}
LOINC_SYS = "http://loinc.org"
UCUM_SYS = "http://unitsofmeasure.org"
INTERP_SYS = "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation"
CAT_SYS = "http://terminology.hl7.org/CodeSystem/observation-category"


def _observation(row, patient_ref, when):
    code, display = row.get("loinc", ("", ""))
    coding = []
    if code:
        coding.append({"system": LOINC_SYS, "code": code, "display": display})
    obs = {
        "resourceType": "Observation",
        "id": f"obs-{row['key'].replace('_', '-')}",
        "status": "final",
        "category": [{"coding": [{"system": CAT_SYS, "code": "laboratory", "display": "Laboratory"}]}],
        "code": {"coding": coding, "text": row["label"]},
        "subject": {"reference": patient_ref},
        "effectiveDateTime": when,
        "valueQuantity": {"value": row["value"], "unit": row["unit"] or "1",
                          "system": UCUM_SYS, "code": row["unit"] or "1"},
    }
    icode, idisp = INTERP.get(row["flag"], ("N", "Normal"))
    obs["interpretation"] = [{"coding": [{"system": INTERP_SYS, "code": icode, "display": idisp}]}]
    rng = {}
    if row.get("low") not in (None, 0):
        rng["low"] = {"value": row["low"], "unit": row["unit"]}
    if row.get("high") is not None:
        rng["high"] = {"value": row["high"], "unit": row["unit"]}
    rng["text"] = row["range"]
    obs["referenceRange"] = [rng]
    return obs


def build_fhir_bundle(result):
    when = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
    patient_ref = "Patient/patient"

    patient = {"resourceType": "Patient", "id": "patient",
               "gender": "male" if result["sex"] == "M" else "female"}
    if result.get("age"):
        patient["birthDate"] = str(datetime.date.today().year - int(result["age"]))

    entries = [{"resource": patient}]
    obs_refs = []
    for row in result["results"]:
        obs = _observation(row, patient_ref, when)
        entries.append({"resource": obs})
        obs_refs.append({"reference": f"Observation/{obs['id']}"})

    report = {
        "resourceType": "DiagnosticReport",
        "id": "report",
        "status": "final",
        "category": [{"coding": [{"system": CAT_SYS, "code": "LAB", "display": "Laboratory"}]}],
        "code": {"coding": [{"system": LOINC_SYS, "code": "11502-2", "display": "Laboratory report"}],
                 "text": "Lab Report Flagger result"},
        "subject": {"reference": patient_ref},
        "effectiveDateTime": when,
        "issued": when,
        "conclusion": f"{result['conclusion']['headline']} — {result['conclusion']['advice']}",
        "result": obs_refs,
    }
    entries.append({"resource": report})

    return {"resourceType": "Bundle", "type": "collection", "timestamp": when, "entry": entries}
