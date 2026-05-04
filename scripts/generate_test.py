import os
import random
import datetime
import requests
import smtplib
from email.message import EmailMessage

# ===== ENVIRONMENT VARIABLES =====
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_ADDRESS")
EMAIL_PASS = os.getenv("EMAIL_APP_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")

TOPICS_FILE = "topics/embedded_topics.txt"

def load_topics():
    with open(TOPICS_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def build_prompt(topics):
    return f"""
Generate EXACTLY 15 embedded systems interview questions.
Level: M.Tech fresher to intermediate.
Mix of theory, coding, and scenario-based questions.

Topics:
{", ".join(topics)}

Return only numbered questions.
"""

def call_deepseek(prompt):
    response = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers={
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        }
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def send_email(questions):
    today = datetime.date.today().strftime("%d %B %Y")

    msg = EmailMessage()
    msg["Subject"] = f"Embedded Daily Interview Test – {today}"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg.set_content(
        f"""Hello Krishna,

Here is your Embedded Systems Daily Interview Test ({today}):

{questions}

Best of luck with your preparation!
"""
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASS)
        server.send_message(msg)

def main():
    topics = load_topics()
    selected_topics = random.sample(topics, min(12, len(topics)))
    prompt = build_prompt(selected_topics)
    questions = call_deepseek(prompt)
    send_email(questions)
    print("✅ Daily embedded test emailed successfully")

if __name__ == "__main__":
    main()
