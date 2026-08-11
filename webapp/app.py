import os
from flask import Flask, request, jsonify, redirect
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)

OWNER_CODES = {
    "TEST-14DAY-RETIRES-2026": 14,
    "RETIRESEC-OWNER-ALL-ACCESS": 3650,
    "FREETRIAL-MITCH-5584-2026": 14,
    "RETIRES-2026-OWNER": 3650,
}

TRIALS = {}

@app.route('/')
def index():
    return redirect("https://mitchell5584dm-tech.github.io/Security-Operations-Forensics-Toolkit/")

@app.route('/health')
def health():
    return "OK - RetireSec Running | See /api/health for details"

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "LIVE",
        "version": "2.0 - With Redirect",
        "time": datetime.utcnow().isoformat(),
        "frontend": "https://mitchell5584dm-tech.github.io/Security-Operations-Forensics-Toolkit/"
    })

@app.route('/start-trial/credentialauditor', methods=['GET','POST'])
def trial():
    if request.method == 'GET':
        return """
        <html><body style='font-family:system-ui;max-width:600px;margin:60px auto;text-align:center'>
        <h1>Start 14-Day Trial - RetireSec Pro</h1>
        <p>100% Offline - No credit card required</p>
        <form method=POST>
        <input name='email' placeholder='Your email' required style='padding:12px;width:80%'><br><br>
        <button style='padding:14px 28px;background:#2563eb;color:white;border:0;border-radius:8px;font-weight:bold;font-size:16px'>Get Trial Code</button>
        </form>
        <p style='margin-top:30px;color:#666'>Owner test code: <b>TEST-14DAY-RETIRES-2026</b></p>
        </body></html>
        """
    email = request.form.get('email','user')
    code = f"TRIAL-{secrets.token_hex(3).upper()}-2026"
    TRIALS[code] = datetime.utcnow() + timedelta(days=14)
    return f"<html><body style='font-family:system-ui;text-align:center;margin-top:80px'><h1>Trial Active for {email}</h1><h2 style='background:#f3f4f6;padding:20px;border-radius:10px;display:inline-block'>{code}</h2><p>Expires in 14 days</p></body></html>"

@app.route('/buy/credentialauditor')
def buy():
    return """
    <html><body style='font-family:system-ui;text-align:center;margin-top:80px'>
    <h1>Buy RetireSec Pro - $99/year</h1>
    <p>Stripe checkout enables after approval</p>
    <p>Use code: <b>RETIRESEC-OWNER-ALL-ACCESS</b> to test full access now</p>
    <br><a href='/start-trial/credentialauditor'>Start 14-Day Free Trial Instead</a>
    </body></html>
    """

@app.route('/api/activate', methods=['POST','GET'])
def activate():
    data = request.get_json(silent=True) or request.form or request.args
    code = str(data.get('code','')).upper().strip()
    if code in OWNER_CODES:
        days = OWNER_CODES[code]
        exp = datetime.utcnow() + timedelta(days=days)
        return jsonify({"valid": True, "code": code, "days": days, "expiry": exp.isoformat(), "message": "Owner access valid"})
    if code in TRIALS:
        return jsonify({"valid": True, "code": code, "expiry": TRIALS[code].isoformat(), "message": "Trial valid"})
    return jsonify({"valid": False, "message": "Invalid code. Try TEST-14DAY-RETIRES-2026"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

@app.route('/success.html')
@app.route('/success')
def success_page():
    return open('success.html').read()
