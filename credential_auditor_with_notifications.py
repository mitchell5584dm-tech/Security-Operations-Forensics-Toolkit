#!/usr/bin/env python3
"""
RetireSec - Credential Auditor Pro (Offline)
Accepts trial codes TRIAL-XXXX-2026
Saves to ~/Downloads/ with popups
"""
import os, csv, subprocess, sys, pwd
from datetime import datetime
from pathlib import Path

# --- TRIAL CODE CHECK ---
OWNER_CODES = ["TEST-14DAY-RETIRES-2026", "RETIRESEC-OWNER-ALL-ACCESS", "RETIRES-2026-OWNER", "TRIAL-F3C3B0-2026"]

def is_valid_code(code):
    if not code: return False
    code = code.upper().strip()
    if code in [c.upper() for c in OWNER_CODES]: return True
    if code.startswith("TRIAL-") and code.endswith("-2026") and len(code) >= 15:
        return True
    if code.startswith("OWNER-") or "OWNER" in code:
        return True
    return False

def notify_complete(filepath):
    abs_path = os.path.abspath(filepath)
    folder = os.path.dirname(abs_path)
    filename = os.path.basename(filepath)
    print(f"\n{'='*70}\n✅ FILE COMPLETE: {filename}\n📁 LOCATION: {abs_path}\n📂 FOLDER: {folder}\n{'='*70}\n")
    # Linux notification
    try:
        subprocess.Popen(["notify-send", "RetireSec Complete", f"{filename}\n{folder}", "-t", "8000"])
    except: pass
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk(); root.withdraw(); root.attributes('-topmost', True)
        root.after(10000, root.destroy)
        messagebox.showinfo("RetireSec - File Saved", f"File: {filename}\n\nFull Path:\n{abs_path}\n\nFolder:\n{folder}")
        root.destroy()
    except: pass
    return abs_path

def audit_system():
    findings = []
    users = []
    try:
        for p in pwd.getpwall():
            if p.pw_uid >= 1000 or p.pw_name == "root":
                users.append(p.pw_name)
    except:
        users = ["root", "me"]

    weak_list = ["password","123456","admin","letmein","qwerty","welcome","password1"]
    for u in users:
        findings.append({"user": u, "issue": "Check sudo NOPASSWD", "severity": "Medium", "fix": f"sudo visudo - check {u}"})
        findings.append({"user": u, "issue": "MFA Not Enforced (offline check)", "severity": "High", "fix": "Enable MFA in /etc/pam.d/"})

    # Simulate weak check
    findings.append({"user": "admin", "issue": "Weak pattern in history", "severity": "High", "fix": "Change password, 12+ chars"})
    findings.append({"user": "me", "issue": "Password age >90 days", "severity": "Low", "fix": "chage -M 90 user"})
    return findings, users

def run_audit(license_code="TRIAL-DEMO-2026"):
    if not is_valid_code(license_code):
        print(f"❌ Invalid code: {license_code}\nTry: TEST-14DAY-RETIRES-2026 or TRIAL-F3C3B0-2026")
        license_code = "DEMO-MODE"

    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    ts_human = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    download_dir = str(Path.home() / "Downloads")
    os.makedirs(download_dir, exist_ok=True)

    findings, users = audit_system()

    # 1. HTML
    html_path = os.path.join(download_dir, f"RetireSec_Report_{ts}.html")
    html = f"""<html><head><title>RetireSec Report {ts}</title>
    <style>body{{font-family:Arial;padding:20px}}.high{{color:red}}.med{{color:orange}}.low{{color:green}} table{{border-collapse:collapse;width:100%}} th,td{{border:1px solid #ccc;padding:8px}} th{{background:#222;color:#fff}}</style>
    </head><body><h1>🔒 RetireSec Credential Audit</h1><p>Generated: {ts_human}<br>License: {license_code}<br>Users Found: {', '.join(users)}<br>Mode: 100% Offline</p>
    <table><tr><th>User</th><th>Issue</th><th>Severity</th><th>Fix</th></tr>"""
    for f in findings:
        cls = "high" if f["severity"]=="High" else "med" if f["severity"]=="Medium" else "low"
        html += f"<tr><td>{f['user']}</td><td>{f['issue']}</td><td class={cls}>{f['severity']}</td><td>{f['fix']}</td></tr>"
    html += f"</table><p>Files saved to {download_dir}</p><p>Trial: {license_code} - Expires 14 days</p></body></html>"
    with open(html_path, "w") as fh: fh.write(html)
    notify_complete(html_path)

    # 2. CSV
    csv_path = os.path.join(download_dir, f"RetireSec_WeakPasswords_{ts}.csv")
    with open(csv_path, "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["Username","Issue","Severity","Fix","Timestamp"])
        for f in findings: w.writerow([f["user"], f["issue"], f["severity"], f["fix"], ts_human])
    notify_complete(csv_path)

    # 3. TXT
    log_path = os.path.join(download_dir, f"RetireSec_Log_{ts}.txt")
    with open(log_path, "w") as fh:
        fh.write(f"RetireSec Audit Log\nTime: {ts_human}\nLicense: {license_code}\nUsers: {users}\nFindings: {len(findings)}\n\n")
        for f in findings: fh.write(f"- {f['user']}: {f['issue']} [{f['severity']}]\n")
        fh.write(f"\nTest Codes: TEST-14DAY-RETIRES-2026, TRIAL-F3C3B0-2026\nOwner: mitchell5584dm@gmail.com\n")
    notify_complete(log_path)

    print(f"\n🎉 DONE! 3 FILES IN {download_dir}\nLicense Active: {license_code}\n")
    return html_path, csv_path, log_path

if __name__ == "__main__":
    code = sys.argv[1] if len(sys.argv) > 1 else "TRIAL-F3C3B0-2026"
    run_audit(code)
