"""
pdf_extract.py - read a lab panel from a PDF report.

Strategy (robust against multi-page reports full of educational prose):
  * Work LINE BY LINE.
  * A value is accepted only when the test name is followed, on the SAME line,
    by a number AND a real unit (mg/dL, g/dL, %, ...). Result rows look like that;
    sentences in the notes pages do not, so prose no longer produces false values.
  * Native text layer first; OCR (PyMuPDF + Tesseract) for scanned PDFs;
    password passed through for locked files.

extract_panel(file_bytes, password=None) -> (panel_dict, notes_list, method)
OCR can still misread digits, so the app always shows the values for a quick review.
"""
import io
import re
import pdfplumber

try:
    import pymupdf
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except Exception:
    OCR_AVAILABLE = False

# Test name -> the many ways labs print it. Longer/more-specific aliases first.
SYNONYMS = {
    "glucose": ["fasting blood sugar", "fasting glucose", "glucose fasting", "fbs", "glucose"],
    "hba1c": ["hba1c", "glycosylated hemoglobin", "glycated haemoglobin", "a1c"],
    "hb": ["hemoglobin", "haemoglobin", "hgb"],
    "creatinine": ["creatinine"],
    "total_chol": ["total cholesterol", "cholesterol"],
    "ldl": ["ldl cholesterol", "ldl"],
    "hdl": ["hdl cholesterol", "hdl"],
    "triglycerides": ["triglycerides", "triglyceride"],
    "alt": ["alt (sgpt)", "sgpt", "alt"],
    "ast": ["ast (sgot)", "sgot", "ast"],
    "alp": ["alkaline phosphatase", "alp"],
    "bilirubin_total": ["total bilirubin"],
    "albumin": ["albumin"],
    "vitamin_d": ["25(oh) vitamin d", "25-oh vitamin d", "vitamin d"],
    "vitamin_b12": ["vitamin b12", "cobalamin", "b12"],
    "iron": ["serum iron", "iron"],
    "ferritin": ["ferritin"],
}

NUM = r"(\d{1,4}(?:\.\d{1,2})?)"
# A real unit must follow the number (this is what rejects prose).
UNIT = (r"\s*(?:mg/dl|g/dl|%|u/l|iu/l|miu/l|ng/ml|pg/ml|mmol/l|umol/l|"
        r"micro\s*g/dl|µg/dl|ug/dl|mg/l)")


def _native_text(src_bytes, password):
    with pdfplumber.open(io.BytesIO(src_bytes), password=password or "") as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


def _ocr_text(src_bytes, password):
    doc = pymupdf.open(stream=src_bytes, filetype="pdf")
    if doc.needs_pass and not doc.authenticate(password or ""):
        return None
    chunks = []
    for page in doc:
        pix = page.get_pixmap(dpi=220)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        chunks.append(pytesseract.image_to_string(img))
    return "\n".join(chunks)


def find_age_sex(text):
    age = sex = ""
    # Primary: a "Sex/Age : Male / 41 Y" style patient line.
    m = re.search(r"sex\s*/\s*age\s*:?\s*(male|female)\s*/\s*(\d{1,3})", text, re.I)
    if m:
        sex = "M" if m.group(1).lower() == "male" else "F"
        age = m.group(2)
        return age, sex
    # Fallbacks.
    m = re.search(r"\b(male|female)\b", text, re.I)
    if m:
        sex = "M" if m.group(1).lower() == "male" else "F"
    m = re.search(r"(?:age\b[^\d\n]{0,10})?(\d{1,3})\s*(?:years|yrs|y\b)", text, re.I)
    if m:
        age = m.group(1)
    return age, sex


def find_value(text, aliases):
    """Line-by-line: accept 'alias ... number unit' on one line. Unit required."""
    lines = text.splitlines()
    for alias in sorted(aliases, key=len, reverse=True):
        pat = re.compile(r"(?<![A-Za-z])" + re.escape(alias) + r"(?![A-Za-z])"
                         + r"[^\d\n]{0,25}?" + NUM + UNIT, re.I)
        for line in lines:
            m = pat.search(line)
            if m:
                return float(m.group(1))
    return None


def _parse(text):
    panel = {}
    age, sex = find_age_sex(text)
    if age:
        panel["age"] = age
    if sex:
        panel["sex"] = sex
    for key, aliases in SYNONYMS.items():
        v = find_value(text, aliases)
        if v is not None:
            panel[key] = v
    return panel


def extract_panel(src, password=None):
    src_bytes = bytes(src) if isinstance(src, (bytes, bytearray)) else src.read()
    text = ""
    try:
        text = _native_text(src_bytes, password)
    except Exception as e:
        text = ""
        if "password" in str(e).lower() or "encrypt" in str(e).lower():
            return {}, ["This PDF is password-protected. Enter its password and try again."], "locked"

    if len(text.strip()) >= 20:
        return _parse(text), ["Read from the PDF text layer. Please review every value below."], "text"

    if not OCR_AVAILABLE:
        return {}, ["This looks like a scanned PDF and OCR isn't installed. "
                    "Install Tesseract (see README) or type the values."], ""
    ocr = _ocr_text(src_bytes, password)
    if ocr is None:
        return {}, ["This PDF is password-protected. Enter its password and try again."], "locked"
    panel = _parse(ocr)
    note = ("Read by OCR from a scanned report. OCR can misread digits, so CHECK every value."
            if panel else
            "OCR could not read values from this report. Please type them.")
    return panel, [note], "ocr"
