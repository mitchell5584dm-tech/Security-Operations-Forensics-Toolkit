import os, secrets, traceback
from flask import Flask, request, jsonify, redirect
from pathlib import Path

app = Flask(__name__)
LICENSES={}

def try_send_email(to_email, code):
    try:
        import smtplib
        from email.mime.text import MIMEText
        user=os.getenv("GMAIL_USER","").strip()
        pwd=os.getenv("GMAIL_APP_PASSWORD","").replace(" ","").strip()
        if not user or not pwd:
            return False, "No creds set"
        html=f"""<div style="font-family:system-ui;max-width:600px;margin:auto">
<h1 style="color:#16a34a">✅ RetireSec Pro Activated!</h1>
<p>Thanks for buying CredentialAuditor Pro $99/yr</p>
<div style="background:#000;color:#0f0;padding:20px;font-size:24px;border-radius:10px;text-align:center;font-family:monospace">{code}</div>
<p>Download: https://mitchell5584dm-tech.github.io/Security-Operations-Forensics-Toolkit/</p>
<p>Use: python3 credential_auditor_with_notifications.py --license {code}</p></div>"""
        msg=MIMEText(html,'html')
        msg['Subject']=f"Your RetireSec Pro License: {code}"
        msg['From']=user
        msg['To']=to_email
        with smtplib.SMTP_SSL('smtp.gmail.com',465, timeout=10) as s:
            s.login(user,pwd)
            s.send_message(msg)
        return True, "sent"
    except Exception as e:
        return False, f"{e} | {traceback.format_exc()[:500]}"

@app.route('/')
def index():
    return redirect("https://mitchell5584dm-tech.github.io/Security-Operations-Forensics-Toolkit/")

@app.route('/health')
def health():
    return f"OK - Gmail: {bool(os.getenv('GMAIL_USER'))} - {os.getenv('GMAIL_USER','')}"

@app.route('/api/health')
def api_h():
    return jsonify({"status":"LIVE","gmail_user": os.getenv("GMAIL_USER",""), "has_pwd": bool(os.getenv("GMAIL_APP_PASSWORD"))})

@app.route('/webhook/stripe', methods=['POST','GET'])
def webhook():
    try:
        data=request.get_json(silent=True) or {}
        email="mitchell5584.dm@gmail.com"
        try:
            obj=data.get('data',{}).get('object',{})
            email=obj.get('customer_email') or (obj.get('customer_details') or {}).get('email') or obj.get('email') or email
        except: pass
        email=request.args.get('email', email)
        if "@" not in email:
            email="mitchell5584.dm@gmail.com"
        code=f"PRO-{secrets.token_hex(3).upper()}-2026"
        LICENSES[email]=code
        sent, info = try_send_email(email, code)
        return jsonify({"received":True,"email":email,"license":code,"emailed":sent,"info":info})
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()[:1000]}), 500

@app.route('/buy/credentialauditor')
def buy():
    return redirect("https://buy.stripe.com/5kQ14m2DQackeP687L5sA00")

@app.route('/success')
def success():
    return "<h1>Success! Check email for license</h1>"

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.getenv("PORT",10000)))
