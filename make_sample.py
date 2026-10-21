from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

c = canvas.Canvas("sample_report.pdf", pagesize=A4)
y = 800
for line in [
    "CITY DIAGNOSTICS LAB",
    "Patient: Asha Verma    Age: 58 Years    Sex: Female", "",
    "Glucose, Fasting (FBS)   168   mg/dL   70 - 99",
    "HbA1c (HPLC)   7.9   %   4.0 - 5.6",
    "Haemoglobin   10.8   g/dL   12.0 - 15.5",
    "Creatinine, Serum   1.7   mg/dL   0.59 - 1.04",
    "Total Cholesterol   240   mg/dL   < 200",
    "HDL Cholesterol   38   mg/dL   > 40",
    "Triglycerides   190   mg/dL   < 150",
    "Ferritin   9   ng/mL   11 - 307",
]:
    c.drawString(60, y, line); y -= 20
c.save()
print("sample_report.pdf created")
