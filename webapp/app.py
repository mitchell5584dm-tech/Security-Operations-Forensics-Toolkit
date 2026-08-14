import os, secrets, requests
from flask import Flask, request, jsonify, redirect, send_from_directory

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index_render.html')

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
                "html": f"<h1>✅ RetireSec Pro Active: {code}</h1><p><b>License:</b> {code}</p>"
            }, timeout=15)
        return r.status_code == 200, f"{r.status_code}: {r.text[:400]}"
    except Exception as e:
        return False, str(e)

@app.route('/success')
def success():
    return """<html><head><meta charset="utf-8"><title>Payment Success — RetireSec</title>
    <style>body{font-family:system-ui,sans-serif;text-align:center;padding:60px 20px;background:#f8fafc}
    .card{background:white;border:1px solid #e2e8f0;border-radius:16px;padding:40px;max-width:480px;margin:0 auto}
    h1{color:#16a34a}p{color:#475569;line-height:1.6}
    a{display:inline-block;margin-top:20px;background:#0f172a;color:white;padding:12px 24px;border-radius:10px;text-decoration:none;font-weight:700}
    </style></head><body><div class="card">
    <h1>✅ Payment Successful!</h1>
    <p>Your license will arrive in your inbox within a few minutes.</p>
    <a href="https://security-operations-forensics-toolkit.onrender.com">← Back to RetireSec</a>
    </div></body></html>"""

@app.route('/cancel')
def cancel():
    return """<html><head><meta charset="utf-8"><title>Cancelled — RetireSec</title>
    <style>body{font-family:system-ui,sans-serif;text-align:center;padding:60px 20px;background:#f8fafc}
    .card{background:white;border:1px solid #e2e8f0;border-radius:16px;padding:40px;max-width:480px;margin:0 auto}
    h1{color:#64748b}p{color:#475569;line-height:1.6}
    a{display:inline-block;margin-top:14px;background:#0f172a;color:white;padding:12px 24px;border-radius:10px;text-decoration:none;font-weight:700}
    </style></head><body><div class="card">
    <h1>Payment Cancelled</h1>
    <p>No charge was made. Start your 14-day free trial anytime.</p>
    <a href="https://security-operations-forensics-toolkit.onrender.com">← Back to RetireSec</a>
    </div></body></html>"""

@app.route('/api/health')
def health():
    return jsonify({"has_resend": bool(os.getenv("RESEND_API_KEY")), "status": "ok"})

@app.route('/webhook/stripe', methods=['POST', 'GET'])
def webhook():
    data = request.get_json(silent=True) or {}
    email = request.args.get('email', 'mitchell5584.dm@gmail.com')
    try:
        obj = data.get('data', {}).get('object', {})
        email = (obj.get('customer_email') or
                 (obj.get('customer_details') or {}).get('email') or
                 obj.get('email') or email)
    except Exception:
        pass
    code = f"PRO-{secrets.token_hex(3).upper()}-2026"
    sent, info = try_send_email(email, code)
    return jsonify({"email": email, "license": code, "emailed": sent, "info": info})

@app.route('/buy/credentialauditor')
def buy():
    return redirect("https://buy.stripe.com/5kQ14m2DQackeP687L5sA00")

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
