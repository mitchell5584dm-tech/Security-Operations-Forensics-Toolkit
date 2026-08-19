# All Programs - Same Stripe - Linking Map

**Primary Stripe Checkout (Live):**
https://buy.stripe.com/5kQ14m2DQackeP687L5sA00
14-day trial → $99/yr - CredentialAuditor Pro
Same Stripe Account ID used for all below

**GitHub Repo:**
https://github.com/mitchell5584dm-tech/Security-Operations-Forensics-Toolkit
Live site: https://mitchell5584dm-tech.github.io/Security-Operations-Forensics-Toolkit/

**Releases (Fixed ZIPs):**
- Free 0.45 MB / 469.1 kB: https://github.com/mitchell5584dm-tech/Security-Operations-Forensics-Toolkit/releases/download/v1.0/RetireSec-Workbench-Free-v1.0.zip
- Pro 0.02 MB / 16.0 kB: https://github.com/mitchell5584dm-tech/Security-Operations-Forensics-Toolkit/releases/download/v1.0/RetireSec-Workbench-Pro-v1.0.zip
- Full 0.93 MB / 978.5 kB: https://github.com/mitchell5584dm-tech/Security-Operations-Forensics-Toolkit/releases/download/v1.0/RetireSec-Workbench-Full-Source-v1.0.zip

**Web Pages (Same Webpage Family - All Interlinked):**
- index.html - Main store - ALL programs one Stripe - links to store.html, pro.html, free.html, arcana.html, success.html
- store.html - Full store - 6 products - all same Stripe account
- pro.html - Dedicated Pro page - same Stripe
- free.html - Dedicated Free page - upgrade to same Stripe
- success.html - Payment success - auto-downloads all 3 ZIPs - Stripe redirect target
- arcana.html - ARCANA offshoot - Starter/Pro/Elite/Enterprise - same Stripe account, different price tiers (replace href with your other Payment Links from dashboard)

**Stripe Dashboard Setting (After Payment):**
Payment Links → CredentialAuditor Pro → After payment → Redirect to URL:
https://mitchell5584dm-tech.github.io/Security-Operations-Forensics-Toolkit/success.html
OR direct ZIP: https://github.com/mitchell5584dm-tech/Security-Operations-Forensics-Toolkit/releases/download/v1.0/RetireSec-Workbench-Pro-v1.0.zip

**Python Files Linked:**
- credential_auditor.py - free - no Stripe needed
- credential_auditor_with_notifications.py - pro - checks Stripe license via https://buy.stripe.com/5kQ14m2DQackeP687L5sA00
- app.py - webapp launcher - pro - same Stripe
- webapp/ folder - dashboard - pro - same Stripe

All programs same browser flow: GitHub Pages → Stripe Checkout (same account) → success.html → ZIP download
