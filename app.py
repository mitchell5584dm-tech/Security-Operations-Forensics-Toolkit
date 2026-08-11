import os, secrets, requests
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

def try_send_email(to_email, code):
    k=os.getenv("RESEND_API_KEY","").strip()
    try:
        r=requests.post("https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {k}", "Content-Type":"application/json"},
            json={
                "from":"RetireSec <onboarding@resend.dev>",
                "to":[to_email],
                "subject":f"Your RetireSec License {code}",
                "html": f"""
                <h1>✅ RetireSec Pro Active: {code}</h1>
                <p>Thanks for subscribing!</p>
                <p><b>License:</b> {code}</p>
                <p>Use: <code>python3 credential_auditor_with_notifications.py --license {code}</code></p>
                <p>Keep this email.</p>
                """
            }, timeout=15)
        return r.status_code==200, f"{r.status_code}: {r.text[:400]}"
    except Exception as e:
        return False, str(e)

@app.route('/')
def index():
    return redirect("https://mitchell5584dm-tech.github.io/Security-Operations-Forensics-Toolkit/")

@app.route('/success')
def success():
    return """
    <html><body style='font-family:sans-serif;text-align:center;padding:50px'>
    <h1>✅ Payment Success!</h1>
    <p>Check your email for license key.</p>
    <p>License sent from RetireSec Workbench.</p>
    <a href='https://mitchell5584dm-tech.github.io/Security-Operations-Forensics-Toolkit/'>Back to Toolkit</a>
    </body></html>
    """

@app.route('/cancel')
def cancel():
    return "<h1>Payment canceled</h1><a href='/'>Try again</a>"

@app.route('/api/health')
def health():
    return jsonify({"has_resend": bool(os.getenv("RESEND_API_KEY")), "status":"ok"})

@app.route('/webhook/stripe', methods=['POST','GET'])
def webhook():
    data=request.get_json(silent=True) or {}
    email=request.args.get('email','mitchell5584.dm@gmail.com')
    try:
        obj=data.get('data',{}).get('object',{})
        email=obj.get('customer_email') or (obj.get('customer_details') or {}).get('email') or email
        if not email:
            email=obj.get('email') or email
    except: pass
    code=f"PRO-{secrets.token_hex(3).upper()}-2026"
    sent,info=try_send_email(email,code)
    return jsonify({"email":email,"license":code,"emailed":sent,"info":info})

@app.route('/buy/credentialauditor')
def buy():
    return redirect("https://buy.stripe.com/5kQ14m2DQackeP687L5sA00")

if __name__ == '__main__':
    app.run()
