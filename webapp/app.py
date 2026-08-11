import os, secrets, smtplib
from email.mime.text import MIMEText
from flask import Flask, request, jsonify, redirect
from datetime import datetime, timedelta
from pathlib import Path

app = Flask(__name__)
TRIALS={}
LICENSES={}
OWNER_CODES={"TEST-14DAY-RETIRES-2026":14,"RETIRESEC-OWNER-ALL-ACCESS":3650,"FREETRIAL-MITCH-5584-2026":14,"RETIRES-2026-OWNER":3650}

def send_license_email(to_email, code):
    user=os.getenv("GMAIL_USER")
    pwd=os.getenv("GMAIL_APP_PASSWORD","").replace(" ","")
    if not user or not pwd:
        print(f"NO CREDS - would email {to_email}: {code}")
        return False
    try:
        html=f"""<div style="font-family:system-ui;max-width:600px;margin:auto">
<h1 style="color:#16a34a">✅ RetireSec Pro Activated!</h1>
<p>Thanks for buying CredentialAuditor Pro $99/yr</p>
<div style="background:#000;color:#0f0;padding:20px;font-size:24px;border-radius:10px;text-align:center;font-family:monospace">{code}</div>
<p>Use: <code>python3 credential_auditor_with_notifications.py --license {code}</code></p>
<p>Download: https://mitchell5584dm-tech.github.io/Security-Operations-Forensics-Toolkit/</p>
<p>Cancel anytime: https://billing.stripe.com</p></div>"""
        msg=MIMEText(html,'html')
        msg['Subject']=f"Your RetireSec Pro License: {code}"
        msg['From']=user
        msg['To']=to_email
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as s:
            s.login(user,pwd)
            s.send_message(msg)
        print(f"EMAILED {to_email} -> {code}")
        return True
    except Exception as e:
        print(f"Email fail: {e}")
        return False

@app.route('/')
def index():
    return redirect("https://mitchell5584dm-tech.github.io/Security-Operations-Forensics-Toolkit/")

@app.route('/health')
def health():
    return "OK - Gmail configured" if os.getenv("GMAIL_USER") else "OK - NO GMAIL CREDS"

@app.route('/api/health')
def api_h():
    return jsonify({"status":"LIVE","gmail": bool(os.getenv("GMAIL_USER"))})

@app.route('/success')
@app.route('/success.html')
def success():
    # try multiple locations
    for p in [Path("success.html"), Path("webapp/success.html"), Path(__file__).parent/"success.html"]:
        if p.exists():
            return p.read_text()
    return "Success - file not found"

@app.route('/webhook/stripe', methods=['POST','GET'])
def webhook():
    data=request.get_json(silent=True) or {}
    email=None
    try:
        obj=data.get('data',{}).get('object',{})
        email=obj.get('customer_email') or (obj.get('customer_details') or {}).get('email') or obj.get('email')
    except:
        pass
    if not email:
        email=request.args.get('email') or "customer@example.com"
    code=f"PRO-{secrets.token_hex(3).upper()}-2026"
    LICENSES[email]=code
    send_license_email(email,code)
    return jsonify({"received":True,"email":email,"license":code,"emailed": bool(os.getenv("GMAIL_USER"))})

@app.route('/api/get-license/<email>')
def gl(email):
    code=LICENSES.get(email) or f"PRO-{secrets.token_hex(3).upper()}-2026"
    LICENSES[email]=code
    return f"<html><body style='text-align:center;margin-top:60px;font-family:system-ui'><h1>Your License: {code}</h1><p>For {email}</p><p>Check email too!</p></body></html>"

@app.route('/buy/credentialauditor')
def buy():
    return redirect("https://buy.stripe.com/5kQ14m2DQackeP687L5sA00")

@app.route('/api/activate', methods=['POST','GET'])
def activate():
    d=request.get_json(silent=True) or request.form or request.args
    c=str(d.get('code','')).upper().strip()
    valid = c in OWNER_CODES or c in TRIALS or c in LICENSES.values()
    return jsonify({"valid": valid, "code": c})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.getenv("PORT",10000)))
