"""
CyberShield User Progress & Achievement Dashboard
Tracks completed modules, quiz mastery, scam scans, badges, and generates completion certificates.
"""

import os
import sys
import pandas as pd
from datetime import datetime
import streamlit as st

st.set_page_config(
    page_title="Progress Dashboard - CyberShield",
    page_icon="📊",
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
    get_user_dashboard_stats,
    get_completed_lessons,
    get_quiz_attempts,
    get_scam_scans,
    get_user_badges,
    get_or_create_user,
    list_users,
)


ALL_AVAILABLE_BADGES = [
    {
        "key": "first_shield",
        "icon": "🛡️",
        "title": "First Shield",
        "requirement": "Complete your first lesson in Scam Awareness or Digital Safety.",
    },
    {
        "key": "scam_spotter",
        "icon": "🔍",
        "title": "Scam Spotter",
        "requirement": "Analyze any message in the Online Scam Checker.",
    },
    {
        "key": "quiz_novice",
        "icon": "🎯",
        "title": "Quiz Explorer",
        "requirement": "Complete your first cybersecurity quiz.",
    },
    {
        "key": "cyber_sentinel",
        "icon": "⚡",
        "title": "Cyber Sentinel",
        "requirement": "Score 80% or higher on any quiz level.",
    },
    {
        "key": "scholar_shield",
        "icon": "🎓",
        "title": "Scholar Shield",
        "requirement": "Complete at least 2 Student Learning Zone lessons.",
    },
    {
        "key": "elder_guardian",
        "icon": "👵",
        "title": "Elder Guardian",
        "requirement": "Complete at least 2 Senior Citizen Safe Mode modules.",
    },
    {
        "key": "master_defender",
        "icon": "👑",
        "title": "Cyber Master Defender",
        "requirement": "Complete 8+ lessons and pass 2+ cybersecurity quizzes.",
    },
]


def render_certificate(user_name: str, rank: str, lessons_count: int, lang: str):
    """Generates a responsive printable CyberShield Certificate card."""
    today = datetime.now().strftime("%B %d, %Y")
    cert_html = f"""
    <div style="background: linear-gradient(135deg, #070d1e 0%, #0d1b3e 100%); border: 3px solid #00f0ff; border-radius: 20px; padding: 40px 30px; text-align: center; box-shadow: 0 0 35px rgba(0,240,255,0.25); max-width: 850px; margin: 20px auto; position: relative;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid rgba(0,240,255,0.3); padding-bottom: 15px; margin-bottom: 25px;">
            <div style="font-size: 28px;">🛡️</div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 20px; font-weight: 800; color: #00f0ff; letter-spacing: 0.15em;">CYBERSHIELD DEFENSE ACADEMY</div>
            <div style="font-size: 28px;">🇮🇳</div>
        </div>
        
        <div style="font-size: 14px; text-transform: uppercase; letter-spacing: 0.2em; color: #00ff9d; font-weight: 700; margin-bottom: 10px;">
            CERTIFICATE OF CYBER DEFENSE AWARENESS
        </div>
        
        <div style="font-size: 15px; color: #94a3b8; margin-bottom: 15px;">
            This document certifies that
        </div>
        
        <div style="font-size: 34px; font-weight: 800; color: #ffffff; text-decoration: underline; text-decoration-color: #00f0ff; margin-bottom: 15px; font-family: 'Plus Jakarta Sans', sans-serif;">
            {user_name}
        </div>
        
        <p style="color: #cbd5e1; font-size: 16px; max-width: 650px; margin: 0 auto 25px auto; line-height: 1.6;">
            Has demonstrated proficiency in identifying cyber fraud vectors, safeguarding personal authentication credentials, and upholding national digital security standards with the distinction of <b>{rank}</b> ({lessons_count} modules completed).
        </p>
        
        <div style="display: flex; justify-content: space-around; align-items: flex-end; border-top: 1px solid rgba(255,255,255,0.15); padding-top: 20px; margin-top: 25px;">
            <div style="text-align: center;">
                <div style="font-size: 14px; color: #00f0ff; font-weight: 700;">{today}</div>
                <div style="font-size: 11px; color: #64748b; text-transform: uppercase;">Date of Verification</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 26px;">🛡️ ⭐ 🛡️</div>
                <div style="font-size: 11px; color: #00ff9d; text-transform: uppercase; font-weight: 700;">Verified Security Seal</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 14px; color: #00f0ff; font-family: 'JetBrains Mono';">CS-IN-2026-OK</div>
                <div style="font-size: 11px; color: #64748b; text-transform: uppercase;">Credential ID</div>
            </div>
        </div>
    </div>
    """
    st.markdown(cert_html, unsafe_allow_html=True)


def main():
    lang = get_current_language()
    title = t("progress_title")
    subtitle = t("progress_subtitle")
    render_page_header(title, subtitle, badge_text="SQLITE PERSISTENCE")

    user = get_active_user()

    # User Switcher & New Profile Creator
    col_u1, col_u2 = st.columns([2, 1])
    with col_u1:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 24px;">👤</span>
                <div>
                    <div style="font-size: 14px; color: #94a3b8;">ACTIVE PROFILE</div>
                    <div style="font-size: 18px; font-weight: 800; color: #00f0ff;">{user['username']} ({user['role'].title()})</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_u2:
        with st.expander("➕ " + ("Create New User Profile" if lang == "en" else "ಹೊಸ ಪ್ರೊಫೈಲ್ ರಚಿಸಿ")):
            new_name = st.text_input("Name:", key="new_user_name_input")
            role_choice = st.selectbox("Role:", ["student", "senior", "general"], key="new_user_role_select")
            if st.button("Save Profile", key="btn_save_new_user"):
                if new_name.strip():
                    created = get_or_create_user(new_name.strip(), role=role_choice, preferred_language=lang)
                    st.session_state["current_user"] = created
                    st.success(f"Profile '{created['username']}' activated!")
                    st.rerun()

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    stats = get_user_dashboard_stats(user["id"])

    # Rank Badge Header Card
    st.markdown(
        f"""
        <div class="cyber-card cyber-card-accent" style="padding: 24px; margin-bottom: 25px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px;">
                <div style="display: flex; gap: 18px; align-items: center;">
                    <div style="font-size: 52px; filter: drop-shadow(0 0 12px rgba(0,255,157,0.5));">{stats['rank_icon']}</div>
                    <div>
                        <span class="badge-pill badge-green">{t('rank_title')}</span>
                        <h2 style="margin: 6px 0 2px 0; color: #ffffff; font-size: 28px;">{stats['rank_tier']}</h2>
                        <div style="color: #94a3b8; font-size: 14px;">User: <b>{user['username']}</b> • Enrolled in CyberShield Digital Defense</div>
                    </div>
                </div>
                <div style="display: flex; gap: 15px; text-align: center;">
                    <div style="background: rgba(11,19,41,0.8); border: 1px solid rgba(0,240,255,0.25); border-radius: 12px; padding: 12px 18px;">
                        <div style="font-size: 26px; font-weight: 800; color: #00f0ff; font-family: 'JetBrains Mono';">{stats['total_lessons']}</div>
                        <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase;">Lessons</div>
                    </div>
                    <div style="background: rgba(11,19,41,0.8); border: 1px solid rgba(0,255,157,0.25); border-radius: 12px; padding: 12px 18px;">
                        <div style="font-size: 26px; font-weight: 800; color: #00ff9d; font-family: 'JetBrains Mono';">{stats['quiz_high_score']}%</div>
                        <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase;">Best Quiz</div>
                    </div>
                    <div style="background: rgba(11,19,41,0.8); border: 1px solid rgba(255,183,3,0.25); border-radius: 12px; padding: 12px 18px;">
                        <div style="font-size: 26px; font-weight: 800; color: #ffb703; font-family: 'JetBrains Mono';">{stats['badges_count']}</div>
                        <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase;">Badges</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(t("completed_lessons_count"), f"{stats['total_lessons']} / 25")
    m2.metric("Quiz Attempts", f"{stats['quiz_attempts']}")
    m3.metric("Scam Scans Run", f"{stats['scams_scanned']}")
    m4.metric(t("badges_earned"), f"{stats['badges_count']} / {len(ALL_AVAILABLE_BADGES)}")

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Category Progress Breakdown
    st.markdown(f"### 📈 {'Curriculum Progress by Category' if lang == 'en' else 'ವರ್ಗವಾರು ಕಲಿಕಾ ಪ್ರಗತಿ'}")
    c_break = stats["category_breakdown"]

    cat_map = [
        {"key": "scam_awareness", "name": "Scam Awareness Centre", "total": 12, "color": "#00f0ff"},
        {"key": "digital_safety", "name": "Digital Safety Guide", "total": 9, "color": "#00ff9d"},
        {"key": "student_zone", "name": "Student Learning Zone", "total": 4, "color": "#ffb703"},
        {"key": "senior_citizen", "name": "Senior Citizen Safe Mode", "total": 4, "color": "#a855f7"},
    ]

    p_cols = st.columns(4)
    for i, cm in enumerate(cat_map):
        done = c_break.get(cm["key"], 0)
        pct = min(int((done / cm["total"]) * 100), 100)
        with p_cols[i]:
            st.markdown(
                f"""
                <div class="cyber-card" style="padding: 16px; text-align: center;">
                    <div style="font-size: 14px; font-weight: 700; color: #ffffff; margin-bottom: 6px;">{cm['name']}</div>
                    <div style="font-size: 22px; font-weight: 800; color: {cm['color']}; font-family: 'JetBrains Mono';">{done} / {cm['total']}</div>
                    <div style="background: rgba(255,255,255,0.06); border-radius: 6px; height: 6px; width: 100%; margin: 8px 0; overflow: hidden;">
                        <div style="background: {cm['color']}; height: 6px; width: {pct}%;"></div>
                    </div>
                    <div style="font-size: 11px; color: #94a3b8;">{pct}% Completed</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # Achievement Badges Showcase
    st.markdown(f"### 🎖️ {'Achievement Badges' if lang == 'en' else 'ಗಳಿಸಿದ ಸಾಧನಾ ಬ್ಯಾಡ್ಜ್‌ಗಳು'}")
    user_badges_raw = get_user_badges(user["id"])
    earned_keys = {b["badge_key"]: b for b in user_badges_raw}

    badge_cols = st.columns(4)
    for b_idx, badge in enumerate(ALL_AVAILABLE_BADGES):
        col_target = badge_cols[b_idx % 4]
        is_earned = badge["key"] in earned_keys
        with col_target:
            if is_earned:
                earned_info = earned_keys[badge["key"]]
                st.markdown(
                    f"""
                    <div class="cyber-card cyber-card-success" style="padding: 16px; text-align: center; height: 100%; box-shadow: 0 0 15px rgba(0,255,157,0.2);">
                        <div style="font-size: 36px; margin-bottom: 6px;">{badge['icon']}</div>
                        <div style="font-weight: 800; color: #00ff9d; font-size: 14px;">{badge['title']}</div>
                        <span class="badge-pill badge-green" style="font-size: 10px; margin: 4px 0;">UNLOCKED</span>
                        <div style="font-size: 11px; color: #cbd5e1; margin-top: 6px;">{badge['requirement']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class="cyber-card" style="padding: 16px; text-align: center; height: 100%; opacity: 0.45; border-color: rgba(255,255,255,0.1);">
                        <div style="font-size: 36px; margin-bottom: 6px; filter: grayscale(100%);">🔒</div>
                        <div style="font-weight: 700; color: #94a3b8; font-size: 14px;">{badge['title']}</div>
                        <span class="badge-pill badge-red" style="font-size: 10px; margin: 4px 0;">LOCKED</span>
                        <div style="font-size: 11px; color: #64748b; margin-top: 6px;">{badge['requirement']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

    # Quiz Attempts Log & Scam Scans Log Tabs
    tab_quiz, tab_scams, tab_cert = st.tabs([
        "🎯 " + ("Quiz History" if lang == "en" else "ರಸಪ್ರಶ್ನೆ ಇತಿಹಾಸ"),
        "🔍 " + ("Scam Scan Logs" if lang == "en" else "ಪರೀಕ್ಷಿಸಿದ ಸಂದೇಶಗಳು"),
        "📜 " + ("Certificate of Completion" if lang == "en" else "ಪ್ರಮಾಣಪತ್ರ"),
    ])

    with tab_quiz:
        attempts = get_quiz_attempts(user["id"])
        if attempts:
            df_q = pd.DataFrame(attempts)
            df_display = df_q[["difficulty", "score", "total_questions", "percentage", "passed", "attempted_at"]].copy()
            df_display.columns = ["Difficulty", "Score", "Total Q", "Percentage (%)", "Passed", "Date & Time"]
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        else:
            st.info("No quiz attempts recorded yet. Head over to the Quiz Centre to take your first test!")

    with tab_scams:
        scans = get_scam_scans(user["id"], limit=10)
        if scans:
            df_s = pd.DataFrame(scans)
            df_s_display = df_s[["sample_title", "risk_level", "risk_score", "detected_triggers", "scanned_at"]].copy()
            df_s_display.columns = ["Message Snippet", "Risk Level", "Threat Score", "Triggers", "Timestamp"]
            st.dataframe(df_s_display, use_container_width=True, hide_index=True)
        else:
            st.info("No scam scans recorded yet. Use the Online Scam Checker to inspect suspicious messages.")

    with tab_cert:
        st.markdown(
            f"""
            <p style="color: #cbd5e1; font-size: 15px;">
                {'Download or display your verified CyberShield completion certificate once you have completed at least 1 lesson.' if lang == 'en' else 'ಕನಿಷ್ಠ 1 ಪಾಠ ಪೂರ್ಣಗೊಳಿಸಿದ ನಂತರ ನಿಮ್ಮ ಪರಿಶೀಲಿಸಿದ ಸೈಬರ್ ಶೀಲ್ಡ್ ಪ್ರಮಾಣಪತ್ರವನ್ನು ವೀಕ್ಷಿಸಿ.'}
            </p>
            """,
            unsafe_allow_html=True,
        )
        if stats["total_lessons"] >= 1:
            render_certificate(user["username"], stats["rank_tier"], stats["total_lessons"], lang)
        else:
            st.warning("Complete at least 1 lesson in Scam Awareness or Digital Safety to unlock your Official Certificate.")

    render_footer()


if __name__ == "__main__":
    main()
