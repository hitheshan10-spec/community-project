"""
CyberShield Digital Safety Guide
Comprehensive operational security manual covering 9 vital digital defense pillars.
"""

import json
import os
import sys
import streamlit as st

st.set_page_config(
    page_title="Digital Safety Guide - CyberShield",
    page_icon="🛡️",
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

GUIDE_PATH = os.path.join(BASE_DIR, "data", "safety_guides.json")


def load_guide_data():
    if os.path.exists(GUIDE_PATH):
        with open(GUIDE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def main():
    lang = get_current_language()
    title = t("nav_digital_safety")
    subtitle = (
        "Practical defensive protocols to secure your passwords, 2FA, UPI apps, smartphone, public Wi-Fi, and Aadhaar identity."
        if lang == "en"
        else "ಪಾಸ್‌ವರ್ಡ್, ದ್ವಿ-ಹಂತದ ದೃಢೀಕರಣ (2FA), ಯುಪಿಐ, ಸಾರ್ವಜನಿಕ ವೈ-ಫೈ ಮತ್ತು ಆಧಾರ್ ಡೇಟಾ ರಕ್ಷಿಸಲು ಪ್ರಾಯೋಗಿಕ ಮಾರ್ಗದರ್ಶಿ."
    )
    render_page_header(title, subtitle, badge_text="9 CORE DEFENSE PILLARS")

    guides = load_guide_data()
    user = get_active_user()

    # Interactive Digital Security Self-Assessment Card
    st.markdown(
        f"""
        <div class="cyber-card cyber-card-accent" style="margin-bottom: 25px;">
            <div style="display: flex; gap: 15px; align-items: center;">
                <span style="font-size: 32px;">📊</span>
                <div style="flex: 1;">
                    <h3 style="margin: 0 0 4px 0; color: #00f0ff;">
                        {'Personal Digital Hygiene Self-Check' if lang == 'en' else 'ನಿಮ್ಮ ವೈಯಕ್ತಿಕ ಡಿಜಿಟಲ್ ಸುರಕ್ಷತೆ ಸ್ವಯಂ-ಪರೀಕ್ಷೆ'}
                    </h3>
                    <p style="margin: 0; color: #94a3b8; font-size: 14px;">
                        {'Tick the security habits you currently follow to calculate your personal Digital Shield Score.' if lang == 'en' else 'ನೀವು ಪ್ರಸ್ತುತ ಪಾಲಿಸುತ್ತಿರುವ ಸುರಕ್ಷತಾ ನಿಯಮಗಳನ್ನು ಆಯ್ಕೆ ಮಾಡಿ ನಿಮ್ಮ ಸ್ಕೋರ್ ತಿಳಿಯಿರಿ.'}
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    check_cols = st.columns(3)
    c1 = check_cols[0].checkbox("🔑 " + ("Unique 12+ char passwords" if lang == "en" else "ಪ್ರತ್ಯೇಕ ಬಲಿಷ್ಠ ಪಾಸ್‌ವರ್ಡ್"), key="chk_1")
    c2 = check_cols[1].checkbox("🛡️ " + ("2FA enabled on Google/WhatsApp" if lang == "en" else "2FA ಸಕ್ರಿಯಗೊಳಿಸಲಾಗಿದೆ"), key="chk_2")
    c3 = check_cols[2].checkbox("💸 " + ("Never enter PIN to receive money" if lang == "en" else "ಹಣ ಪಡೆಯಲು ಪಿನ್ ಹಾಕುವುದಿಲ್ಲ"), key="chk_3")
    c4 = check_cols[0].checkbox("📶 " + ("No banking on public Wi-Fi" if lang == "en" else "ಸಾರ್ವಜನಿಕ ವೈ-ಫೈನಲ್ಲಿ ಬ್ಯಾಂಕಿಂಗ್ ಮಾಡುವುದಿಲ್ಲ"), key="chk_4")
    c5 = check_cols[1].checkbox("📲 " + ("Only official app stores used" if lang == "en" else "ಪ್ಲೇಸ್ಟೋರ್‌ನಿಂದ ಮಾತ್ರ ಆ್ಯಪ್ ಬಳಕೆ"), key="chk_5")
    c6 = check_cols[2].checkbox("🪪 " + ("Masked Aadhaar / Bio lock active" if lang == "en" else "ಮಾಸ್ಕ್ಡ್ ಆಧಾರ್ / ಬಯೋಮೆಟ್ರಿಕ್ ಲಾಕ್"), key="chk_6")

    score = sum([c1, c2, c3, c4, c5, c6]) * (100 // 6)
    score_color = "#00ff9d" if score >= 80 else ("#ffb703" if score >= 50 else "#ff3366")
    st.markdown(
        f"""
        <div style="background: rgba(11,19,41,0.8); border: 1px solid rgba(0,240,255,0.2); border-radius: 10px; padding: 10px 18px; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 14px; color: #94a3b8;">{'Your Hygiene Shield Score:' if lang == 'en' else 'ನಿಮ್ಮ ಸುರಕ್ಷತಾ ಶೀಲ್ಡ್ ಸ್ಕೋರ್:'}</span>
            <span style="font-size: 20px; font-weight: 800; color: {score_color}; font-family: 'JetBrains Mono';">{score}%</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Render Guides
    for idx, guide in enumerate(guides):
        g_id = guide["id"]
        g_title = guide["title_en"] if lang == "en" else guide["title_kn"]
        g_summary = guide["summary_en"] if lang == "en" else guide["summary_kn"]
        g_advice = guide["core_advice_en"] if lang == "en" else guide["core_advice_kn"]
        g_dos = guide["dos_en"] if lang == "en" else guide["dos_kn"]
        g_donts = guide["donts_en"] if lang == "en" else guide["donts_kn"]

        is_done = is_lesson_completed(user["id"], "digital_safety", g_id)
        status_pill = (
            """<span class="badge-pill badge-green">✓ COMPLETED</span>"""
            if is_done
            else """<span class="badge-pill badge-cyan">GUIDE</span>"""
        )

        with st.expander(f"{guide.get('icon', '🛡️')} {g_title}", expanded=(idx == 0)):
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid rgba(0,240,255,0.15); padding-bottom: 10px;">
                    <div style="font-size: 15px; color: #00f0ff; font-weight: 600;">{g_summary}</div>
                    <div>{status_pill}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Core advice callout
            st.markdown(
                f"""
                <div class="cyber-card" style="background: rgba(0, 240, 255, 0.05); border-left: 4px solid #00f0ff; padding: 16px; margin-bottom: 18px;">
                    <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 6px;">
                        <span style="font-size: 20px;">💡</span>
                        <h4 style="margin: 0; color: #00f0ff;">{'Core Security Principle' if lang == 'en' else 'ಪ್ರಮುಖ ಸುರಕ್ಷತಾ ನಿಯಮ'}</h4>
                    </div>
                    <p style="margin: 0; color: #f8fafc; font-size: 15px; line-height: 1.6;">{g_advice}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            col_dos, col_donts = st.columns(2)

            with col_dos:
                st.markdown(
                    f"""
                    <div class="cyber-card cyber-card-success" style="height: 100%; padding: 18px;">
                        <h4 style="color: #00ff9d; margin-top: 0;">✅ {'Best Practices (Do This)' if lang == 'en' else 'ಉತ್ತಮ ಅಭ್ಯಾಸಗಳು (ಮಾಡಬೇಕಾದವು)'}</h4>
                        <ul style="color: #cbd5e1; font-size: 14px; line-height: 1.7; padding-left: 20px; margin-bottom: 0;">
                            {''.join([f"<li>{do}</li>" for do in g_dos])}
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col_donts:
                st.markdown(
                    f"""
                    <div class="cyber-card cyber-card-danger" style="height: 100%; padding: 18px;">
                        <h4 style="color: #ff3366; margin-top: 0;">❌ {'Critical Hazards (Never Do This)' if lang == 'en' else 'ಅಪಾಯಕಾರಿ ತಪ್ಪುಗಳು (ಮಾಡಬಾರದವು)'}</h4>
                        <ul style="color: #cbd5e1; font-size: 14px; line-height: 1.7; padding-left: 20px; margin-bottom: 0;">
                            {''.join([f"<li>{dont}</li>" for dont in g_donts])}
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

            if not is_done:
                if st.button(
                    f"✅ {t('mark_as_completed')}",
                    key=f"complete_guide_{g_id}",
                ):
                    mark_lesson_completed(user["id"], "digital_safety", g_id)
                    st.success(t("lesson_completed"))
                    st.rerun()
            else:
                st.info(f"✓ {t('already_completed')}")

    render_footer()


if __name__ == "__main__":
    main()
