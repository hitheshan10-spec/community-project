"""
CyberShield Emergency Help Centre
National incident response protocols, 1930 helpline guidelines, bank fraud desks, and evidence preservation.
"""

import os
import sys
import streamlit as st

st.set_page_config(
    page_title="Emergency Help - CyberShield",
    page_icon="🚨",
    layout="wide",
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from utils.progress import (
    render_page_header,
    render_footer,
)
from utils.translation import t, get_current_language


BANK_HELPLINES = [
    {"name": "State Bank of India (SBI)", "toll_free": "1800 1234 / 1800 2100", "fraud_sms": "SMS 'BLOCK' to 567676", "site": "onlinesbi.sbi"},
    {"name": "HDFC Bank", "toll_free": "1800 202 6161 / 1800 1600", "fraud_sms": "Use MobileBanking App Card Block", "site": "hdfcbank.com"},
    {"name": "ICICI Bank", "toll_free": "1800 1080", "fraud_sms": "SMS 'BLOCK <card>' to 9215676766", "site": "icicibank.com"},
    {"name": "Canara Bank", "toll_free": "1800 425 0018", "fraud_sms": "SMS 'CAN <card>' to 9266623333", "site": "canarabank.com"},
    {"name": "Axis Bank", "toll_free": "1800 419 5959 / 1800 419 5577", "fraud_sms": "SMS 'BLOCK <card>' to 5676782", "site": "axisbank.com"},
    {"name": "Punjab National Bank (PNB)", "toll_free": "1800 180 2222 / 1800 103 2222", "fraud_sms": "SMS 'HOTLIST' to 5607040", "site": "pnbindia.in"},
    {"name": "Bank of Baroda", "toll_free": "1800 5700 / 1800 5000", "fraud_sms": "Use BOB World App Instant Freeze", "site": "bankofbaroda.in"},
    {"name": "Kotak Mahindra Bank", "toll_free": "1860 266 2666", "fraud_sms": "SMS 'BLOCK' to 9971056767", "site": "kotak.com"},
]


def main():
    lang = get_current_language()
    title = t("emergency_title")
    subtitle = t("emergency_subtitle")
    render_page_header(title, subtitle, badge_text="INCIDENT RESPONSE")

    # High-Impact National Emergency Banner
    st.markdown(
        f"""
        <div class="cyber-card cyber-card-danger" style="padding: 28px; text-align: center; background: rgba(255, 51, 102, 0.12); border-width: 2px;">
            <div style="font-size: 14px; text-transform: uppercase; letter-spacing: 0.1em; color: #ff85a2; font-weight: 700;">
                {'NATIONAL CYBERCRIME REPORTING HELPLINE (GOVERNMENT OF INDIA)' if lang == 'en' else 'ರಾಷ್ಟ್ರೀಯ ಸೈಬರ್ ಕ್ರೈಂ ರಿಪೋರ್ಟಿಂಗ್ ಸಹಾಯವಾಣಿ (ಭಾರತ ಸರ್ಕಾರ)'}
            </div>
            <div style="font-size: 52px; font-weight: 900; color: #ff3366; font-family: 'JetBrains Mono'; margin: 8px 0; text-shadow: 0 0 20px rgba(255, 51, 102, 0.5);">
                📞 1930
            </div>
            <div style="font-size: 18px; color: #f8fafc; font-weight: 600;">
                {'Toll-Free • 24 Hours x 7 Days • Available in Kannada, English, Hindi, and All Regional Languages' if lang == 'en' else 'ಉಚಿತ ಸಹಾಯವಾಣಿ • 24 ಗಂಟೆ ಲಭ್ಯ • ಕನ್ನಡ, ಇಂಗ್ಲಿಷ್ ಮತ್ತು ಎಲ್ಲಾ ಪ್ರಾದೇಶಿಕ ಭಾಷೆಗಳಲ್ಲಿ'}
            </div>
            <div style="margin-top: 15px;">
                <a href="https://cybercrime.gov.in" target="_blank" style="text-decoration: none;">
                    <span class="badge-pill badge-cyan" style="padding: 8px 18px; font-size: 14px; cursor: pointer;">
                        🌐 Official Portal: cybercrime.gov.in
                    </span>
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    step1_info = (
        "Provide your name, mobile number, bank account number, and transaction UTR / Reference ID. The operator alerts the Citizen Financial Cyber Fraud Reporting System to freeze funds at the receiving bank."
        if lang == "en"
        else "ನಿಮ್ಮ ಹೆಸರು, ಮೊಬೈಲ್ ಸಂಖ್ಯೆ, ಬ್ಯಾಂಕ್ ಖಾತೆ ಮತ್ತು UTR ವಹಿವಾಟು ಐಡಿ ತಿಳಿಸಿ. ಆಪರೇಟರ್ ಹಣ ಸ್ವೀಕರಿಸಿದ ವಂಚಕರ ಬ್ಯಾಂಕ್ ಖಾತೆಯನ್ನು ತಕ್ಷಣ ಫ್ರೀಜ್ ಮಾಡುತ್ತಾರೆ."
    )
    step2_info = (
        "Call your bank 24x7 toll-free emergency line. Ask them to block your debit/credit card, disable UPI services, and freeze NetBanking access immediately."
        if lang == "en"
        else "ನಿಮ್ಮ ಬ್ಯಾಂಕಿನ ತುರ್ತು ಸಹಾಯವಾಣಿಗೆ ಕರೆ ಮಾಡಿ ನಿಮ್ಮ ಡೆಬಿಟ್ ಕಾರ್ಡ್ ಬ್ಲಾಕ್ ಮಾಡಿ ಮತ್ತು ಯುಪಿಐ ಸೇವೆಯನ್ನು ತಾತ್ಕಾಲಿಕವಾಗಿ ಸ್ಥಗಿತಗೊಳಿಸಿ."
    )
    step3_info = (
        "Do NOT delete text messages, WhatsApp chats, or call history. Take clear screenshots showing caller numbers, timestamps, transaction alerts, and bank SMS."
        if lang == "en"
        else "ಯಾವುದೇ ಸಂದೇಶ ಅಥವಾ ಚಾಟ್ ಡಿಲೀಟ್ ಮಾಡಬೇಡಿ. ಫೋನ್ ಸಂಖ್ಯೆ, ವಹಿವಾಟಿನ UTR ನಂಬರ್ ಮತ್ತು ಬ್ಯಾಂಕ್ ಮೆಸೇಜ್‌ಗಳ ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ತೆಗೆದಿಟ್ಟುಕೊಳ್ಳಿ."
    )
    step4_info = (
        "Visit cybercrime.gov.in, select 'Report Financial Fraud', fill in transaction details, and upload evidence to receive an official formal Complaint Acknowledgement Number."
        if lang == "en"
        else "cybercrime.gov.in ಗೆ ಭೇಟಿ ನೀಡಿ 'Report Financial Fraud' ಆಯ್ಕೆ ಮಾಡಿ ಎಲ್ಲಾ ಸಾಕ್ಷ್ಯಗಳನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಸ್ವೀಕೃತಿ ಸಂಖ್ಯೆ (Acknowledgement Number) ಪಡೆದುಕೊಳ್ಳಿ."
    )

    # The Golden Hour Protocol (First 60 Minutes)
    st.markdown(
        f"""
        <div class="cyber-card cyber-card-warning" style="padding: 24px;">
            <div style="display: flex; gap: 14px; align-items: center; margin-bottom: 12px;">
                <span style="font-size: 32px;">⏱️</span>
                <div>
                    <h3 style="margin: 0; color: #ffb703;">{t('golden_hour_title')}</h3>
                    <p style="margin: 4px 0 0 0; color: #cbd5e1; font-size: 14px;">{t('golden_hour_desc')}</p>
                </div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr; gap: 12px; margin-top: 18px;">
                <div style="background: rgba(11, 19, 41, 0.85); border-left: 4px solid #ff3366; border-radius: 8px; padding: 14px;">
                    <div style="font-weight: 700; color: #ff3366; font-size: 16px;">{t('step1_dial')}</div>
                    <div style="font-size: 14px; color: #e2e8f0; margin-top: 4px;">{step1_info}</div>
                </div>
                <div style="background: rgba(11, 19, 41, 0.85); border-left: 4px solid #ffb703; border-radius: 8px; padding: 14px;">
                    <div style="font-weight: 700; color: #ffb703; font-size: 16px;">{t('step2_bank')}</div>
                    <div style="font-size: 14px; color: #e2e8f0; margin-top: 4px;">{step2_info}</div>
                </div>
                <div style="background: rgba(11, 19, 41, 0.85); border-left: 4px solid #00f0ff; border-radius: 8px; padding: 14px;">
                    <div style="font-weight: 700; color: #00f0ff; font-size: 16px;">{t('step3_evidence')}</div>
                    <div style="font-size: 14px; color: #e2e8f0; margin-top: 4px;">{step3_info}</div>
                </div>
                <div style="background: rgba(11, 19, 41, 0.85); border-left: 4px solid #00ff9d; border-radius: 8px; padding: 14px;">
                    <div style="font-weight: 700; color: #00ff9d; font-size: 16px;">{t('step4_portal')}</div>
                    <div style="font-size: 14px; color: #e2e8f0; margin-top: 4px;">{step4_info}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # Major Indian Banks 24x7 Emergency Contact Directory
    st.markdown(f"### 🏦 {t('bank_helplines_title')}")
    st.markdown(
        f"<p style='color: #94a3b8; font-size: 14px;'>{'Official toll-free fraud reporting and card hotlisting contacts for leading financial institutions across India.' if lang == 'en' else 'ಭಾರತದ ಪ್ರಮುಖ ಬ್ಯಾಂಕುಗಳ ತುರ್ತು ಸಹಾಯವಾಣಿ ಮತ್ತು ಕಾರ್ಡ್ ಬ್ಲಾಕ್ ಸಂಖ್ಯೆಗಳು.'}</p>",
        unsafe_allow_html=True,
    )

    b_col1, b_col2 = st.columns(2)
    for i, b in enumerate(BANK_HELPLINES):
        target_col = b_col1 if i % 2 == 0 else b_col2
        with target_col:
            st.markdown(
                f"""
                <div class="cyber-card" style="padding: 16px; margin-bottom: 12px;">
                    <div style="font-size: 16px; font-weight: 700; color: #00f0ff; margin-bottom: 6px;">{b['name']}</div>
                    <div style="font-size: 14px; color: #ffffff;">📞 <b>Toll-Free Helpline:</b> <span style="font-family: 'JetBrains Mono'; color: #00ff9d;">{b['toll_free']}</span></div>
                    <div style="font-size: 13px; color: #cbd5e1; margin-top: 4px;">📲 <b>Card Block SMS:</b> {b['fraud_sms']}</div>
                    <div style="font-size: 12px; color: #64748b; margin-top: 4px;">🌐 Official: {b['site']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Formal Grievance Complaint Letter Generator
    st.markdown(
        f"""
        <div class="cyber-card" style="padding: 22px;">
            <div style="display: flex; gap: 12px; align-items: center; margin-bottom: 10px;">
                <span style="font-size: 28px;">📄</span>
                <div>
                    <h3 style="margin: 0; color: #00f0ff;">
                        {'Formal Bank & Cyber Cell Complaint Template' if lang == 'en' else 'ಬ್ಯಾಂಕ್ ಮತ್ತು ಸೈಬರ್ ಪೊಲೀಸ್ ಠಾಣೆಗೆ ದೂರು ಅರ್ಜಿ ಮಾದರಿ'}
                    </h3>
                    <p style="margin: 2px 0 0 0; color: #94a3b8; font-size: 13px;">
                        {'Copy this ready template, fill in your details, and submit it to your bank branch and local cyber police station.' if lang == 'en' else 'ಈ ದೂರು ಪತ್ರವನ್ನು ನಕಲಿಸಿ, ನಿಮ್ಮ ವಿವರಗಳನ್ನು ಭರ್ತಿ ಮಾಡಿ ಬ್ಯಾಂಕ್ ಮತ್ತು ಪೊಲೀಸ್ ಠಾಣೆಗೆ ಸಲ್ಲಿಸಿ.'}
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sample_letter = """To,
The Branch Manager,
[Name of Your Bank], [Branch Name]
AND
The Station House Officer (SHO),
Cyber Crime Police Station, [City/District]

Subject: Urgent Complaint Regarding Unauthorized Cyber Financial Fraud of ₹[Amount]

Respected Sir/Madam,

I, [Your Full Name], holding Savings Account No: [Your Account Number] at your branch, wish to report an unauthorized financial cyber fraud that occurred on [Date] at approximately [Time].

Details of the Fraudulent Transaction:
1. Amount Debited: ₹[Enter Amount]
2. Transaction Reference / UTR Number: [Enter UTR from Bank SMS]
3. Fraudster Beneficiary Account / UPI ID / Phone: [Enter Details]
4. Mode of Fraud: [e.g., Phishing Link / UPI Collect / Remote Access / Electricity SMS]
5. National Cyber Helpline 1930 Complaint ID: [Enter Acknowledgement Number]

I have NOT shared my OTP, UPI PIN, or Netbanking passwords. In accordance with RBI Circular DBR.No.Leg.BC.78/09.07.005/2017-18 on Customer Protection and Zero Liability, I hereby report this unauthorized transaction within the mandatory 3-day window.

I request you to:
1. Immediately place a freeze on the beneficiary account to recall the funds.
2. Provide an official acknowledgement of this complaint.
3. Initiate insurance / chargeback procedures to reverse the debited amount.

Attached Documents:
- Bank Account Statement highlighting the unauthorized debit
- Screenshots of SMS transaction alert and fraud communication
- Copy of National Cybercrime Portal Acknowledgement

Thanking you,
Yours sincerely,
[Your Name]
Mobile Number: [Your Mobile Number]
Date: [Current Date]
"""

    st.text_area(
        "Copyable Complaint Letter:" if lang == "en" else "ನಕಲಿಸಬಹುದಾದ ದೂರು ಪತ್ರ:",
        value=sample_letter,
        height=260,
        key="complaint_template_area",
    )

    render_footer()


if __name__ == "__main__":
    main()
