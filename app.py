import streamlit as st
from llm import quick_ai_summary
from db import init_db, save_run, get_recent_runs, save_run_with_ai, get_ai_summary


st.set_page_config(page_title="AI Job Application Copilot", layout="wide")

init_db()

st.title("AI Job Application Copilot (v1)")
st.write("Step 2: Saving CV + JD runs into SQLite ✅")

with st.sidebar:
    st.header("Optional metadata")
    company = st.text_input("Company", value="")
    role_title = st.text_input("Role title", value="")

cv_text = st.text_area("CV text", height=250, placeholder="Paste CV text here…")
jd_text = st.text_area("Job description", height=250, placeholder="Paste job description here…")
store_ai = st.checkbox("Include AI summary when saving", value=True)


if st.button("Save this run"):
    if not cv_text.strip() or not jd_text.strip():
        st.error("Please paste both CV text and the job description.")
    else:
        if store_ai:
            summary = quick_ai_summary(cv_text.strip(), jd_text.strip())
            save_run_with_ai(company.strip(), role_title.strip(), cv_text.strip(), jd_text.strip(), summary)
        else:
            save_run(company.strip(), role_title.strip(), cv_text.strip(), jd_text.strip())
        st.success("Saved ✅ (to runs.db)")


if st.button("AI Analyse (quick)"):
    if not cv_text.strip() or not jd_text.strip():
        st.error("Please paste both CV text and the job description.")
    else:
        with st.spinner("Asking the AI..."):
            summary = quick_ai_summary(cv_text.strip(), jd_text.strip())
        st.subheader("AI summary")
        st.write(summary)


st.divider()
st.subheader("Recent saved runs")

rows = get_recent_runs(limit=10)
if not rows:
    st.info("No runs saved yet. Paste CV + JD and click 'Save this run'.")
else:
    st.table([{"run_id": r[0], "created_at": r[1], "company": r[2], "role_title": r[3]} for r in rows])

st.subheader("View AI summary for a run")

run_id = st.number_input("Enter run_id", min_value=1, step=1)

if st.button("Load AI summary"):
    summary = get_ai_summary(int(run_id))
    if summary:
        st.text_area("Saved AI summary", summary, height=250)
    else:
        st.warning("No AI summary found for this run_id (or it was saved without AI).")


