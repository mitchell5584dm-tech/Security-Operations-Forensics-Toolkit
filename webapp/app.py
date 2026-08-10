import os
from flask import Flask, redirect

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html><head><title>RetireSec Workbench - App Running</title>
    <style>body{font-family:system-ui;padding:40px;max-width:700px;margin:0 auto}
    .card{border:1px solid #e2e8f0;border-radius:16px;padding:20px;margin:20px 0}
    .btn{padding:12px 18px;background:#2563eb;color:white;border-radius:10px;text-decoration:none;display:inline-block;margin:5px}
    </style></head><body>
    <h1>RetireSec Workbench - App is LIVE</h1>
    <p><strong>Security help for everyone.</strong> Small business model with hardcoded help for individuals, startups, non-profits, schools.</p>
    <div class="card">
    <h3>✅ Your Render App is Running</h3>
    <p>GitHub Pages: https://mitchell5584dm-tech.github.io/Security-Operations-Forensics-Toolkit/</p>
    <p>This is your backend for Stripe payments + license generation.</p>
    </div>
    <div class="card">
    <h3>Small Business Checklist - Hardcoded</h3>
    <ol><li>Run Password Health Check monthly</li><li>Remove ex-employees from admin</li><li>Test backup restore</li><li>Scan Linux logs</li><li>Check fake SaaS invoices</li></ol>
    </div>
    <p><a class="btn" href="/health">Health Check</a> <a class="btn" href="/">Home</a></p>
    <p style="color:#64748b;font-size:13px">Free tools stay free. Pro tool $99/yr. Built in retirement as busy work that helps.</p>
    </body></html>
    """

@app.route("/health")
def health():
    return "OK - RetireSec Running"

# Stripe placeholders - will work once you add keys in Render
@app.route("/start-trial/credentialauditor")
def trial():
    return redirect("/")

@app.route("/buy/credentialauditor")
def buy():
    return redirect("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
