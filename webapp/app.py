import os, secrets, requests
from flask import Flask, request, jsonify, redirect, send_from_directory

app = Flask(__name__)

# ── Serve index.html at root — no GitHub Pages redirect ──
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# ── Keep-alive ping — called every 14 min by index.html JS ──
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
                <p><a href="https://security-operations-forensics-toolkit.onrender.com">
                Return to RetireSec Workbench</a></p>
                """
            }, timeout=15)
        return r.status_code == 200, f"{r.status_code}: {r.text[:400]}"
    except Exception as e:
        return False, str(e)

@app.route('/success')
def success():
    return """
    <html><head><meta charset="utf-8"><title>Payment Success — RetireSec</title>
    <style>body{font-family:system-ui,sans-serif;text-align:center;padding:60px 20px;background:#f8fafc}
    .card{background:white;border:1px solid #e2e8f0;border-radius:16px;padding:40px;max-width:480px;margin:0 auto}
    h1{color:#16a34a}p{color:#475569;line-height:1.6}
    a{display:inline-block;margin-top:20px;background:#0f172a;color:white;padding:12px 24px;border-radius:10px;text-decoration:none;font-weight:700}
    </style></head><body><div class="card">
    <h1>✅ Payment Successful!</h1>
    <p>Your RetireSec Pro license is being generated and will arrive in your inbox within a few minutes.</p>
    <p><strong>Check your email</strong> for your license key and activation instructions.</p>
    <a href="https://security-operations-forensics-toolkit.onrender.com">← Back to RetireSec Workbench</a>
    </div></body></html>"""

@app.route('/cancel')
def cancel():
    return """
    <html><head><meta charset="utf-8"><title>Cancelled — RetireSec</title>
    <style>body{font-family:system-ui,sans-serif;text-align:center;padding:60px 20px;background:#f8fafc}
    .card{background:white;border:1px solid #e2e8f0;border-radius:16px;padding:40px;max-width:480px;margin:0 auto}
    h1{color:#64748b}p{color:#475569;line-height:1.6}
    a{display:inline-block;margin-top:14px;background:#0f172a;color:white;padding:12px 24px;border-radius:10px;text-decoration:none;font-weight:700}
    </style></head><body><div class="card">
    <h1>Payment Cancelled</h1>
    <p>No worries — no charge was made. Start your 14-day free trial anytime, no credit card required.</p>
    <a href="https://security-operations-forensics-toolkit.onrender.com">← Back to RetireSec Workbench</a>
    </div></body></html>"""

@app.route('/api/health')
def health
