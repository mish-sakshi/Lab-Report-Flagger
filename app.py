import streamlit as st
import pandas as pd
import altair as alt
import json
from fhir_export import build_fhir_bundle
from lab_engine import REFERENCE, get_range, build_result
from pdf_extract import extract_panel

st.set_page_config(page_title="Read Your Report - A Lab Report Flagger", page_icon="🩸", layout="wide")

LEVEL = {"immediate": ("#fdecea", "#b3261e", "🚨"),
         "soon": ("#fff4e5", "#9a6700", "⚠️"),
         "routine": ("#e6f4ea", "#1e7e34", "✅")}
FLAGCOLOR = {"Normal": "#2e7d32", "Low": "#1565c0", "High": "#e65100"}
LABEL2KEY = {meta["label"]: k for k, meta in REFERENCE.items()}

st.title("🩸 Read Your Report - Lab Report Flagger")
st.caption("Upload a report (PDF or scan) or type your values — get flagged results, "
           "what they mean, and whether to see a doctor.")
st.info("**Educational screening only — not a diagnosis.**Currently available for Blood checkups/Urine/Sugar/LFT/vitamine checkups. Ranges are standard adult values "
        "and vary by lab. Always consult a doctor. In an emergency, seek care immediately.", icon="ℹ️")

if "panel" not in st.session_state:
    st.session_state.panel = {}

# sidebar
with st.sidebar:
    st.header("1 · Enter results")
    mode = st.radio("Method", ["Upload a report", "Type my values"])
    if mode == "Upload a report":
        up = st.file_uploader("Lab report (PDF — native or scanned)", type=["pdf"])
        pwd = st.text_input("PDF password (if locked)", type="password")
        if up is not None:
            with st.spinner("Reading your report…"):
                panel, notes, method = extract_panel(up.read(), pwd or None)
            st.session_state.panel = {k: str(v) for k, v in panel.items()}
            for n in notes:
                if method == "text":
                    st.success(n)
                else:
                    st.warning(n)
            badge = {"text": "📄 Read from PDF text", "ocr": "🔍 Read by OCR (scan)",
                     "locked": "🔒 Locked", "": "⚠️ Not read"}.get(method, "")
            if badge:
                st.caption(badge)

    st.divider()
    p = st.session_state.panel
    st.header("2 · Your details")
    age = st.text_input("Age (years)", value=p.get("age", ""))
    sex = st.radio("Sex", ["M", "F"], index=0 if p.get("sex", "M") != "F" else 1, horizontal=True)

#  review + analyse
p = st.session_state.panel
st.subheader("Review your values")
st.caption("Values from your report are pre-filled — edit any cell, add blanks, then Analyse.")

grid = []
for key, meta in REFERENCE.items():
    lo, hi = get_range(key, sex)
    grid.append({"Test": meta["label"], "Your value": p.get(key, ""),
                 "Unit": meta["unit"], "Normal range": f"{lo}–{hi}"})
edited = st.data_editor(pd.DataFrame(grid), hide_index=True, use_container_width=True,
                        disabled=["Test", "Unit", "Normal range"], key="grid",
                        column_config={"Your value": st.column_config.TextColumn("Your value", width="medium")})

analyse = st.button("🔬 Analyse my report", type="primary", use_container_width=True)

if analyse:
    entered = {}
    for _, row in edited.iterrows():
        v = str(row["Your value"]).strip()
        if v:
            entered[LABEL2KEY[row["Test"]]] = v
    if not entered:
        st.error("Please enter at least one test value.")
        st.stop()
    panel = {"sex": sex, **entered}
    if age.strip():
        panel["age"] = age.strip()
    try:
        r = build_result(panel)
    except ValueError as e:
        st.error(f"Could not read a value: {e}. Please make sure every value is a number.")
        st.stop()

    # Conclusion banner
    c = r["conclusion"]
    bg, fg, icon = LEVEL[c["level"]]
    st.markdown(f"<div style='background:{bg};border-left:7px solid {fg};padding:18px;border-radius:10px'>"
                f"<div style='font-size:1.25rem;font-weight:700;color:{fg}'>{icon} {c['headline']}</div>"
                f"<div style='margin-top:6px;color:#333'>{c['advice']}</div></div>", unsafe_allow_html=True)

    #  Metrics 
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Tests analysed", len(r["results"]))
    m2.metric("Outside range", r["abnormal_count"])
    m3.metric("eGFR", f"{r['egfr']:.0f}" if r["egfr"] is not None else "—",
              help=r["ckd_stage"] or "needs age + creatinine")
    m4.metric("Urgency", c["level"].capitalize())

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🚩 Flag details", "🧩 Patterns", "⬇️ Download"])

    #  TAB 1: interactive severity chart
    with tab1:
        chart_rows = []
        for x in r["results"]:
            lo, hi = get_range(x["key"], r["sex"])
            if x["flag"] == "High" and hi > 0:
                sev = x["value"] / hi
            elif x["flag"] == "Low" and x["value"] > 0:
                sev = lo / x["value"]
            else:
                sev = 1.0
            chart_rows.append({"Test": x["label"], "Severity": round(sev, 2), "Value": x["value"],
                               "Unit": x["unit"], "Normal": x["range"], "Flag": x["flag"],
                               "Meaning": x["meaning"]})
        cdf = pd.DataFrame(chart_rows)
        st.caption("How far each value sits relative to its normal limit (1.0 = right at the limit). Hover for details.")
        base = alt.Chart(cdf).encode(
            y=alt.Y("Test:N", sort="-x", title=None),
            x=alt.X("Severity:Q", title="× of normal limit"),
            color=alt.Color("Flag:N", scale=alt.Scale(domain=list(FLAGCOLOR), range=list(FLAGCOLOR.values())),
                            legend=alt.Legend(title="Flag")),
            tooltip=["Test", "Value", "Unit", "Normal", "Flag", "Meaning"])
        rule = alt.Chart(pd.DataFrame({"x": [1.0]})).mark_rule(strokeDash=[4, 4], color="#888").encode(x="x:Q")
        st.altair_chart((base.mark_bar() + rule).properties(height=28 * len(cdf) + 40), use_container_width=True)
        if r["egfr"] is not None:
            st.info(f"**Kidney function (eGFR):** {r['egfr']:.0f} mL/min — {r['ckd_stage']}")

    # TAB 2: colour table + meanings
    with tab2:
        loincs = {x["label"]: x["loinc"][0] for x in r["results"]}
        tbl = cdf.copy()
        tbl["LOINC"] = tbl["Test"].map(loincs)
        df = tbl[["Test", "Value", "Unit", "Normal", "Flag", "LOINC"]]

        def paint(v):
            return {"High": "background-color:#fff4e5", "Low": "background-color:#e7f0ff",
                    "Normal": "background-color:#e6f4ea"}.get(v, "")
        st.dataframe(df.style.map(paint, subset=["Flag"]), hide_index=True, use_container_width=True)
        st.markdown("**What the flags mean**")
        any_abn = False
        for x in r["results"]:
            if x["flag"] != "Normal":
                any_abn = True
                st.markdown(f"- **{x['label']} ({x['flag']})** — {x['meaning']}")
        if not any_abn:
            st.success("Every value is within its normal range.")

    # TAB 3: patterns
    with tab3:
        for name, conf, ev in r["patterns"]:
            if name.startswith("No clear"):
                st.success("No clear disease pattern — values support a healthy panel.")
            else:
                with st.expander(f"{name}  ·  {conf}", expanded=True):
                    for e in ev:
                        st.write(f"• {e}")
        st.caption("Patterns read several tests together — leads to discuss with a doctor, not diagnoses.")

    #  TAB 4: download 
    with tab4:
        lines = [f"LAB REPORT FLAGGER — result ({r['sex']}, {r['age'] or '?'}y)",
                 f"Ruleset: {r['ruleset']}", ""]
        for x in r["results"]:
            lines.append(f"{x['label']}: {x['value']:g} {x['unit']} (normal {x['range']}) -> {x['flag']}")
            if x["flag"] != "Normal":
                lines.append(f"   meaning: {x['meaning']}")
        if r["egfr"] is not None:
            lines.append(f"\neGFR: {r['egfr']:.0f} ({r['ckd_stage']})")
        lines += ["", f"CONCLUSION [{c['level'].upper()}]: {c['headline']}", c["advice"], "",
                  "Educational screening only — not a diagnosis."]
        st.download_button("⬇️ Download result (.txt)", "\n".join(lines),
                           file_name="lab_result.txt", use_container_width=True)
        bundle = build_fhir_bundle(r)
        st.download_button("🏥 Download FHIR bundle (.json)", json.dumps(bundle, indent=2),
                           file_name="lab_result_fhir.json", mime="application/json",
                           use_container_width=True)
        st.caption("FHIR R4 Bundle with LOINC-coded Observations — importable by health systems (Apple Health, EHRs).")
        with st.expander("Preview FHIR JSON"):
            st.json(bundle)

    st.caption(f"Ruleset: {r['ruleset']}. Your data is processed in memory and not stored.")

