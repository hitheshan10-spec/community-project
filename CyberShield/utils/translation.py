"""
CyberShield Internationalization & Translation Helper
Provides multilingual support (English and Kannada) across all pages.
"""

import json
import os
import streamlit as st
from typing import Dict, Any

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
TRANS_FILE = os.path.join(DATA_DIR, "translations.json")

_translations: Dict[str, Dict[str, str]] = {}


def load_translations() -> Dict[str, Dict[str, str]]:
    """Loads translations from JSON file with caching."""
    global _translations
    if not _translations:
        try:
            if os.path.exists(TRANS_FILE):
                with open(TRANS_FILE, "r", encoding="utf-8") as f:
                    _translations = json.load(f)
            else:
                _translations = {"en": {}, "kn": {}}
        except Exception as e:
            print(f"Error loading translations: {e}")
            _translations = {"en": {}, "kn": {}}
    return _translations


def get_current_language() -> str:
    """Returns the current language code from Streamlit session state ('en' or 'kn')."""
    if "language" not in st.session_state:
        st.session_state["language"] = "en"
    return st.session_state["language"]


def set_current_language(lang_code: str) -> None:
    """Sets the active language code."""
    if lang_code in ("en", "kn"):
        st.session_state["language"] = lang_code


def t(key: str, default: str = "") -> str:
    """
    Translates a key into the active session language.
    Falls back to English, then to default text, then to key itself.
    """
    trans = load_translations()
    lang = get_current_language()
    
    # Try current language
    if lang in trans and key in trans[lang]:
        return trans[lang][key]
    
    # Fallback to English
    if "en" in trans and key in trans["en"]:
        return trans["en"][key]
    
    return default if default else key


def render_language_selector(sidebar: bool = True) -> str:
    """Renders a modern language selector in the sidebar or main page."""
    current_lang = get_current_language()
    options = {"en": "English 🇬🇧", "kn": "ಕನ್ನಡ (Kannada) 🇮🇳"}
    labels = list(options.values())
    current_idx = 0 if current_lang == "en" else 1

    container = st.sidebar if sidebar else st
    selected_label = container.selectbox(
        t("select_language", "Language / ಭಾಷೆ"),
        options=labels,
        index=current_idx,
        key="global_language_dropdown",
    )

    new_lang = "en" if selected_label == options["en"] else "kn"
    if new_lang != current_lang:
        st.session_state["language"] = new_lang
        st.rerun()

    return new_lang
