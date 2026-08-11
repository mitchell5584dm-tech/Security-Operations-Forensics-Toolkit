import os
import csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def notify_complete(filepath):
    abs_path = os.path.abspath(filepath)
    folder = os.path.dirname(abs_path)
    print("\n" + "="*70)
    print(f"✅ FILE COMPLETE: {os.path.basename(filepath)}")
    print(f"📁 LOCATION: {abs_path}")
    print(f"📂 FOLDER: {folder}")
    print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        messagebox.showinfo(
            "RetireSec - File Complete",
            f"✅ File Saved!\n\nFile: {os.path.basename(filepath)}\n\nFull Path:\n{abs_path}\n\nFolder:\n{folder}"
        )
        root.destroy()
    except:
        pass
    return abs_path

def run_credential_audit():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Example 1: HTML Report
    html_path = os.path.expanduser(f"~/Downloads/RetireSec_Report_{timestamp}.html")
    with open(html_path, "w") as f:
        f.write(f"<html><body><h1>RetireSec Report {timestamp}</h1><p>Scan complete - 100% offline</p></body></html>")
    notify_complete(html_path)
    
    # Example 2: CSV Results
    csv_path = os.path.expanduser(f"~/Downloads/RetireSec_WeakPasswords_{timestamp}.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Username", "Issue", "Severity"])
        writer.writerow(["admin", "Weak Password", "High"])
        writer.writerow(["user1", "No MFA", "Medium"])
    notify_complete(csv_path)
    
    # Example 3: TXT Log
    log_path = os.path.expanduser(f"~/Downloads/RetireSec_Log_{timestamp}.txt")
    with open(log_path, "w") as f:
        f.write(f"RetireSec Audit Log\nTime: {timestamp}\nFiles in ~/Downloads/\nTest codes: TEST-14DAY-RETIRES-2026")
    notify_complete(log_path)
    
    print("\n🎉 ALL 3 FILES SAVED TO ~/Downloads/ - Check popups!")

if __name__ == "__main__":
    run_credential_audit()
