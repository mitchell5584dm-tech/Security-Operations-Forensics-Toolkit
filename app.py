import os, secrets, requests
from flask import Flask, request, jsonify, redirect
app = Flask(__name__)
def try_send_email(to_email, code):
    k=os.getenv("RESEND_API_KEY","").strip()
    r=requests.post("https://api.resend.com/emails", headers={"Authorization": f"Bearer {k}", "Content-Type":"application/json"},
        json={"from":"RetireSec <onboarding@resend.dev>","to":[to_email],"subject":f"License {code}","html":f"<h1>License {code}</h1>"}, timeout=15)
    return r.status_code==200, f"{r.status_code}: {r.text[:300]}"
@app.route('/api/health')
def h(): return jsonify({"has_resend": bool(os.getenv("RESEND_API_KEY"))})
@app.route('/webhook/stripe', methods=['POST','GET'])
def w():
    import secrets
    d=request.get_json(silent=True) or {}
    email=request.args.get('email','mitchell5584.dm@gmail.com')
    try: email=d.get('data',{}).get('object',{}).get('customer_email') or email
    except: pass
    code=f"PRO-{secrets.token_hex(3).upper()}-2026"
    sent,info=try_send_email(email,code)
    return jsonify({"email":email,"license":code,"emailed":sent,"info":info})
@app.route('/')
def index(): return redirect("https://mitchell5584dm-tech.github.io/Security-Operations-Forensics-Toolkit/")
