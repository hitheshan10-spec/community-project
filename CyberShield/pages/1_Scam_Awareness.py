"""
CyberShield Scam Awareness Centre
Comprehensive educational modules covering 12 major cyber fraud attack vectors in India.
"""

import json
import os
import sys
import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="Scam Awareness Centre - CyberShield",
    page_icon="🚨",
    layout="wide",
)

# Include parent directory in sys.path
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

DATA_PATH = os.path.join(BASE_DIR, "data", "scams.json")


def load_scam_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def main():
    lang = get_current_language()
    title = t("nav_scam_awareness")
    subtitle = (
        "In-depth analysis of 12 prevalent cyber fraud vectors: attack mechanics, red flags, fictional case studies, and defense protocols."
        if lang == "en"
        else "12 ಪ್ರಮುಖ ಸೈಬರ್ ವಂಚನೆಗಳ ಸಮಗ್ರ ಅಧ್ಯಯನ: ದಾಳಿಯ ವಿಧಾನ, ಎಚ್ಚರಿಕೆಯ ಚಿಹ್ನೆಗಳು, ನೈಜ ಉದಾಹರಣೆಗಳು ಮತ್ತು ರಕ್ಷಣಾ ಕ್ರಮಗಳು."
    )
    render_page_header(title, subtitle, badge_text="12 THREAT PROFILES")

    scams = load_scam_data()
    user = get_active_user()

    # Search & Filter bar
    s_col1, s_col2 = st.columns([3, 1])
    with s_col1:
        search_query = st.text_input(
            "🔍 " + ("Search scams by keyword or title..." if lang == "en" else "ವಂಚನೆಗಳನ್ನು ಹುಡುಕಿ..."),
            "",
            key="scam_search_input",
        )
    with s_col2:
        category_options = [
            ("All Scams" if lang == "en" else "ಎಲ್ಲಾ ವಂಚನೆಗಳು"),
            ("Banking & UPI" if lang == "en" else "ಬ್ಯಾಂಕಿಂಗ್ ಮತ್ತು ಯುಪಿಐ"),
            ("Social Engineering" if lang == "en" else "ಸಾಮಾಜಿಕ ಮೋಸಗಳು"),
            ("Tech & Identity" if lang == "en" else "ತಂತ್ರಜ್ಞಾನ ಮತ್ತು ಗುರುತು"),
        ]
        selected_cat = st.selectbox(
            "📁 " + ("Filter Category" if lang == "en" else "ವರ್ಗ"),
            options=category_options,
            key="scam_cat_filter",
        )

    # Filter logic
    filtered_scams = []
    for s in scams:
        title_text = s.get("title_en" if lang == "en" else "title_kn", "")
        summary_text = s.get("summary_en" if lang == "en" else "summary_kn", "")
        full_text = f"{title_text} {summary_text} {s['id']}".lower()

        if search_query.strip() and search_query.strip().lower() not in full_text:
            continue

        # Optional category tag mapping
        if selected_cat in ("Banking & UPI", "ಬ್ಯಾಂಕಿಂಗ್ ಮತ್ತು ಯುಪಿಐ"):
            if s["id"] not in ("upi_fraud", "otp_fraud", "qr_code_scams", "phishing_scams"):
                continue
        elif selected_cat in ("Social Engineering", "ಸಾಮಾಜಿಕ ಮೋಸಗಳು"):
            if s["id"] not in ("fake_job_offers", "lottery_scams", "social_media_scams", "fake_customer_care", "online_shopping_scams", "investment_scams"):
                continue
        elif selected_cat in ("Tech & Identity", "ತಂತ್ರಜ್ಞಾನ ಮತ್ತು ಗುರುತು"):
            if s["id"] not in ("remote_access_scams", "identity_theft"):
                continue

        filtered_scams.append(s)

    st.markdown(
        f"<p style='color: #94a3b8; font-size: 14px;'>Showing <b>{len(filtered_scams)}</b> scam lessons</p>",
        unsafe_allow_html=True,
    )

    if not filtered_scams:
        st.warning("No scams match your search criteria. Try a different query.")
        return

    # Render each scam as a detailed interactive card
    for idx, scam in enumerate(filtered_scams):
        s_id = scam["id"]
        s_title = scam["title_en"] if lang == "en" else scam["title_kn"]
        s_summary = scam["summary_en"] if lang == "en" else scam["summary_kn"]
        s_what = scam["what_is_it_en"] if lang == "en" else scam["what_is_it_kn"]
        s_how_list = scam["how_it_works_en"] if lang == "en" else scam["how_it_works_kn"]
        s_warnings = scam["warning_signs_en"] if lang == "en" else scam["warning_signs_kn"]
        s_example = scam["fictional_example_en"] if lang == "en" else scam["fictional_example_kn"]
        s_prevent = scam["prevention_methods_en"] if lang == "en" else scam["prevention_methods_kn"]

        is_done = is_lesson_completed(user["id"], "scam_awareness", s_id)
        status_badge = (
            """<span class="badge-pill badge-green">✓ COMPLETED</span>"""
            if is_done
            else """<span class="badge-pill badge-amber">INCOMPLETE</span>"""
        )

        with st.expander(f"{scam.get('icon', '🚨')} {s_title}", expanded=(idx == 0)):
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid rgba(0,240,255,0.15); padding-bottom: 10px;">
                    <div style="font-size: 15px; color: #00f0ff; font-weight: 600;">{s_summary}</div>
                    <div>{status_badge}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # What is it?
            st.markdown(
                f"""
                <div class="cyber-card" style="padding: 16px; margin-bottom: 15px;">
                    <h4 style="color: #00f0ff; margin-top: 0; margin-bottom: 8px;">📖 {'What is this attack?' if lang == 'en' else 'ಈ ದಾಳಿ ಎಂದರೇನು?'}</h4>
                    <p style="color: #e2e8f0; font-size: 15px; line-height: 1.6; margin: 0;">{s_what}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            c_left, c_right = st.columns(2)

            with c_left:
                # How it works (attack flow)
                st.markdown(
                    f"""
                    <div class="cyber-card cyber-card-warning" style="height: 100%; padding: 18px;">
                        <h4 style="color: #ffb703; margin-top: 0;">⚙️ {t('how_it_works_heading')}</h4>
                        <ol style="color: #cbd5e1; font-size: 14px; line-height: 1.7; padding-left: 20px; margin-bottom: 0;">
                            {''.join([f"<li>{step}</li>" for step in s_how_list])}
                        </ol>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with c_right:
                # Warning signs
                st.markdown(
                    f"""
                    <div class="cyber-card cyber-card-danger" style="height: 100%; padding: 18px;">
                        <h4 style="color: #ff3366; margin-top: 0;">🚩 {t('warning_signs_heading')}</h4>
                        <ul style="color: #cbd5e1; font-size: 14px; line-height: 1.7; padding-left: 20px; margin-bottom: 0;">
                            {''.join([f"<li>{w}</li>" for w in s_warnings])}
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

            # Fictional real-life incident scenario
            st.markdown(
                f"""
                <div class="cyber-card" style="background: rgba(15, 23, 42, 0.85); border-left: 4px solid #a855f7; padding: 18px;">
                    <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 6px;">
                        <span style="font-size: 22px;">🎭</span>
                        <h4 style="color: #c084fc; margin: 0;">{t('real_life_example_heading')}</h4>
                    </div>
                    <p style="color: #f1f5f9; font-style: italic; font-size: 14px; line-height: 1.6; margin: 0;">
                        "{s_example}"
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Prevention protocols
            st.markdown(
                f"""
                <div class="cyber-card cyber-card-success" style="padding: 18px; margin-top: 15px;">
                    <h4 style="color: #00ff9d; margin-top: 0;">🛡️ {t('prevention_heading')}</h4>
                    <ul style="color: #e2e8f0; font-size: 14px; line-height: 1.7; padding-left: 20px; margin-bottom: 0;">
                        {''.join([f"<li><b>{p}</b></li>" for p in s_prevent])}
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Actions row
            btn_col1, btn_col2 = st.columns([2, 1])
            with btn_col1:
                if not is_done:
                    if st.button(
                        f"✅ {t('mark_as_completed')}",
                        key=f"complete_scam_{s_id}",
                    ):
                        mark_lesson_completed(user["id"], "scam_awareness", s_id)
                        st.success(t("lesson_completed"))
                        st.rerun()
                else:
                    st.info(f"✓ {t('already_completed')}")

            with btn_col2:
                if st.button(
                    "🔍 " + ("Test in Scam Checker" if lang == "en" else "ಸ್ಕ್ಯಾಮರ್‌ನಲ್ಲಿ ಪರೀಕ್ಷಿಸಿ"),
                    key=f"jump_checker_{s_id}",
                ):
                    st.switch_page("pages/3_Scam_Checker.py")

    render_footer()


if __name__ == "__main__":
    main()
