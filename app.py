import os, secrets, requests
from flask import Flask, request, jsonify, redirect, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/ping')
def ping():
    return jsonify({"status": "alive"})

def try_send_email(to_email, code):
    k = os.getenv("RESEND_API_KEY", "").strip()
    try:
        r = requests.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {k}", "Content-Type": "application/json"},
            json={
                "from": "RetireSec <onboarding@resend.dev>",
                "to": [to_email],
                "subject": f"Your RetireSec License {code}",
                "html": f"""
                <h1>✅ RetireSec Pro Active: {code}</h1>
                <p>Thanks for subscribing!</p>
                <p><b>License:</b> {code}</p>
                <p>Use: <code>python3 credential_auditor_with_notifications.py --license {code}</code></p>
                <p>Keep this email safe.</p>
                <p><a href="https://security-operations-forensics-toolkit.onrender.com">Return to RetireSec Workbench</a></p>
                """
            }, timeout=15)
        return r.status_code == 200, f"{r.status_code}: {r.text[:400]}"
    except Exception as e:
        return False, str(e)

@app.route('/success')
def success():
    return """
    <html><head><meta charset="utf-8"><title>Payment Success — RetireSec Workbench</title>
    <style>body{font-family:system-ui,sans-serif;text-align:center;padding:60px 20px;background:#f8
