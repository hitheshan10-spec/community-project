"""
CyberShield Progress & UI Component Helper
Handles session user management, CSS injection, theme design, and lesson state.
"""

import os
import streamlit as st
from typing import Dict, Any, List
import sys

# Ensure parent directory is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from database.database import (
    get_or_create_user,
    list_users,
    mark_lesson_completed,
    is_lesson_completed,
    get_completed_lessons,
    record_scam_scan,
    get_user_dashboard_stats,
    update_user_preference,
)
from utils.translation import t, get_current_language, render_language_selector


def apply_custom_css():
    """Injects high-end cybersecurity dark glassmorphism styling into the Streamlit app."""
    custom_css = """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

    /* Global Color Palette & Variables */
    :root {
        --bg-deep: #060913;
        --bg-surface: #0b1329;
        --bg-card: rgba(13, 23, 49, 0.7);
        --accent-cyan: #00f0ff;
        --accent-green: #00ff9d;
        --accent-amber: #ffb703;
        --accent-crimson: #ff3366;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --border-glass: rgba(0, 240, 255, 0.15);
        --border-glow: rgba(0, 255, 157, 0.3);
    }

    /* Overall Body & Main Canvas */
    .stApp {
        background-color: var(--bg-deep) !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(0, 240, 255, 0.08) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(0, 255, 157, 0.06) 0px, transparent 50%),
            radial-gradient(at 50% 100%, rgba(13, 23, 49, 0.8) 0px, transparent 60%) !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--text-primary) !important;
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: -0.02em !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #070d1e !important;
        border-right: 1px solid var(--border-glass) !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] {
        padding-top: 1rem;
    }

    /* Glassmorphism Cards */
    .cyber-card {
        background: var(--bg-card);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid var(--border-glass);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }
    .cyber-card:hover {
        border-color: rgba(0, 240, 255, 0.35);
        box-shadow: 0 14px 35px rgba(0, 240, 255, 0.12), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transform: translateY(-2px);
    }

    .cyber-card-accent {
        border-left: 4px solid var(--accent-cyan);
    }
    .cyber-card-warning {
        border-left: 4px solid var(--accent-amber);
    }
    .cyber-card-danger {
        border-left: 4px solid var(--accent-crimson);
    }
    .cyber-card-success {
        border-left: 4px solid var(--accent-green);
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.15) 0%, rgba(0, 255, 157, 0.15) 100%) !important;
        color: #00f0ff !important;
        border: 1px solid rgba(0, 240, 255, 0.4) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        font-size: 15px !important;
        transition: all 0.25s ease-in-out !important;
        box-shadow: 0 4px 15px rgba(0, 240, 255, 0.1) !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #00f0ff 0%, #00ff9d 100%) !important;
        color: #060913 !important;
        border-color: #00ff9d !important;
        box-shadow: 0 6px 22px rgba(0, 255, 157, 0.35) !important;
        transform: translateY(-1px) !important;
    }

    /* Primary CTA Buttons */
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(135deg, #00f0ff 0%, #00ff9d 100%) !important;
        color: #060913 !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 4px 20px rgba(0, 240, 255, 0.3) !important;
    }

    /* Metric Badges & Tiles */
    div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        color: var(--accent-cyan) !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
    }

    /* Input Fields */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background-color: rgba(11, 19, 41, 0.9) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        border-radius: 10px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--accent-cyan) !important;
        box-shadow: 0 0 0 2px rgba(0, 240, 255, 0.25) !important;
    }

    /* Badges Pill */
    .badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-cyan {
        background: rgba(0, 240, 255, 0.12);
        color: #00f0ff;
        border: 1px solid rgba(0, 240, 255, 0.3);
    }
    .badge-green {
        background: rgba(0, 255, 157, 0.12);
        color: #00ff9d;
        border: 1px solid rgba(0, 255, 157, 0.3);
    }
    .badge-amber {
        background: rgba(255, 183, 3, 0.12);
        color: #ffb703;
        border: 1px solid rgba(255, 183, 3, 0.3);
    }
    .badge-red {
        background: rgba(255, 51, 102, 0.12);
        color: #ff3366;
        border: 1px solid rgba(255, 51, 102, 0.3);
    }

    /* Pulse Shield Animation */
    @keyframes shieldGlow {
        0% { filter: drop-shadow(0 0 4px rgba(0, 240, 255, 0.4)); }
        50% { filter: drop-shadow(0 0 16px rgba(0, 255, 157, 0.7)); }
        100% { filter: drop-shadow(0 0 4px rgba(0, 240, 255, 0.4)); }
    }
    .pulse-shield {
        animation: shieldGlow 3s infinite ease-in-out;
    }

    /* Senior Mode Specific Helper Classes */
    .senior-text-lg {
        font-size: 1.35rem !important;
        line-height: 1.8 !important;
    }
    .senior-header-xl {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


def get_active_user() -> Dict[str, Any]:
    """Retrieves or initializes the active user from session state."""
    if "current_user" not in st.session_state or not st.session_state["current_user"]:
        user = get_or_create_user("Default User")
        st.session_state["current_user"] = user
    return st.session_state["current_user"]


def render_sidebar_profile():
    """Renders user profile switcher and language toggle in the sidebar."""
    st.sidebar.markdown(
        """
        <div style="text-align: center; margin-bottom: 15px;">
            <div style="font-size: 32px; filter: drop-shadow(0 0 10px rgba(0,240,255,0.6));">🛡️</div>
            <div style="font-size: 18px; font-weight: 800; color: #00f0ff; letter-spacing: 0.05em;">CYBERSHIELD</div>
            <div style="font-size: 11px; color: #00ff9d; text-transform: uppercase; font-weight: 600;">Learn • Identify • Protect</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Language selection
    render_language_selector(sidebar=True)

    # Active User Profile selector
    users = list_users()
    user_names = [u["username"] for u in users]
    if "Default User" not in user_names:
        user_names.insert(0, "Default User")

    current_user = get_active_user()
    current_idx = (
        user_names.index(current_user["username"])
        if current_user["username"] in user_names
        else 0
    )

    selected_username = st.sidebar.selectbox(
        f"👤 {t('switch_user', 'Active User')}",
        options=user_names,
        index=current_idx,
        key="global_user_switcher",
    )

    if selected_username != current_user["username"]:
        new_u = get_or_create_user(selected_username)
        st.session_state["current_user"] = new_u
        st.rerun()

    # Quick badge count in sidebar
    stats = get_user_dashboard_stats(current_user["id"])
    st.sidebar.markdown(
        f"""
        <div style="background: rgba(11, 19, 41, 0.7); border: 1px solid rgba(0, 240, 255, 0.2); border-radius: 10px; padding: 12px; margin-top: 10px; text-align: center;">
            <div style="font-size: 11px; color: #94a3b8;">DEFENSE RANK</div>
            <div style="font-size: 15px; font-weight: 700; color: #00ff9d;">{stats['rank_icon']} {stats['rank_tier']}</div>
            <div style="font-size: 11px; color: #64748b; margin-top: 4px;">Completed Lessons: <b>{stats['total_lessons']}</b> | Badges: <b>{stats['badges_count']}</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Quick Emergency Dial pill
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style="background: rgba(255, 51, 102, 0.12); border: 1px solid rgba(255, 51, 102, 0.35); border-radius: 10px; padding: 10px; text-align: center;">
            <div style="font-size: 11px; color: #ff85a2; font-weight: 600;">CYBERCRIME HELPLINE</div>
            <div style="font-size: 20px; font-weight: 800; color: #ff3366; letter-spacing: 0.05em;">📞 1930</div>
            <div style="font-size: 10px; color: #cbd5e1; margin-top: 2px;">Toll-Free Immediate Assistance</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(title: str, subtitle: str, badge_text: str = "OFFICIAL GUIDE"):
    """Renders a standard sleek cybersecurity banner at the top of pages."""
    apply_custom_css()
    render_sidebar_profile()

    st.markdown(
        f"""
        <div class="cyber-card cyber-card-accent" style="margin-bottom: 25px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
                <div>
                    <span class="badge-pill badge-cyan">{badge_text}</span>
                    <h1 style="margin: 8px 0 4px 0; font-size: 2rem; background: linear-gradient(90deg, #ffffff, #00f0ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{title}</h1>
                    <p style="color: #94a3b8; font-size: 15px; margin: 0;">{subtitle}</p>
                </div>
                <div style="text-align: right;">
                    <span class="badge-pill badge-green">🛡️ Active Protection</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    """Renders the standard privacy notice and footer."""
    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align: center; padding: 20px 0; color: #64748b; font-size: 13px;">
            <p style="margin-bottom: 6px;">🛡️ <b>CYBERSHIELD</b> — Your Digital Safety Companion • National Cyber Helpline: <b>1930</b></p>
            <p style="font-size: 12px; color: #475569; max-width: 800px; margin: 0 auto;">{t('privacy_notice')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
