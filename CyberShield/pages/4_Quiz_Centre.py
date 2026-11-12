"""
CyberShield Interactive Quiz Centre
Test your cybersecurity awareness with multiple-choice questions across 3 difficulty tiers.
"""

import json
import os
import sys
import random
import streamlit as st

st.set_page_config(
    page_title="Quiz Centre - CyberShield",
    page_icon="🎯",
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
from database.database import record_quiz_attempt, get_user_badges

QUIZ_PATH = os.path.join(BASE_DIR, "data", "quiz.json")


def load_quiz_questions():
    if os.path.exists(QUIZ_PATH):
        with open(QUIZ_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def init_quiz_state(difficulty: str, num_questions: int = 5):
    all_q = load_quiz_questions()
    if difficulty != "all":
        filtered = [q for q in all_q if q["difficulty"] == difficulty]
    else:
        filtered = all_q

    # Shuffle and select questions
    random.seed(None)
    selected = random.sample(filtered, min(num_questions, len(filtered)))

    st.session_state["quiz_active"] = True
    st.session_state["quiz_questions"] = selected
    st.session_state["quiz_difficulty"] = difficulty
    st.session_state["quiz_current_index"] = 0
    st.session_state["quiz_score"] = 0
    st.session_state["quiz_answered"] = False
    st.session_state["quiz_selected_option"] = None
    st.session_state["quiz_completed"] = False


def main():
    lang = get_current_language()
    title = t("quiz_title")
    subtitle = t("quiz_subtitle")
    render_page_header(title, subtitle, badge_text="30+ QUESTIONS")

    user = get_active_user()

    # If quiz is not running, show level selector & instructions
    if "quiz_active" not in st.session_state or not st.session_state["quiz_active"]:
        st.markdown(
            f"""
            <div class="cyber-card cyber-card-accent">
                <h3 style="color: #00f0ff; margin-top: 0;">🎯 {'Select Challenge Level' if lang == 'en' else 'ಸವಾಲಿನ ಹಂತವನ್ನು ಆಯ್ಕೆಮಾಡಿ'}</h3>
                <p style="color: #cbd5e1; font-size: 15px;">
                    {'Test your instincts against real-world attack simulations. Pass with 60% or more to earn badges on your Progress Dashboard!' if lang == 'en' else 'ನೈಜ ಜಗತ್ತಿನ ಸೈಬರ್ ಸವಾಲುಗಳನ್ನು ಎದುರಿಸಿ 60% ಕ್ಕಿಂತ ಹೆಚ್ಚು ಅಂಕಗಳಿಸಿ ಸೈಬರ್ ಶೀಲ್ಡ್ ಬ್ಯಾಡ್ಜ್‌ಗಳನ್ನು ಪಡೆಯಿರಿ.'}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        q1_col, q2_col, q3_col = st.columns(3)
        with q1_col:
            st.markdown(
                f"""
                <div class="cyber-card cyber-card-success" style="text-align: center; height: 100%;">
                    <div style="font-size: 32px;">🔰</div>
                    <h4 style="color: #00ff9d;">{t('difficulty_easy')}</h4>
                    <p style="color: #94a3b8; font-size: 13px;">Everyday safety: UPI basics, password strength, ATM hygiene, public Wi-Fi rules.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("🚀 " + ("Start Easy Quiz" if lang == "en" else "ಸುಲಭ ಹಂತ ಪ್ರಾರಂಭಿಸಿ"), key="btn_start_easy", use_container_width=True):
                init_quiz_state("easy", 5)
                st.rerun()

        with q2_col:
            st.markdown(
                f"""
                <div class="cyber-card cyber-card-warning" style="text-align: center; height: 100%;">
                    <div style="font-size: 32px;">⚡</div>
                    <h4 style="color: #ffb703;">{t('difficulty_medium')}</h4>
                    <p style="color: #94a3b8; font-size: 13px;">Social engineering, UPI collect traps, credential stuffing, Masked Aadhaar.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("🚀 " + ("Start Medium Quiz" if lang == "en" else "ಮಧ್ಯಮ ಹಂತ ಪ್ರಾರಂಭಿಸಿ"), key="btn_start_med", use_container_width=True):
                init_quiz_state("medium", 5)
                st.rerun()

        with q3_col:
            st.markdown(
                f"""
                <div class="cyber-card cyber-card-danger" style="text-align: center; height: 100%;">
                    <div style="font-size: 32px;">🛡️</div>
                    <h4 style="color: #ff3366;">{t('difficulty_hard')}</h4>
                    <p style="color: #94a3b8; font-size: 13px;">Advanced exploits: SIM swap mechanics, Evil Twin Wi-Fi, AI deepfakes, RBI zero-liability rules.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("🚀 " + ("Start Hard Quiz" if lang == "en" else "ಕಠಿಣ ಹಂತ ಪ್ರಾರಂಭಿಸಿ"), key="btn_start_hard", use_container_width=True):
                init_quiz_state("hard", 5)
                st.rerun()

        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        if st.button("🌟 " + ("Take Full Master Challenge (10 Random Questions Across All Levels)" if lang == "en" else "ಮಾಸ್ಟರ್ ಚಾಲೆಂಜ್ (ಎಲ್ಲಾ ಹಂತಗಳ 10 ಪ್ರಶ್ನೆಗಳು)"), key="btn_start_all", use_container_width=True):
            init_quiz_state("all", 10)
            st.rerun()

        render_footer()
        return

    # If Quiz is Completed
    if st.session_state.get("quiz_completed", False):
        score = st.session_state["quiz_score"]
        total = len(st.session_state["quiz_questions"])
        pct = round((score / total) * 100, 1)
        passed = pct >= 60.0

        res_color = "#00ff9d" if passed else "#ff3366"
        eval_text = (
            "🏆 Outstanding! You possess strong cyber defensive instincts!"
            if pct >= 80
            else ("✅ Good effort! You cleared the passing threshold." if passed else "❌ Keep practicing! Review the Scam and Safety guides to sharpen your defenses.")
        )

        st.markdown(
            f"""
            <div class="cyber-card" style="text-align: center; border-color: {res_color}; padding: 35px 20px;">
                <div style="font-size: 60px;">{'🏆' if passed else '📚'}</div>
                <h1 style="color: {res_color}; margin: 8px 0;">{t('quiz_completed_title')}</h1>
                <div style="font-size: 48px; font-weight: 800; color: #ffffff; font-family: 'JetBrains Mono';">
                    {score} / {total}
                </div>
                <div style="font-size: 20px; font-weight: 700; color: {res_color}; margin: 10px 0;">
                    {pct}% — {'PASSED' if passed else 'NEEDS IMPROVEMENT'}
                </div>
                <p style="color: #cbd5e1; font-size: 16px; max-width: 600px; margin: 15px auto;">
                    {eval_text}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Show badges
        user_badges = get_user_badges(user["id"])
        if user_badges:
            st.markdown(f"#### 🎖️ {'Your Achievement Badges' if lang == 'en' else 'ನಿಮ್ಮ ಬ್ಯಾಡ್ಜ್‌ಗಳು'}")
            b_cols = st.columns(min(len(user_badges), 4))
            for b_idx, b in enumerate(user_badges[:4]):
                with b_cols[b_idx]:
                    st.markdown(
                        f"""
                        <div style="background: rgba(11,19,41,0.8); border: 1px solid rgba(0,255,157,0.3); border-radius: 10px; padding: 12px; text-align: center;">
                            <div style="font-size: 24px;">🛡️</div>
                            <div style="font-weight: 700; color: #00ff9d; font-size: 13px;">{b['badge_title']}</div>
                            <div style="font-size: 11px; color: #94a3b8;">{b['description']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            if st.button(f"🔄 {t('restart_quiz')}", key="btn_restart_quiz", use_container_width=True):
                st.session_state["quiz_active"] = False
                st.session_state["quiz_completed"] = False
                st.rerun()
        with col_c2:
            if st.button("📊 " + ("View Progress Dashboard" if lang == "en" else "ಪ್ರಗತಿ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ ವೀಕ್ಷಿಸಿ"), key="btn_go_dash", use_container_width=True):
                st.switch_page("pages/8_Progress_Dashboard.py")

        render_footer()
        return

    # Running Active Quiz
    questions = st.session_state["quiz_questions"]
    curr_idx = st.session_state["quiz_current_index"]
    total_q = len(questions)
    curr_q = questions[curr_idx]

    # Progress & Score Header
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <span class="badge-pill badge-cyan">QUESTION {curr_idx + 1} OF {total_q}</span>
            <span style="font-family: 'JetBrains Mono'; font-weight: 700; color: #00ff9d; font-size: 16px;">
                {t('quiz_score')}: {st.session_state['quiz_score']}
            </span>
        </div>
        <div style="background: rgba(255,255,255,0.06); border-radius: 6px; height: 6px; width: 100%; overflow: hidden; margin-bottom: 25px;">
            <div style="background: #00f0ff; height: 6px; width: {((curr_idx + 1) / total_q) * 100}%;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    q_text = curr_q["question_en"] if lang == "en" else curr_q["question_kn"]
    opts = curr_q["options_en"] if lang == "en" else curr_q["options_kn"]
    correct_idx = curr_q["correct_index"]
    explanation = curr_q["explanation_en"] if lang == "en" else curr_q["explanation_kn"]

    # Question Box
    st.markdown(
        f"""
        <div class="cyber-card" style="padding: 24px; margin-bottom: 20px;">
            <h3 style="color: #ffffff; margin-top: 0; line-height: 1.5; font-size: 1.25rem;">
                {q_text}
            </h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # If question has not been submitted yet
    if not st.session_state["quiz_answered"]:
        selected_option = st.radio(
            "Select your answer:" if lang == "en" else "ನಿಮ್ಮ ಉತ್ತರವನ್ನು ಆಯ್ಕೆಮಾಡಿ:",
            options=list(range(len(opts))),
            format_func=lambda i: f" {opts[i]}",
            key=f"q_radio_{curr_idx}",
        )

        if st.button(f"🎯 {t('submit_answer')}", type="primary", key=f"btn_sub_{curr_idx}"):
            st.session_state["quiz_answered"] = True
            st.session_state["quiz_selected_option"] = selected_option
            if selected_option == correct_idx:
                st.session_state["quiz_score"] += 1
            st.rerun()

    else:
        # Question was answered - show feedback
        user_choice = st.session_state["quiz_selected_option"]
        is_correct = user_choice == correct_idx

        feedback_banner = (
            f"""
            <div class="cyber-card cyber-card-success" style="padding: 18px; margin-bottom: 20px;">
                <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 6px;">
                    <span style="font-size: 24px;">✅</span>
                    <h4 style="color: #00ff9d; margin: 0;">{'CORRECT ANSWER!' if lang == 'en' else 'ಸರಿಯಾದ ಉತ್ತರ!'}</h4>
                </div>
                <div style="color: #e2e8f0; font-size: 14px; line-height: 1.6;">
                    <b>{t('explanation')}:</b> {explanation}
                </div>
            </div>
            """
            if is_correct
            else f"""
            <div class="cyber-card cyber-card-danger" style="padding: 18px; margin-bottom: 20px;">
                <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 6px;">
                    <span style="font-size: 24px;">❌</span>
                    <h4 style="color: #ff3366; margin: 0;">{'INCORRECT ANSWER' if lang == 'en' else 'ತಪ್ಪು ಉತ್ತರ'}</h4>
                </div>
                <p style="color: #fca5a5; font-size: 14px; margin: 4px 0 8px 0;">
                    <b>{'Correct Answer:' if lang == 'en' else 'ಸರಿಯಾದ ಉತ್ತರ:'}</b> {opts[correct_idx]}
                </p>
                <div style="color: #e2e8f0; font-size: 14px; line-height: 1.6;">
                    <b>{t('explanation')}:</b> {explanation}
                </div>
            </div>
            """
        )
        st.markdown(feedback_banner, unsafe_allow_html=True)

        # Next question button
        if curr_idx + 1 < total_q:
            if st.button(f"➡️ {t('next_question')}", type="primary", key="btn_next_q"):
                st.session_state["quiz_current_index"] += 1
                st.session_state["quiz_answered"] = False
                st.session_state["quiz_selected_option"] = None
                st.rerun()
        else:
            if st.button("🏁 " + ("Complete Quiz & View Score" if lang == "en" else "ರಸಪ್ರಶ್ನೆ ಪೂರ್ಣಗೊಳಿಸಿ"), type="primary", key="btn_finish_quiz"):
                # Record in database
                record_quiz_attempt(
                    user["id"],
                    st.session_state["quiz_difficulty"],
                    st.session_state["quiz_score"],
                    total_q,
                )
                st.session_state["quiz_completed"] = True
                st.rerun()

    render_footer()


if __name__ == "__main__":
    main()
