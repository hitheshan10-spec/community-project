# CYBERSHIELD
### Your Digital Safety Companion
**Tagline:** *Learn. Identify. Protect.* | *ಕಲಿಯಿರಿ. ಗುರುತಿಸಿ. ರಕ್ಷಿಸಿಕೊಳ್ಳಿ.*

CyberShield is a production-grade, privacy-first cybersecurity education and scam detection web application built with Python, Streamlit, and SQLite. It is engineered specifically for Indian digital citizens—including school and college students, senior citizens, and everyday internet users.

---

## 🌟 Key Modules & Features

1. **Home Dashboard (`app.py`)**
   - High-contrast cybersecurity dark theme with neon cyan (`#00f0ff`) and emerald (`#00ff9d`) accents.
   - Real-time statistics across all 9 defense pillars, 12 scam vectors, and 30+ quiz questions.
   - Prominent National Cyber Crime Helpline (**1930**) alert integration.
   - Bilingual language selector (English and Kannada) and active user profile switcher.

2. **Scam Awareness Centre (`pages/1_Scam_Awareness.py`)**
   - 12 comprehensive cyber attack lessons:
     - Phishing & Clone Website Scams
     - OTP & Verification Code Fraud
     - UPI Collect Request & PIN Scams
     - Fake Work-From-Home & YouTube Like Scams
     - Lottery & KBC Lucky Draw Frauds
     - Social Media Impersonation & Cloned Friend Scams
     - QR Code Payment Traps
     - Fake Customer Care Search Listings
     - Fake E-Commerce & Deep Discount Stores
     - Investment & Crypto Ponzi Schemes
     - Identity Theft & SIM Swap Attacks
     - Remote Screen-Sharing Applications (AnyDesk / TeamViewer)
   - Detailed attack flows, warning signs, fictional case studies, and actionable defense checklists.
   - Interactive lesson completion tracker saved directly to SQLite.

3. **Digital Safety Guide (`pages/2_Digital_Safety.py`)**
   - 9 vital operational security guides: Passphrase hygiene, Two-Factor Authentication (TOTP vs SMS), UPI safety, NetBanking hygiene, Social media privacy, Public Wi-Fi safety, Smartphone permissions, Safe browsing, and Aadhaar biometric locking.
   - Interactive "Digital Hygiene Self-Assessment" calculator with instant score calculation.

4. **Online Scam Checker (`pages/3_Scam_Checker.py`)**
   - Rule-based text analysis engine that evaluates suspicious SMS, WhatsApp forwards, and emails completely offline.
   - Analyzes urgency, coercion triggers, credential harvesting, suspicious URLs, APK links, and UPI collect traps.
   - Generates Threat Score (0-100), Risk Level (High, Moderate, Low, Safe), red flag breakdown, and step-by-step counter-measures.
   - 6 one-click pre-loaded real-world scam templates (including Kannada scenarios).
   - Local privacy guarantee: zero external APIs, never stores credentials.

5. **Interactive Quiz Centre (`pages/4_Quiz_Centre.py`)**
   - 30+ multiple choice questions categorized across Easy, Medium, and Hard difficulty levels.
   - Instant feedback with green/red banners and detailed technical explanations.
   - Real-time running score and passing criteria calculation (60% threshold).
   - Milestone badges automatically awarded upon passing.

6. **Student Learning Zone (`pages/5_Student_Zone.py`)**
   - Gaming account protection (BGMI, Steam, Roblox, Free Fire, fake skin giveaways).
   - Cyberbullying and online harassment response playbook.
   - AI Deepfakes and Sextortion warning ("Never send money" rule).
   - Fake college internship and typing job scam defense.
   - Interactive "Spot the Fake" scenario challenges.

7. **Senior Citizen Mode (`pages/6_Senior_Citizen.py`)**
   - High-contrast, large-font typography and simplified navigation.
   - The 4 Golden Rules for Older Adults (PIN is never for receiving money; never install apps on calls).
   - Targeted scenarios: Pension Digital Life Certificate (Jeevan Pramaan) fraud, electricity disconnection SMS, ATM strangers.
   - Printable wallet and refrigerator emergency reference card.

8. **Emergency Help Centre (`pages/7_Emergency_Help.py`)**
   - Direct helpline: **1930** (National Cybercrime Reporting Portal).
   - Official portal link: `https://cybercrime.gov.in`.
   - "The Golden Hour" protocol: Step-by-step action plan for the first 60 minutes after being scammed.
   - Major Indian Banks 24x7 emergency fraud desks (SBI, HDFC, ICICI, Canara, Axis, PNB, BOB, Kotak).
   - Copyable Formal Bank & Police Grievance Letter template under RBI zero-liability rules.

9. **User Progress & Achievement Dashboard (`pages/8_Progress_Dashboard.py`)**
   - Multi-user profile management.
   - Rank progression system: Cyber Recruit 🔰 ➔ Cyber Sentinel ⚡ ➔ Cyber Guardian 🛡️ ➔ Cyber Master 👑.
   - 7 unlockable glowing achievement badges.
   - Quiz history and scam scan logs with Pandas data tables.
   - Official Printable Certificate of Cyber Defense Awareness.

10. **English & Kannada Bilingual Support**
    - Seamless toggle between English (`en`) and Kannada (`kn`) across all screens, headers, buttons, quizzes, and alert boxes.

---

## 🏗️ Architecture & File Structure

```
CyberShield/
  ├── app.py                      # Main entrypoint and Home Dashboard
  ├── requirements.txt            # Python dependencies
  ├── README.md                   # Documentation and manual
  ├── pages/
  │   ├── 1_Scam_Awareness.py     # 12 Scam awareness vector lessons
  │   ├── 2_Digital_Safety.py     # 9 Core operational security guides
  │   ├── 3_Scam_Checker.py       # Rule-based scam text analysis engine
  │   ├── 4_Quiz_Centre.py        # 30+ question multi-tier interactive quiz
  │   ├── 5_Student_Zone.py       # Gaming, cyberbullying & deepfake hub
  │   ├── 6_Senior_Citizen.py     # Large-print senior citizen safe mode
  │   ├── 7_Emergency_Help.py     # 1930 helpline & bank fraud directories
  │   └── 8_Progress_Dashboard.py # SQLite progress & completion certificates
  ├── database/
  │   ├── database.py             # SQLite schema, queries, and achievements
  │   └── cybershield.db          # Auto-created local database
  ├── data/
  │   ├── scams.json              # 12 scam lessons (EN & KN)
  │   ├── safety_guides.json      # 9 digital safety guides (EN & KN)
  │   ├── quiz.json               # 30+ quiz questions with explanations (EN & KN)
  │   └── translations.json       # Bilingual translations dictionary
  ├── utils/
  │   ├── scam_detection.py       # Pattern and heuristic NLP scam detector
  │   ├── translation.py          # Language management helper
  │   └── progress.py             # Session state, custom CSS & UI components
  └── assets/
      └── logo.png                # Generated CyberShield glowing emblem
```

---

## 🚀 How to Run Locally

### 1. Prerequisites
- Python 3.10, 3.11, or higher.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Application
```bash
streamlit run app.py
```
Or from the project root:
```bash
streamlit run CyberShield/app.py
```

The application will launch automatically in your default browser at `http://localhost:8501`.

---

## 🛡️ Privacy & Local Execution Notice
- CyberShield is completely self-contained and local.
- No third-party or paid APIs are invoked.
- No user credentials, passwords, OTPs, or PII are collected or stored.
