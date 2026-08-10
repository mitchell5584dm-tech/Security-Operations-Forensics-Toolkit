import os
from flask import Flask, request, jsonify, redirect
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)

# === YOUR TEST CODES ===
OWNER_CODES = {
    "TEST-14DAY-RETIRES-2026": 14,
    "RETIRESEC-OWNER-ALL-ACCESS": 3650,
    "FREETRIAL-MITCH-5584-2026": 14,
}

TRIALS = {}

@app.route('/')
def index():
    # REDIRECT to your real frontend - fixes blank screen
    return redirect("https://mitchell5584dm-tech.github.io/Security-Operations-Forensics-Toolkit/")

@app.route('/health')
def health():
    return "OK - RetireSec Running | Full API at /api/health"

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "LIVE",
        "version": "2.0 - With redirects & notifications",
        "time": datetime.utcnow().isoformat(),
        "frontend": "https://mitchell5584dm-tech.github.io/Security-Operations-Forensics-Toolkit/"
    })

@app.route('/start-trial/credentialauditor', methods=['GET','POST'])
def trial():
    if request.method == 'GET':
        return """
        <html><body style='font-family:system-ui;max-width:600px;margin:60px auto;text-align:center'>
        <h1>🚀 Start 14-Day Trial - RetireSec Pro</h1>
        <p>100% Offline - No credit card</p>
        <form method=POST>
        <input name='email' placeholder='Your email' required style='padding:12px;width:80%'><br><br>
        <button style='padding:14px 28px;background:#2563eb;color:white;border:0;border-radius:8px;font-weight:bold'>Get Trial Code</button>
        </form>
        <p>Owner test: TEST-14DAY-RETIRES-2026</p>
        </body></html>
        """
    email = request.form.get('email')
    code = f"TRIAL-{secrets.token_hex(3).upper()}-2026"
    TRIALS[code] = datetime.utcnow() + timedelta(days=14)
    return f"<h1>✅ Trial Active for {email}</h1><h2 style='background:#eee;padding:15px'>{code}</h2><p>Expires in 14 days</p><a href='/'>Home</a>"

@app.route('/buy/credentialauditor')
def buy():
    return "<h1>Buy $99/yr</h1><p>Stripe checkout enables after Stripe approval. Use RETIRESEC-OWNER-ALL-ACCESS to test.</p><a href='/start-trial/credentialauditor'>Try free instead</a>"

@app.route('/api/activate', methods=['POST'])
def activate():
    data = request.get_json() or request.form
    code = data.get('code','').upper().strip()
    if code in OWNER_CODES:
        days = OWNER_CODES[code]
        exp = datetime.utcnow() + timedelta(days=days)
        return jsonify({"valid": True, "code": code, "expiry": exp.isoformat(), "message": f"Owner access {days} days"})
    if code in TRIALS:
        return jsonify({"valid": True, "code": code, "expiry": TRIALS[code].isoformat()})
    return jsonify({"valid": False, "message": "Invalid code. Try TEST-14DAY-RETIRES-2026"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',10000)))
