"""
CyberShield Rule-Based Scam Detection Engine
Performs heuristic, keyword, and pattern analysis on suspicious messages (SMS, WhatsApp, emails).
Works completely offline without requiring paid APIs or internet access.
"""

import re
from typing import Dict, List, Any


SAMPLE_SCAMS = [
    {
        "title": "⚡ Electricity Disconnection Threat",
        "category": "Utility Scam",
        "text": "Dear customer, your electricity power will be disconnected tonight at 9:30 PM from the electricity office because your previous month bill was not updated. Please immediately contact our electricity officer at 9876543210. Thank you.",
        "lang": "en",
    },
    {
        "title": "🎉 KBC 25 Lakh Lucky Draw WhatsApp",
        "category": "Lottery Fraud",
        "text": "Dear user, congratulations! Your mobile number has won ₹25,00,000 in Kaun Banega Crorepati (KBC) All India SIM Card Lucky Draw. To claim your prize money, immediately contact bank manager Mr. Verma on WhatsApp number +923001234567 and deposit ₹12,500 government registration tax.",
        "lang": "en",
    },
    {
        "title": "💼 Part-Time YouTube Like Job Scam",
        "category": "Job / Task Scam",
        "text": "Hello, I am Priya from Global Media Recruitment. We offer part-time work from home. Just like and subscribe to 3 YouTube videos and earn ₹3,500 daily. No investment needed initially. Contact our Telegram supervisor @TaskManagerVIP right now to get your first ₹200 bonus.",
        "lang": "en",
    },
    {
        "title": "🏦 Bank Account / KYC Suspension SMS",
        "category": "Phishing & Credential Theft",
        "text": "URGENT ALERT: Your SBI Bank savings account has been suspended due to incomplete KYC documentation. Please click http://sbi-kyc-verify-portal.top/login to update your PAN and Aadhaar number immediately or your account will be permanently closed within 24 hours.",
        "lang": "en",
    },
    {
        "title": "📱 OLX QR Code & UPI Collect Scam",
        "category": "UPI Trap",
        "text": "Sir, I am purchasing your sofa for ₹14,000. I have sent a PhonePe QR code payment request. Please scan this QR code and type your 6-digit UPI PIN to accept the cash directly into your bank account.",
        "lang": "en",
    },
    {
        "title": "⚡ ವಿದ್ಯುತ್ ಸಂಪರ್ಕ ಕಡಿತ (Kannada Utility Scam)",
        "category": "Utility Scam (Kannada)",
        "text": "ಗ್ರಾಹಕರೇ, ನಿಮ್ಮ ವಿದ್ಯುತ್ ಬಿಲ್ ಬಾಕಿ ಇರುವುದರಿಂದ ಇಂದು ರಾತ್ರಿ ನಿಮ್ಮ ವಿದ್ಯುತ್ ಸಂಪರ್ಕ ಕಡಿತಗೊಳ್ಳಲಿದೆ. ತಕ್ಷಣ ಸರಿಪಡಿಸಲು ವಿದ್ಯುತ್ ಅಧಿಕಾರಿಗೆ ಕರೆ ಮಾಡಿ ಅಥವಾ ಈ ಲಿಂಕ್ ಕ್ಲಿಕ್ ಮಾಡಿ ಹಣ ಪಾವತಿಸಿ.",
        "lang": "kn",
    },
]


# Detection rules and indicator weights
RULES = [
    # 1. Credential & Sensitive Data Requests (Severity: Critical)
    {
        "category": "Credential Harvesting",
        "weight": 35,
        "patterns": [
            r"\b(otp|one[\s-]?time[\s-]?password|verification code)\b",
            r"\b(upi[\s-]?pin|atm[\s-]?pin|mpin|security pin)\b",
            r"\b(cvv|card expiry|netbanking password|profile password)\b",
            r"\b(aadhaar|pan card|pan number)\b.*\b(update|verify|link|submit)\b",
            r"(ಒಟಿಪಿ|ಪಿನ್|ಪಾಸ್‌ವರ್ಡ್|ಸಿವಿವಿ|ಆಧಾರ್)",
        ],
        "red_flag": "Explicit request for sensitive credentials (OTP, PIN, Password, or Aadhaar/PAN linking).",
        "advice": "Banks and legitimate portals will NEVER request OTPs, UPI PINs, or CVVs via message.",
    },
    # 2. Urgency, Coercion & Intimidation (Severity: High)
    {
        "category": "Coercion & Urgency",
        "weight": 25,
        "patterns": [
            r"\b(immediately|urgent|urgently|within 24 hours|within 2 hours|tonight|today)\b",
            r"\b(disconnected|deactivated|suspended|blocked|terminated|closed permanently)\b",
            r"\b(police|court|legal notice|arrest warrant|cbi|rbi notice)\b",
            r"(ತಕ್ಷಣ|ಇಂದೇ|24 ಗಂಟೆ|ಬ್ಲಾಕ್|ರದ್ದಾಗಲಿದೆ|ಕಡಿತಗೊಳ್ಳಲಿದೆ)",
        ],
        "red_flag": "Manufactured urgency or fear-inducing threats of immediate disconnection, blockage, or legal action.",
        "advice": "Scammers create artificial panic so victims act emotionally before thinking rationally.",
    },
    # 3. Fake Prizes, Lotteries, Cashback & High Returns (Severity: High)
    {
        "category": "Prize & Financial Lures",
        "weight": 30,
        "patterns": [
            r"\b(won|winner|winning|congratulations|lottery|lucky draw|kbc|car prize)\b",
            r"\b(₹\s?\d+,\d+|\b\d+\s?lakh|\b\d+\s?crore)\b.*\b(won|claim|reward|prize)\b",
            r"\b(cashback|free gift|reward points|claim prize|double your money)\b",
            r"\b(earn\s?₹?\s?\d+.*daily|work from home.*₹?\d+)\b",
            r"(ಲಾಟರಿ|ಗೆದ್ದಿದ್ದೀರಿ|ಬಹುಮಾನ|ಲಕ್ಕಿ ಡ್ರಾ|ಕ್ಯಾಶ್‌ಬ್ಯಾಕ್|ದಿನಕ್ಕೆ ಗಳಿಸಿ)",
        ],
        "red_flag": "Unrealistic lottery win, lucky draw, or effortless high-earning promise.",
        "advice": "You cannot win a lottery you never entered. No company gives away free lakhs of rupees.",
    },
    # 4. Remote Screen Sharing Tools (Severity: Critical)
    {
        "category": "Remote Access Exploit",
        "weight": 40,
        "patterns": [
            r"\b(anydesk|teamviewer|quicksupport|rustdesk|screenshare|zoho assist)\b",
            r"\b(install|download)\b.*\b(app|apk|software)\b.*\b(support|verify|kyc)\b",
            r"(anydesk|teamviewer|quicksupport|ಆ್ಯಪ್ ಡೌನ್‌ಲೋಡ್)",
        ],
        "red_flag": "Instructions to install remote screen-sharing software (AnyDesk, TeamViewer, QuickSupport).",
        "advice": "Never install remote desktop apps on caller requests. They give attackers total control of your device.",
    },
    # 5. Suspicious Links, Domains, and Shorteners (Severity: High)
    {
        "category": "Suspicious Links",
        "weight": 25,
        "patterns": [
            r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",  # IP address URL
            r"https?://(bit\.ly|tinyurl\.com|t\.me|is\.gd|cutt\.ly|rb\.gy)/\S+",
            r"https?://\S+\.(xyz|top|vip|club|work|shop|in\.net|cc|app|site)/\S*",
            r"https?://\S*(kyc|update|login|bank|sbi|hdfc|pan|verify)\S*\.(?!gov\.in|bank|sbi|hdfcbank\.com)\S+",
            r"\b\.apk\b",
        ],
        "red_flag": "Suspicious URL: shortener, IP address, unverified domain (.xyz/.top), or raw APK download.",
        "advice": "Do not tap on untrusted links. Inspect URLs carefully for misspelling and suspicious domains.",
    },
    # 6. UPI Inverted Payment Traps (Severity: High)
    {
        "category": "UPI Payment Trap",
        "weight": 30,
        "patterns": [
            r"\b(scan\s?(this)?\s?qr|enter\s?(your)?\s?pin\s?to\s?receive|type\s?pin\s?to\s?credit)\b",
            r"\b(phonepe|google\s?pay|gpay|paytm)\b.*\b(qr\s?code|collect request|refund)\b",
            r"(ಕ್ಯೂಆರ್ ಕೋಡ್ ಸ್ಕ್ಯಾನ್|ಪಿನ್ ನಮೂದಿಸಿ ಹಣ ಪಡೆಯಿರಿ)",
        ],
        "red_flag": "Deceptive instruction to scan a QR code or enter a UPI PIN in order to 'receive' funds.",
        "advice": "Entering your PIN DEBITS money from your account. You NEVER type a PIN to receive money.",
    },
    # 7. Unofficial Contact Channels for Official Services (Severity: Moderate)
    {
        "category": "Unofficial Contact Point",
        "weight": 20,
        "patterns": [
            r"\b(call|contact|whatsapp)\b.*\b(\+?91[\s-]?[6-9]\d{9}|[6-9]\d{9})\b",
            r"\b(telegram|t\.me/|whatsapp group)\b",
            r"(ಕರೆ ಮಾಡಿ|ವಾಟ್ಸಾಪ್ ಮಾಡಿ|ಟೆಲಿಗ್ರಾಂ)",
        ],
        "red_flag": "Personal 10-digit mobile number or Telegram handle given for an official institutional service.",
        "advice": "Government agencies, banks, and major corporations use official 1800 toll-free lines, not personal mobile numbers.",
    },
]


def analyze_message(text: str) -> Dict[str, Any]:
    """
    Performs deterministic rule-based analysis on the given message text.
    Returns risk level, calculated risk score (0-100), detected triggers, explanation, and actionable advice.
    """
    clean_text = text.strip()
    if not clean_text:
        return {
            "risk_level": "SAFE",
            "risk_score": 0,
            "detected_triggers": [],
            "scam_category": "None",
            "explanation": "No text provided for analysis.",
            "recommendations": ["Paste a suspicious message into the text box above to analyze it."],
        }

    detected_triggers: List[Dict[str, str]] = []
    total_score = 0
    matched_categories = set()

    for rule in RULES:
        rule_matched = False
        for pattern in rule["patterns"]:
            if re.search(pattern, clean_text, re.IGNORECASE):
                rule_matched = True
                break

        if rule_matched:
            total_score += rule["weight"]
            matched_categories.add(rule["category"])
            detected_triggers.append(
                {
                    "category": rule["category"],
                    "red_flag": rule["red_flag"],
                    "advice": rule["advice"],
                }
            )

    # Heuristic adjustments:
    # Bonus score if multiple high-risk categories are present together (e.g. Urgency + Link or Credential + Urgency)
    if len(matched_categories) >= 3:
        total_score += 15
    elif len(matched_categories) >= 2:
        total_score += 10

    # Cap score between 0 and 100
    risk_score = min(max(total_score, 0), 100)

    # Determine risk level
    if risk_score >= 65:
        risk_level = "HIGH RISK"
        risk_color = "#ff3366"
        explanation = (
            "🚨 CRITICAL FRAUD ALERT: This message exhibits multiple classic markers of an active cyber scam. "
            "High likelihood of financial fraud, credential theft, or unauthorized device takeover."
        )
    elif risk_score >= 40:
        risk_level = "MODERATE RISK"
        risk_color = "#ffb703"
        explanation = (
            "⚠️ SUSPICIOUS CONTENT: This message contains red flags commonly found in deceptive communications. "
            "Exercise extreme caution and verify independently through official channels."
        )
    elif risk_score >= 20:
        risk_level = "LOW RISK"
        risk_color = "#38bdf8"
        explanation = (
            "ℹ️ CAUTION ADVISED: Some minor automated or marketing triggers were detected. "
            "While not immediately hazardous, never share passwords or click unverified links."
        )
    else:
        risk_level = "SAFE"
        risk_color = "#00ff9d"
        explanation = (
            "✅ NO IMMEDIATE THREAT IDENTIFIED: The analyzed text does not exhibit common automated scam triggers. "
            "However, always stay vigilant and never provide confidential financial credentials."
        )

    # Determine primary scam category label
    if "Remote Access Exploit" in matched_categories:
        scam_category = "Remote Screen Access Scam"
    elif "Credential Harvesting" in matched_categories and "Suspicious Links" in matched_categories:
        scam_category = "Phishing & Credential Theft"
    elif "UPI Payment Trap" in matched_categories:
        scam_category = "UPI Collect / QR Code Trap"
    elif "Prize & Financial Lures" in matched_categories and "Coercion & Urgency" in matched_categories:
        scam_category = "Lottery / Prize Advance Fee Fraud"
    elif "Prize & Financial Lures" in matched_categories:
        scam_category = "Work-from-Home / Investment Scam"
    elif "Coercion & Urgency" in matched_categories and "Unofficial Contact Point" in matched_categories:
        scam_category = "Utility / Bank Impersonation Scam"
    elif matched_categories:
        scam_category = list(matched_categories)[0]
    else:
        scam_category = "Unclassified / Normal"

    # Compile actionable recommendations
    recommendations = []
    if risk_score >= 40:
        recommendations.append("❌ DO NOT click any links, open attachments, or download APK files mentioned.")
        recommendations.append("🔒 NEVER share your OTP, UPI PIN, ATM PIN, or passwords with anyone under any pretext.")
        recommendations.append("📞 DO NOT call phone numbers provided in the message. Only use official numbers from bank passbooks or official apps.")
        recommendations.append("🚫 Block the sender immediately and report as spam in your messaging application.")
        recommendations.append("🛡️ If you already shared credentials or lost funds, immediately dial 1930 and contact your bank to freeze transactions.")
    else:
        recommendations.append("🔍 Always inspect sender information and verify unexpected communications.")
        recommendations.append("🛡️ Keep your smartphone operating system and security apps up to date.")

    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "risk_color": risk_color,
        "scam_category": scam_category,
        "detected_triggers": detected_triggers,
        "explanation": explanation,
        "recommendations": recommendations,
    }
