"""
CyberShield Senior Citizen Mode
Accessible, large-font, simplified digital safety guidance for older adults and digital newcomers.
"""

import os
import sys
import streamlit as st

st.set_page_config(
    page_title="Senior Citizen Mode - CyberShield",
    page_icon="👴",
    layout="wide",
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from utils.progress import (
    render_page_header,
    render_footer,
    get_active_user,
)
from utils.translation import t, get_current_language
from database.database import (
    mark_lesson_completed,
    is_lesson_completed,
)


SENIOR_SCENARIOS = [
    {
        "id": "senior_pension",
        "icon": "📜",
        "title_en": "Pension & Jeevan Pramaan Certificate Scams",
        "title_kn": "ಪಿಂಚಣಿ ಮತ್ತು ಜೀವನ್ ಪ್ರಮಾಣ ಪತ್ರ ವಂಚನೆ",
        "desc_en": "Fraudsters call retired seniors stating: 'Your pension will stop next month because your digital life certificate expired. Give us your Aadhaar OTP to update online.'",
        "desc_kn": "ನಿವೃತ್ತ ಹಿರಿಯರಿಗೆ ಕರೆ ಮಾಡಿ 'ನಿಮ್ಮ ಡಿಜಿಟಲ್ ಲೈಫ್ ಸರ್ಟಿಫಿಕೇಟ್ ಮುಗಿದಿದೆ, ಮುಂದಿನ ತಿಂಗಳಿಂದ ಪಿಂಚಣಿ ಬರುವುದಿಲ್ಲ. ಆನ್‌ಲೈನ್‌ನಲ್ಲಿ ಅಪ್‌ಡೇಟ್ ಮಾಡಲು ಆಧಾರ್ OTP ತಿಳಿಸಿ' ಎಂದು ಮೋಸ ಮಾಡುವುದು.",
        "rule_en": "NEVER share Aadhaar OTP over phone calls. Digital Life Certificates can ONLY be submitted in person at bank branches, post offices, or Citizen Service Centers (CSC).",
        "rule_kn": "ಫೋನ್‌ನಲ್ಲಿ ಯಾವುದೇ ಕಾರಣಕ್ಕೂ ಆಧಾರ್ OTP ಹೇಳಬೇಡಿ. ಜೀವನ್ ಪ್ರಮಾಣ ಪತ್ರವನ್ನು ಬ್ಯಾಂಕ್ ಶಾಖೆ ಅಥವಾ ಅಂಚೆ ಕಚೇರಿಯಲ್ಲಿ ಮಾತ್ರ ಸಲ್ಲಿಸಬೇಕು."
    },
    {
        "id": "senior_electricity",
        "icon": "⚡",
        "title_en": "Electricity Power Cutoff Threat SMS",
        "title_kn": "ವಿದ್ಯುತ್ ಸಂಪರ್ಕ ಕಡಿತದ ಸುಳ್ಳು ಸಂದೇಶಗಳು",
        "desc_en": "A message arrives: 'Dear Customer, your electricity will be disconnected at 9:30 PM tonight because bill was not updated. Call official 9876543210.'",
        "desc_kn": "'ಗ್ರಾಹಕರೇ, ನಿಮ್ಮ ಹಿಂದಿನ ತಿಂಗಳ ಬಿಲ್ ಪಾವತಿಯಾಗಿಲ್ಲ, ಇಂದು ರಾತ್ರಿ 9:30 ಕ್ಕೆ ವಿದ್ಯುತ್ ಕಡಿತಗೊಳ್ಳಲಿದೆ. ತಕ್ಷಣ 9876543210 ಗೆ ಕರೆ ಮಾಡಿ' ಎಂದು ಬೆದರಿಸುವುದು.",
        "rule_en": "BESCOM, KPTCL, and electricity boards NEVER disconnect power at night or use personal 10-digit mobile numbers. This is a 100% fake scam. Delete the message.",
        "rule_kn": "ಬೆಸ್ಕಾಂ ಅಥವಾ ಯಾವುದೇ ವಿದ್ಯುತ್ ಮಂಡಳಿ ರಾತ್ರಿ ವೇಳೆ ವಿದ್ಯುತ್ ಕಡಿತ ಮಾಡುವುದಿಲ್ಲ ಮತ್ತು ವೈಯಕ್ತಿಕ ಮೊಬೈಲ್‌ನಿಂದ ಮೆಸೇಜ್ ಕಳುಹಿಸುವುದಿಲ್ಲ. ಇದು ಸಂಪೂರ್ಣ ಸುಳ್ಳು."
    },
    {
        "id": "senior_atm_help",
        "icon": "🏧",
        "title_en": "The 'Friendly Stranger' at the ATM",
        "title_kn": "ಎಟಿಎಂನಲ್ಲಿ 'ಸಹಾಯ ಮಾಡುವ' ಅಪರಿಚಿತ ವ್ಯಕ್ತಿ",
        "desc_en": "A stranger standing behind you at an ATM offers to help you insert your card or enter your PIN, secretly memorizing your PIN and swapping your card with an expired dummy card.",
        "desc_kn": "ಎಟಿಎಂ ಕೇಂದ್ರದಲ್ಲಿ ಹಣ ತೆಗೆಯಲು ಸಹಾಯ ಮಾಡುವ ನೆಪದಲ್ಲಿ ನಿಮ್ಮ ಕಾರ್ಡ್ ಬದಲಾಯಿಸಿ, ನೀವು ಪಿನ್ ನಮೂದಿಸುವಾಗ ಕದ್ದು ನೋಡಿ ನಂತರ ಹಣ ಲಪಟಾಯಿಸುವುದು.",
        "rule_en": "Never accept ATM assistance from strangers. Always cover the keypad with your free hand while typing your 4-digit PIN.",
        "rule_kn": "ಎಟಿಎಂನಲ್ಲಿ ಅಪರಿಚಿತರ ಸಹಾಯ ಪಡೆಯಬೇಡಿ. ಪಿನ್ ನಮೂದಿಸುವಾಗ ಕೀಪ್ಯಾಡ್ ಮೇಲೆ ಇನ್ನೊಂದು ಕೈಯನ್ನು ಅಡ್ಡಲಾಗಿ ಇಟ್ಟುಕೊಳ್ಳಿ."
    },
    {
        "id": "senior_kyc_freeze",
        "icon": "🏦",
        "title_en": "Bank Account Freeze / KYC Expired Call",
        "title_kn": "ಬ್ಯಾಂಕ್ ಖಾತೆ ಬ್ಲಾಕ್ / KYC ನವೀಕರಣ ಕರೆ",
        "desc_en": "A caller speaks very politely in your native language claiming to be from your bank branch: 'Sir, your account is temporarily on hold. Download QuickSupport app to restore it.'",
        "desc_kn": "'ಸರ್, ನಾವು ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಶಾಖೆಯಿಂದ ಮಾತನಾಡುತ್ತಿದ್ದೇವೆ. ನಿಮ್ಮ ಖಾತೆ ಬ್ಲಾಕ್ ಆಗಿದೆ, ಸರಿಪಡಿಸಲು QuickSupport ಅಥವಾ AnyDesk ಆ್ಯಪ್ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ' ಎಂದು ಹೇಳುವುದು.",
        "rule_en": "HANG UP IMMEDIATELY. Real bank managers never ask you to install apps. Visit your local branch with your passbook if you have any questions.",
        "rule_kn": "ತಕ್ಷಣ ಫೋನ್ ಕರೆ ಕಟ್ ಮಾಡಿ. ಯಾವುದೇ ಬ್ಯಾಂಕ್ ಆ್ಯಪ್ ಡೌನ್‌ಲೋಡ್ ಮಾಡಲು ಹೇಳುವುದಿಲ್ಲ. ಸಂಶಯವಿದ್ದರೆ ಬ್ಯಾಂಕ್ ಶಾಖೆಗೆ ನೇರವಾಗಿ ಭೇಟಿ ನೀಡಿ."
    }
]


def main():
    lang = get_current_language()
    title = t("senior_title")
    subtitle = t("senior_subtitle")
    render_page_header(title, subtitle, badge_text="SENIOR SAFETY SHIELD")

    user = get_active_user()

    # Large Prominent Emergency Alert Card
    st.markdown(
        f"""
        <div class="cyber-card cyber-card-danger" style="padding: 24px; text-align: center; background: rgba(255, 51, 102, 0.1);">
            <div style="font-size: 28px; font-weight: 800; color: #ff3366; margin-bottom: 8px;">
                🚨 {'IN ANY SUSPICION OR MONEY LOSS: DIAL 1930' if lang == 'en' else 'ಯಾವುದೇ ಸಂಶಯವಿದ್ದಲ್ಲಿ ಅಥವಾ ಹಣ ಕಳೆದುಕೊಂಡರೆ: 1930 ಗೆ ಕರೆ ಮಾಡಿ'}
            </div>
            <div style="font-size: 18px; color: #f8fafc;">
                {'National Toll-Free Cyber Helpline • Free & Available 24x7 in Kannada & English' if lang == 'en' else 'ರಾಷ್ಟ್ರೀಯ ಉಚಿತ ಸೈಬರ್ ಸಹಾಯವಾಣಿ • ಕನ್ನಡ ಮತ್ತು ಇಂಗ್ಲಿಷ್‌ನಲ್ಲಿ 24x7 ಲಭ್ಯ'}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # 4 Golden Rules for Seniors with Extra-Large Typography
    st.markdown(
        f"""
        <div class="cyber-card cyber-card-accent" style="padding: 24px;">
            <h2 style="color: #00f0ff; margin-top: 0; font-size: 26px;">
                ⭐ {t('golden_rules_seniors')}
            </h2>
            <div style="display: grid; grid-template-columns: 1fr; gap: 18px; margin-top: 15px;">
                <div style="background: rgba(11, 19, 41, 0.85); border: 2px solid rgba(0, 255, 157, 0.4); border-radius: 14px; padding: 18px;">
                    <div style="font-size: 20px; font-weight: 800; color: #00ff9d;">1. 💸 {t('rule1_title')}</div>
                    <div style="font-size: 16px; color: #f1f5f9; margin-top: 6px; line-height: 1.6;">{t('rule1_desc')}</div>
                </div>
                <div style="background: rgba(11, 19, 41, 0.85); border: 2px solid rgba(255, 51, 102, 0.4); border-radius: 14px; padding: 18px;">
                    <div style="font-size: 20px; font-weight: 800; color: #ff3366;">2. 📱 {t('rule2_title')}</div>
                    <div style="font-size: 16px; color: #f1f5f9; margin-top: 6px; line-height: 1.6;">{t('rule2_desc')}</div>
                </div>
                <div style="background: rgba(11, 19, 41, 0.85); border: 2px solid rgba(255, 183, 3, 0.4); border-radius: 14px; padding: 18px;">
                    <div style="font-size: 20px; font-weight: 800; color: #ffb703;">3. ⚡ {t('rule3_title')}</div>
                    <div style="font-size: 16px; color: #f1f5f9; margin-top: 6px; line-height: 1.6;">{t('rule3_desc')}</div>
                </div>
                <div style="background: rgba(11, 19, 41, 0.85); border: 2px solid rgba(0, 240, 255, 0.4); border-radius: 14px; padding: 18px;">
                    <div style="font-size: 20px; font-weight: 800; color: #00f0ff;">4. 👨‍👩‍👧 {t('rule4_title')}</div>
                    <div style="font-size: 16px; color: #f1f5f9; margin-top: 6px; line-height: 1.6;">{t('rule4_desc')}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Common Senior Targeted Scam Scenarios
    st.markdown(
        f"""<h2 style="color: #ffffff; font-size: 24px;">🛡️ {'Common Traps Aimed at Senior Citizens' if lang == 'en' else 'ಹಿರಿಯ ನಾಗರಿಕರನ್ನು ಗುರಿಯಾಗಿಸುವ ಪ್ರಮುಖ ವಂಚನೆಗಳು'}</h2>""",
        unsafe_allow_html=True,
    )

    for idx, sc in enumerate(SENIOR_SCENARIOS):
        sc_id = sc["id"]
        sc_title = sc["title_en"] if lang == "en" else sc["title_kn"]
        sc_desc = sc["desc_en"] if lang == "en" else sc["desc_kn"]
        sc_rule = sc["rule_en"] if lang == "en" else sc["rule_kn"]

        is_done = is_lesson_completed(user["id"], "senior_citizen", sc_id)
        pill = (
            """<span class="badge-pill badge-green" style="font-size: 14px;">✓ COMPLETED</span>"""
            if is_done
            else """<span class="badge-pill badge-amber" style="font-size: 14px;">IMPORTANT</span>"""
        )

        with st.expander(f"{sc.get('icon', '👵')} {sc_title}", expanded=(idx == 0)):
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <div style="font-size: 18px; font-weight: 700; color: #00f0ff;">{sc_title}</div>
                    <div>{pill}</div>
                </div>
                <div class="cyber-card" style="padding: 18px; background: rgba(15,23,42,0.9); margin-bottom: 15px;">
                    <h4 style="color: #ff3366; margin-top: 0; font-size: 18px;">⚠️ {'What Scammers Tell You:' if lang == 'en' else 'ವಂಚಕರು ಹೇಗೆ ಸುಳ್ಳು ಹೇಳುತ್ತಾರೆ:'}</h4>
                    <p style="font-size: 16px; color: #f8fafc; line-height: 1.7; margin: 0;">"{sc_desc}"</p>
                </div>
                <div class="cyber-card cyber-card-success" style="padding: 18px; margin-bottom: 15px;">
                    <h4 style="color: #00ff9d; margin-top: 0; font-size: 18px;">🛡️ {'The Safe Rule to Follow:' if lang == 'en' else 'ನೀವು ಪಾಲಿಸಬೇಕಾದ ಸುರಕ್ಷಿತ ನಿಯಮ:'}</h4>
                    <p style="font-size: 16px; color: #f8fafc; line-height: 1.7; margin: 0; font-weight: 600;">{sc_rule}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if not is_done:
                if st.button(
                    f"✅ {t('mark_as_completed')}",
                    key=f"complete_senior_{sc_id}",
                ):
                    mark_lesson_completed(user["id"], "senior_citizen", sc_id)
                    st.success(t("lesson_completed"))
                    st.rerun()
            else:
                st.info(f"✓ {t('already_completed')}")

    # Refrigerator / Wallet Emergency Printable Safety Card
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="cyber-card" style="border: 2px dashed #00f0ff; background: rgba(7, 13, 30, 0.95); padding: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(0,240,255,0.3); padding-bottom: 10px; margin-bottom: 15px;">
                <div style="font-size: 20px; font-weight: 800; color: #00f0ff;">
                    📋 {'SENIOR CITIZEN EMERGENCY WALLET & FRIDGE CARD' if lang == 'en' else 'ಹಿರಿಯ ನಾಗರಿಕರ ತುರ್ತು ಸುರಕ್ಷಾ ಕಾರ್ಡ್'}
                </div>
                <div style="color: #00ff9d; font-weight: 700;">CYBERSHIELD DEFENSE</div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; font-size: 15px; color: #f1f5f9;">
                <div><b>📞 National Cyber Helpline:</b> 1930</div>
                <div><b>🌐 Official Complaint Portal:</b> cybercrime.gov.in</div>
                <div><b>🛑 Rule #1:</b> NEVER tell OTP or UPI PIN on calls</div>
                <div><b>🛑 Rule #2:</b> NEVER install AnyDesk / TeamViewer</div>
                <div><b>🛑 Rule #3:</b> Receiving money NEVER requires PIN</div>
                <div><b>🛑 Rule #4:</b> When in doubt, call your children or bank</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_footer()


if __name__ == "__main__":
    main()
