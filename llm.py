def quick_ai_summary(cv_text: str, jd_text: str) -> str:
    return """Fit score: 72/100

Strengths:
- Strong SQL and analytics experience
- Experience with dashboards and stakeholders
- Public sector domain knowledge

Gaps:
- Limited dbt experience → build 2 models
- No Airflow mentioned → add a small pipeline
- Cloud depth unclear → highlight BigQuery usage

Next action:
- Tailor CV bullets to emphasise automation + scale
"""

"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def quick_ai_summary(cv_text: str, jd_text: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful career-focused data analyst assistant. Be concise."},
            {"role": "user", "content": f"""
"""Given the CV and Job Description, output:
- Fit score (0-100)
- 5 required skills from the JD
- 3 strongest matching points from the CV
- 3 gaps + a concrete next action for each

CV:
{cv_text}

Job Description:
{jd_text}
""" """}
        ],
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip() """
