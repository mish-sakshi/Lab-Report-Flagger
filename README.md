🩸 **Lab Report Flagger**

A transparent, rule-based web app that reads a blood-test report (PDF or scan), flags each value against age- and sex-specific reference ranges, explains what each abnormal value means, reads the results together to surface likely disease patterns, and ends with a clear verdict: see a doctor immediately, soon, or not urgently.

Built as an open, auditable alternative to black-box "explain my labs" tools — every flag is traceable to its range and rule-set version, the output is spec-valid FHIR R4 with LOINC codes, and the engine ships with a validation suite.

⚕️ Educational screening only — not a diagnosis. Reference ranges are standard adult values and vary by lab. Always consult a qualified doctor. In an emergency, seek care immediately.

✨ **Features**
Two ways in — upload a lab report (native-text PDF or scanned/image PDF via OCR) or type values manually.
Smart PDF reading — a unit-anchored, line-by-line parser that ignores the pages of educational prose real reports contain, and OCR (Tesseract) for scanned/photographed reports. Password-protected PDFs supported.
Flagging — each of 20+ tests flagged Low / Normal / High against age/sex ranges, with plain-English meanings.
Clinical reasoning — reads flags together to raise patterns: Diabetes, Anaemia, Chronic kidney disease, Dyslipidaemia, Liver injury, vitamin deficiencies, and combined patterns like Diabetic kidney disease and Iron-deficiency anaemia.
Real calculations — eGFR via the 2021 CKD-EPI equation with CKD staging (G1–G5).
One clear conclusion — immediate / soon / routine, with the reasoning behind it.
Interoperability — export a FHIR R4 Bundle (LOINC-coded Observations + DiagnosticReport), importable by health systems.
Validated — a labelled validation suite measures conclusion-level accuracy and pattern recall.
Private by design — values are processed in memory; nothing is stored.

🧰 **Tech stack**
Area	Tools
App / UI -->	Streamlit, Altair, pandas
PDF / OCR -->	pdfplumber (text), PyMuPDF + pytesseract (scans)
Standards	LOINC codes, FHIR R4 (validated with fhir.resources)
Testing	pytest (unit tests) + a labelled validation suite

📁**Project structure**
lab-report-flagger/
├── app.py                 # Streamlit web app (UI)
├── lab_engine.py          # The engine: ranges, flags, eGFR, patterns, conclusion, LOINC
├── pdf_extract.py         # Native-PDF + OCR report reader
├── fhir_export.py         # FHIR R4 Bundle export
├── validation_cases.py    # Labelled "gold standard" cases
├── validate.py            # Runs the validation suite, prints accuracy
├── test_lab_engine.py     # pytest unit tests
├── make_sample.py         # Generates a sample PDF for testing
├── requirements.txt       # Python dependencies
└── packages.txt           # System packages for deploy (tesseract-ocr)
🚀 Run it locally
bash
# 1. clone
git clone https://github.com/mish-sakshi/Lab-Report-Flagger.git
cd Lab-Report-Flagger

# 2. (optional) virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. install Python deps
pip install -r requirements.txt

# 4. install the OCR engine (needed only for scanned PDFs)
sudo apt install -y tesseract-ocr     # macOS: brew install tesseract

# 5. run
streamlit run app.py

Then open the URL it prints (usually http://localhost:8501).

Make a test report: python make_sample.py creates sample_report.pdf you can upload.

✅ Tests & validation
bash
pytest -q          # unit tests (specific behaviours)
python validate.py # validation suite (accuracy on labelled cases)

The validation suite reports conclusion-level accuracy and pattern recall across labelled cases, and lists any mismatch — a safety net that catches regressions when ranges or rules change.

Honest note on "accuracy": the validation suite proves the engine is internally consistent and regression-safe against a labelled set. It is not a clinical certification — true clinical validation would require an independent, clinician-labelled dataset.

🧬 **How the reasoning works**
The engine keeps all reference ranges as data, so adding a test is a one-line change. Flags feed a small rule engine that reads several tests together — e.g. diabetes and reduced eGFR → Diabetic kidney disease — and a conclusion layer that escalates to immediate on panic values (critical glucose, severe anaemia, eGFR < 15), soon on a likely pattern, else routine.

🗺️ **Roadmap**
Qualitative urine dipstick handling (protein/glucose as negative/trace/+)
Trend tracking across multiple reports (needs opt-in storage)
A Doench-style on-target score… (kidding — wrong project); instead: expand the validation set with clinician review
More analytes (full CBC indices, thyroid panel, coagulation)

📄 **License & disclaimer**
For education and portfolio demonstration. Not a medical device and not for clinical use. No warranty. Reference ranges are illustrative and must not be used for diagnosis.
