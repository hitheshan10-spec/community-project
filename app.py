"""
CYBERSHIELD: Your Digital Safety Companion
Main Streamlit Application & Home Dashboard
"""

import os
import sys
import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="CyberShield - Digital Safety Companion",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Set path to include local packages
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from utils.progress import (
    apply_custom_css,
    render_sidebar_profile,
    get_active_user,
    render_footer,
)
from utils.translation import t, get_current_language
from database.database import get_user_dashboard_stats


def main():
    apply_custom_css()
    render_sidebar_profile()

    user = get_active_user()
    stats = get_user_dashboard_stats(user["id"])
    lang = get_current_language()

    # Hero Banner
    logo_path = os.path.join(CURRENT_DIR, "assets", "logo.png")
    col_hero_1, col_hero_2 = st.columns([1, 4])

    with col_hero_1:
        if os.path.exists(logo_path):
            st.image(logo_path, width=170)
        else:
            st.markdown(
                """<div style="font-size: 90px; text-align: center; filter: drop-shadow(0 0 15px #00f0ff);">🛡️</div>""",
                unsafe_allow_html=True,
            )

    with col_hero_2:
        title_text = t("app_title")
        subtitle_text = t("app_subtitle")
        tagline_text = t("app_tagline")

        st.markdown(
            f"""
            <div style="padding-top: 10px;">
                <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 6px;">
                    <span class="badge-pill badge-green">🛡️ National Cyber Awareness Initiative</span>
                    <span class="badge-pill badge-cyan">v2.5 Local Edition</span>
                </div>
                <h1 style="margin: 0; font-size: 3rem; background: linear-gradient(135deg, #00f0ff 0%, #00ff9d 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{title_text}</h1>
                <h3 style="margin: 4px 0 8px 0; color: #e2e8f0; font-weight: 500;">{subtitle_text}</h3>
                <p style="color: #00ff9d; font-family: 'JetBrains Mono', monospace; font-size: 16px; font-weight: 600; margin: 0 0 10px 0;">{tagline_text}</p>
                <p style="color: #94a3b8; font-size: 15px; margin: 0; max-width: 820px;">{t('welcome_banner_desc')}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # National Emergency Alert Banner
    st.markdown(
        f"""
        <div class="cyber-card cyber-card-danger" style="padding: 16px 24px; background: rgba(255, 51, 102, 0.08);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                <div style="display: flex; align-items: center; gap: 14px;">
                    <span style="font-size: 32px;">🚨</span>
                    <div>
                        <div style="color: #ff3366; font-weight: 800; font-size: 15px; text-transform: uppercase; letter-spacing: 0.05em;">Financial Fraud Alert • Indian Cybercrime Helpline</div>
                        <div style="color: #f1f5f9; font-size: 14px;">If you have lost money to a scam within the last 2 hours, call <b>1930</b> immediately to freeze scammed accounts.</div>
                    </div>
                </div>
                <div style="display: flex; gap: 10px;">
                    <a href="pages/7_Emergency_Help.py" target="_self" style="text-decoration: none;">
                        <span class="badge-pill badge-red" style="font-size: 14px; padding: 8px 16px; cursor: pointer;">📞 Dial 1930 Emergency Guide</span>
                    </a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Real-Time Platform Key Metrics
    st.markdown(
        f"""<h3 style="margin-top: 15px; margin-bottom: 12px; color: #ffffff;">📊 {t('stats_overview')}</h3>""",
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(
            f"""
            <div class="cyber-card" style="text-align: center; padding: 20px 10px;">
                <div style="font-size: 26px;">📚</div>
                <div style="font-size: 28px; font-weight: 800; color: #00f0ff; font-family: 'JetBrains Mono';">9</div>
                <div style="color: #94a3b8; font-size: 13px; font-weight: 600;">{t('total_modules')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            f"""
            <div class="cyber-card" style="text-align: center; padding: 20px 10px;">
                <div style="font-size: 26px;">⚠️</div>
                <div style="font-size: 28px; font-weight: 800; color: #ffb703; font-family: 'JetBrains Mono';">12</div>
                <div style="color: #94a3b8; font-size: 13px; font-weight: 600;">{t('scam_types_covered')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            f"""
            <div class="cyber-card" style="text-align: center; padding: 20px 10px;">
                <div style="font-size: 26px;">🎯</div>
                <div style="font-size: 28px; font-weight: 800; color: #00ff9d; font-family: 'JetBrains Mono';">30+</div>
                <div style="color: #94a3b8; font-size: 13px; font-weight: 600;">{t('quiz_questions_count')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m4:
        st.markdown(
            f"""
            <div class="cyber-card" style="text-align: center; padding: 20px 10px;">
                <div style="font-size: 26px;">📞</div>
                <div style="font-size: 28px; font-weight: 800; color: #ff3366; font-family: 'JetBrains Mono';">1930</div>
                <div style="color: #94a3b8; font-size: 13px; font-weight: 600;">{t('helpline_active')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Core Navigation Modules Grid
    st.markdown(
        f"""<h3 style="margin-top: 25px; margin-bottom: 12px; color: #ffffff;">🧭 {t('quick_nav_title')}</h3>""",
        unsafe_allow_html=True,
    )

    card_c1, card_c2 = st.columns(2)

    with card_c1:
        st.markdown(
            f"""
            <div class="cyber-card cyber-card-accent">
                <div style="display: flex; gap: 14px; align-items: flex-start;">
                    <div style="font-size: 38px;">🚨</div>
                    <div style="flex: 1;">
                        <span class="badge-pill badge-cyan">ESSENTIAL KNOWLEDGE</span>
                        <h3 style="margin: 6px 0; font-size: 20px; color: #ffffff;">{t('nav_scam_awareness')}</h3>
                        <p style="color: #94a3b8; font-size: 14px; margin-bottom: 14px;">
                            {'Learn how phishing, OTP fraud, UPI collect traps, lottery messages, and remote access scams operate with real fictional incident scenarios.' if lang == 'en' else 'ಫಿಶಿಂಗ್, ಒಟಿಪಿ ವಂಚನೆ, ಯುಪಿಐ ಟ್ರ್ಯಾಪ್, ಲಾಟರಿ ಮತ್ತು ರಿಮೋಟ್ ಆ್ಯಪ್ ವಂಚನೆಗಳು ಹೇಗೆ ನಡೆಯುತ್ತವೆ ಎಂಬುದನ್ನು ವಿವರವಾಗಿ ಕಲಿಯಿರಿ.'}
                        </p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            f"📖 {t('nav_scam_awareness')}",
            key="btn_go_scams",
            use_container_width=True,
        ):
            st.switch_page("pages/1_Scam_Awareness.py")

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="cyber-card cyber-card-warning">
                <div style="display: flex; gap: 14px; align-items: flex-start;">
                    <div style="font-size: 38px;">🔍</div>
                    <div style="flex: 1;">
                        <span class="badge-pill badge-amber">DETECTION TOOL</span>
                        <h3 style="margin: 6px 0; font-size: 20px; color: #ffffff;">{t('nav_scam_checker')}</h3>
                        <p style="color: #94a3b8; font-size: 14px; margin-bottom: 14px;">
                            {'Paste suspicious SMS, WhatsApp forwards, or emails to analyze urgency, links, OTP triggers, and fake lottery rewards in real time.' if lang == 'en' else 'ಅನುಮಾನಾಸ್ಪದ SMS, ವಾಟ್ಸಾಪ್ ಸಂದೇಶ ಅಥವಾ ಇಮೇಲ್ ಪೇಸ್ಟ್ ಮಾಡಿ ಅಪಾಯದ ಮಟ್ಟವನ್ನು ಕ್ಷಣಾರ್ಧದಲ್ಲಿ ಪರೀಕ್ಷಿಸಿ.'}
                        </p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            f"🔍 {t('check_message_btn')}",
            key="btn_go_checker",
            use_container_width=True,
        ):
            st.switch_page("pages/3_Scam_Checker.py")

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="cyber-card cyber-card-accent">
                <div style="display: flex; gap: 14px; align-items: flex-start;">
                    <div style="font-size: 38px;">🎓</div>
                    <div style="flex: 1;">
                        <span class="badge-pill badge-cyan">YOUTH & STUDENTS</span>
                        <h3 style="margin: 6px 0; font-size: 20px; color: #ffffff;">{t('nav_student_zone')}</h3>
                        <p style="color: #94a3b8; font-size: 14px; margin-bottom: 14px;">
                            {'Protect gaming credentials (Steam, BGMI), guard against cyberbullying, navigate AI deepfakes, and spot fake college internship traps.' if lang == 'en' else 'ಗೇಮಿಂಗ್ ಖಾತೆ ರಕ್ಷಣೆ, ಸೈಬರ್‌ಬುಲ್ಲಿಯಿಂಗ್ ತಡೆ ಮತ್ತು ನಕಲಿ ಇಂಟರ್ನ್‌ಶಿಪ್‌ಗಳಿಂದ ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ಸುರಕ್ಷತೆ.'}
                        </p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            f"🎓 {t('explore_student_btn')}",
            key="btn_go_student",
            use_container_width=True,
        ):
            st.switch_page("pages/5_Student_Zone.py")

    with card_c2:
        st.markdown(
            f"""
            <div class="cyber-card cyber-card-success">
                <div style="display: flex; gap: 14px; align-items: flex-start;">
                    <div style="font-size: 38px;">🛡️</div>
                    <div style="flex: 1;">
                        <span class="badge-pill badge-green">PRACTICAL DEFENSE</span>
                        <h3 style="margin: 6px 0; font-size: 20px; color: #ffffff;">{t('nav_digital_safety')}</h3>
                        <p style="color: #94a3b8; font-size: 14px; margin-bottom: 14px;">
                            {'9 core guides covering passphrases, two-factor authentication, public Wi-Fi safety, UPI hygiene, and biometric locking on mAadhaar.' if lang == 'en' else 'ಪಾಸ್‌ವರ್ಡ್, 2FA, ಸಾರ್ವಜನಿಕ ವೈ-ಫೈ, ಯುಪಿಐ ಮತ್ತು ಆಧಾರ್ ಬಯೋಮೆಟ್ರಿಕ್ ಲಾಕ್ ಮಾಡುವ 9 ಪ್ರಮುಖ ಮಾರ್ಗದರ್ಶಿಗಳು.'}
                        </p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            f"🛡️ {t('nav_digital_safety')}",
            key="btn_go_safety",
            use_container_width=True,
        ):
            st.switch_page("pages/2_Digital_Safety.py")

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="cyber-card cyber-card-accent">
                <div style="display: flex; gap: 14px; align-items: flex-start;">
                    <div style="font-size: 38px;">🎯</div>
                    <div style="flex: 1;">
                        <span class="badge-pill badge-cyan">SKILL TEST</span>
                        <h3 style="margin: 6px 0; font-size: 20px; color: #ffffff;">{t('nav_quiz_centre')}</h3>
                        <p style="color: #94a3b8; font-size: 14px; margin-bottom: 14px;">
                            {'Take interactive multi-tier cybersecurity quizzes (Easy, Medium, Hard), view instant explanations, and unlock Cyber Sentinel badges.' if lang == 'en' else 'ಸುಲಭ, ಮಧ್ಯಮ ಮತ್ತು ಕಠಿಣ ಹಂತದ ಸೈಬರ್ ರಸಪ್ರಶ್ನೆಗಳಲ್ಲಿ ಭಾಗವಹಿಸಿ ಸೈಬರ್ ಬ್ಯಾಡ್ಜ್‌ಗಳನ್ನು ಪಡೆಯಿರಿ.'}
                        </p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            f"🎯 {t('take_quiz_btn')}",
            key="btn_go_quiz",
            use_container_width=True,
        ):
            st.switch_page("pages/4_Quiz_Centre.py")

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="cyber-card cyber-card-warning">
                <div style="display: flex; gap: 14px; align-items: flex-start;">
                    <div style="font-size: 38px;">👴</div>
                    <div style="flex: 1;">
                        <span class="badge-pill badge-amber">ACCESSIBILITY FIRST</span>
                        <h3 style="margin: 6px 0; font-size: 20px; color: #ffffff;">{t('nav_senior_citizen')}</h3>
                        <p style="color: #94a3b8; font-size: 14px; margin-bottom: 14px;">
                            {'Large fonts, simplified language, audio-friendly guidance, and step-by-step defense against pension, electricity, and KYC phone calls.' if lang == 'en' else 'ಹಿರಿಯ ನಾಗರಿಕರಿಗಾಗಿ ದೊಡ್ಡ ಅಕ್ಷರಗಳೊಂದಿಗೆ ಸರಳ ಮಾರ್ಗದರ್ಶಿ ಮತ್ತು ವಿದ್ಯುತ್ ಬಿಲ್ ಹಾಗೂ ಪಿಂಚಣಿ ವಂಚನೆಗಳ ತಡೆ.'}
                        </p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            f"👴 {t('explore_senior_btn')}",
            key="btn_go_senior",
            use_container_width=True,
        ):
            st.switch_page("pages/6_Senior_Citizen.py")

    # Bottom Quick Actions: Emergency Help & Progress Dashboard
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        if st.button(
            f"🚨 {t('nav_emergency_help')}",
            key="btn_bottom_help",
            use_container_width=True,
        ):
            st.switch_page("pages/7_Emergency_Help.py")
    with b_col2:
        if st.button(
            f"📊 {t('nav_progress_dashboard')}",
            key="btn_bottom_progress",
            use_container_width=True,
        ):
            st.switch_page("pages/8_Progress_Dashboard.py")

    # Cyber Tip of the Day Box
    st.markdown(
        f"""
        <div class="cyber-card" style="margin-top: 25px; background: rgba(0, 240, 255, 0.05); border-color: rgba(0, 240, 255, 0.25);">
            <div style="display: flex; gap: 14px; align-items: center;">
                <span style="font-size: 30px;">💡</span>
                <div>
                    <div style="color: #00f0ff; font-weight: 700; font-size: 14px; text-transform: uppercase;">CyberShield Daily Safety Rule</div>
                    <div style="color: #f8fafc; font-size: 15px; margin-top: 2px;">
                        {'Never type your UPI PIN to RECEIVE funds. PIN entry is solely for money leaving your account. If anyone says entering your PIN will credit money to your bank, it is 100% a fraud.' if lang == 'en' else 'ಹಣ ಪಡೆಯಲು ಎಂದಿಗೂ ಯುಪಿಐ ಪಿನ್ (UPI PIN) ಹಾಕಬೇಡಿ. ಹಣ ಕಳುಹಿಸುವಾಗ ಮಾತ್ರ ಪಿನ್ ಬಳಸಬೇಕು. ಯಾರಾದರೂ ಹಣ ಪಡೆಯಲು ಪಿನ್ ಹಾಕಿ ಎಂದರೆ ಅದು ಖಂಡಿತ ಮೋಸ.'}
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_footer()


if __name__ == "__main__":
    main()
