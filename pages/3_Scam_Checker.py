"""
CyberShield Online Scam Checker
Analyzes suspicious text messages, SMS, WhatsApp forwards, and emails using rule-based heuristics.
"""

import os
import sys
import streamlit as st

st.set_page_config(
    page_title="Scam Checker - CyberShield",
    page_icon="🔍",
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
from utils.scam_detection import analyze_message, SAMPLE_SCAMS
from database.database import record_scam_scan


def main():
    lang = get_current_language()
    title = t("scam_checker_title")
    subtitle = t("scam_checker_subtitle")
    render_page_header(title, subtitle, badge_text="RULE-BASED AI ENGINE")

    user = get_active_user()

    # Privacy Guarantee Card
    st.markdown(
        f"""
        <div style="background: rgba(0, 255, 157, 0.06); border: 1px solid rgba(0, 255, 157, 0.25); border-radius: 12px; padding: 12px 18px; margin-bottom: 20px;">
            <div style="display: flex; gap: 10px; align-items: center;">
                <span style="font-size: 20px;">🔒</span>
                <div style="font-size: 13px; color: #cbd5e1;">
                    <b>{'Local & Private Analysis:' if lang == 'en' else 'ಗೌಪ್ಯತೆ ಭರವಸೆ:'}</b>
                    {' All text is evaluated locally inside your browser environment. Never paste actual passwords, live banking credentials, or personal identity numbers.' if lang == 'en' else ' ಎಲ್ಲಾ ಪಠ್ಯವನ್ನು ಸ್ಥಳೀಯವಾಗಿ ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತದೆ. ನಿಮ್ಮ ನಿಜವಾದ ಪಾಸ್‌ವರ್ಡ್ ಅಥವಾ ರಹಸ್ಯ ಬ್ಯಾಂಕ್ ಪಿನ್ ವಿವರಗಳನ್ನು ಎಂದಿಗೂ ನಮೂದಿಸಬೇಡಿ.'}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Initialize session state for input
    if "checker_input_text" not in st.session_state:
        st.session_state["checker_input_text"] = ""

    # Sample Pre-load Buttons
    st.markdown(f"#### ⚡ {t('sample_prompts_title')}")
    sample_cols = st.columns(3)
    for i, sample in enumerate(SAMPLE_SCAMS):
        col_idx = i % 3
        with sample_cols[col_idx]:
            if st.button(sample["title"], key=f"btn_sample_{i}", use_container_width=True):
                st.session_state["checker_input_text"] = sample["text"]
                st.rerun()

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Text Input Area
    input_text = st.text_area(
        "📝 " + ("Message Content to Analyze" if lang == "en" else "ವಿಶ್ಲೇಷಿಸಬೇಕಾದ ಸಂದೇಶ"),
        value=st.session_state["checker_input_text"],
        height=140,
        placeholder=t("paste_placeholder"),
        key="main_scam_textarea",
    )

    col_act1, col_act2 = st.columns([1, 4])
    with col_act1:
        analyze_clicked = st.button(
            f"🔍 {t('analyze_btn')}",
            key="btn_run_analysis",
            type="primary",
            use_container_width=True,
        )
    with col_act2:
        if st.button("🗑️ " + ("Clear Input" if lang == "en" else "ಅಳಿಸಿ"), key="btn_clear_input"):
            st.session_state["checker_input_text"] = ""
            st.rerun()

    # Perform Analysis
    if analyze_clicked or input_text.strip():
        if not input_text.strip():
            st.warning("Please paste or type a message before analyzing.")
            return

        result = analyze_message(input_text)

        # Log scan in database
        triggers_summary = ", ".join([tr["category"] for tr in result["detected_triggers"]])
        record_scam_scan(
            user["id"],
            input_text[:80],
            result["risk_level"],
            result["risk_score"],
            triggers_summary,
        )

        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

        # Result Summary Card
        risk_color = result["risk_color"]
        badge_style = f"background: {risk_color}22; color: {risk_color}; border: 1px solid {risk_color}88;"

        st.markdown(
            f"""
            <div class="cyber-card" style="border-left: 6px solid {risk_color}; margin-top: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; margin-bottom: 12px;">
                    <div>
                        <span class="badge-pill" style="{badge_style}; font-size: 14px; padding: 6px 14px;">
                            {result['risk_level']}
                        </span>
                        <h2 style="margin: 8px 0 2px 0; color: #ffffff;">{result['scam_category']}</h2>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 13px; color: #94a3b8; font-weight: 600;">CALCULATED THREAT INDEX</div>
                        <div style="font-size: 36px; font-weight: 800; color: {risk_color}; font-family: 'JetBrains Mono';">
                            {result['risk_score']}<span style="font-size: 20px; color: #64748b;">/100</span>
                        </div>
                    </div>
                </div>
                <div style="background: rgba(255,255,255,0.05); border-radius: 8px; height: 8px; width: 100%; overflow: hidden; margin-bottom: 15px;">
                    <div style="background: {risk_color}; height: 8px; width: {result['risk_score']}%; transition: width 0.5s ease;"></div>
                </div>
                <p style="color: #f1f5f9; font-size: 15px; line-height: 1.6; margin: 0;">
                    {result['explanation']}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Trigger Breakdown & Recommendations Grid
        col_res1, col_res2 = st.columns(2)

        with col_res1:
            st.markdown(
                f"""
                <div class="cyber-card" style="height: 100%;">
                    <h4 style="color: #00f0ff; margin-top: 0;">🚩 {t('detected_red_flags')}</h4>
                """,
                unsafe_allow_html=True,
            )
            if result["detected_triggers"]:
                for tr in result["detected_triggers"]:
                    st.markdown(
                        f"""
                        <div style="background: rgba(11, 19, 41, 0.7); border: 1px solid rgba(0, 240, 255, 0.2); border-radius: 10px; padding: 12px; margin-bottom: 10px;">
                            <div style="color: #ffb703; font-weight: 700; font-size: 14px;">⚠️ {tr['category']}</div>
                            <div style="color: #f8fafc; font-size: 13px; margin: 4px 0;">{tr['red_flag']}</div>
                            <div style="color: #94a3b8; font-size: 12px; font-style: italic;">💡 {tr['advice']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(
                    f"""
                    <div style="color: #00ff9d; font-size: 14px; padding: 15px 0;">
                        ✅ {'No specific high-threat keywords or malicious URL patterns identified.' if lang == 'en' else 'ಯಾವುದೇ ಹೆಚ್ಚಿನ ಬೆದರಿಕೆಯ ಲಕ್ಷಣಗಳು ಕಂಡುಬಂದಿಲ್ಲ.'}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

        with col_res2:
            st.markdown(
                f"""
                <div class="cyber-card" style="height: 100%;">
                    <h4 style="color: #00ff9d; margin-top: 0;">🛡️ {t('recommendations_heading')}</h4>
                    <ul style="color: #f1f5f9; font-size: 14px; line-height: 1.8; padding-left: 20px;">
                        {''.join([f"<li>{rec}</li>" for rec in result['recommendations']])}
                    </ul>
                    <div style="margin-top: 20px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.1);">
                        <a href="pages/7_Emergency_Help.py" target="_self" style="text-decoration: none;">
                            <span class="badge-pill badge-red" style="padding: 8px 16px; font-size: 13px; cursor: pointer;">
                                📞 Incident Response: National Helpline 1930
                            </span>
                        </a>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    render_footer()


if __name__ == "__main__":
    main()
