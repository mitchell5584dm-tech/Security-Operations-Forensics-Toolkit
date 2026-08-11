import os, secrets, traceback, requests
from flask import Flask, request, jsonify, redirect
app = Flask(__name__)
def try_send_email(to_email, code):
    try:
        resend_key=os.getenv("RESEND_API_KEY","").strip()
        gmail_user=os.getenv("GMAIL_USER","").strip()
        if not resend_key:
            return False, "No RESEND_API_KEY"
        r=requests.post("https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {resend_key}", "Content-Type":"application/json"},
            json={"from": f"RetireSec <onboarding@resend.dev>", "to": [to_email], "subject": f"License {code}",
                  "html": f"<h1>✅ RetireSec Pro {code}</h1><p>Use: python3 credential_auditor_with_notifications.py --license {code}</p>"}, timeout=15)
        return r.status_code==200, f"{r.status_code}: {r.text[:400]}"
    except Exception as e:
        return False, f"{e}"
@app.route('/api/health')
def h(): return jsonify({"has_resend": bool(os.getenv("RESEND_API_KEY"))})
@app.route('/webhook/stripe', methods=['POST','GET'])
def w():
    email=request.args.get('email','mitchell5584.dm@gmail.com')
    data=request.get_json(silent=True) or {}
    try:
        obj=data.get('data',{}).get('object',{})
        email=obj.get('customer_email') or (obj.get('customer_details') or {}).get('email') or email
    except: pass
    code=f"PRO-{secrets.token_hex(3).upper()}-2026"
    sent,info=try_send_email(email,code)
    return jsonify({"email":email,"license":code,"emailed":sent,"info":info})
@app.route('/')
def index(): return redirect("https://mitchell5584dm-tech.github.io/Security-Operations-Forensics-Toolkit/")
@app.route('/buy/credentialauditor')
def buy(): return redirect("https://buy.stripe.com/5kQ14m2DQackeP687L5sA00")
