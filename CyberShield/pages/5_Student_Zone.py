"""
CyberShield Student & Youth Learning Zone
Specially tailored digital defense curriculum for school, college students, and gamers.
"""

import os
import sys
import streamlit as st

st.set_page_config(
    page_title="Student Zone - CyberShield",
    page_icon="🎓",
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


STUDENT_TOPICS = [
    {
        "id": "gaming_protection",
        "icon": "🎮",
        "title_en": "Gaming Account & Asset Protection",
        "title_kn": "ಗೇಮಿಂಗ್ ಖಾತೆ ಮತ್ತು ಆಸ್ತಿಗಳ ರಕ್ಷಣೆ",
        "summary_en": "Defend against BGMI, Steam, Roblox, and Free Fire credential theft, fake skin giveaways, and cheat engine malware.",
        "summary_kn": "BGMI, Steam, ಮತ್ತು Roblox ಖಾತೆಗಳ ರಕ್ಷಣೆ, ಉಚಿತ ಸ್ಕಿನ್‌ಗಳ ಆಮಿಷ ಮತ್ತು ನಕಲಿ ಚೀಟ್ ಕೋಡ್‌ಗಳಿಂದ ರಕ್ಷಣೆ.",
        "content_en": """
        **The Gaming Threat Landscape:**
        - **Fake Diamond / UC Generators:** Websites claiming to generate free BGMI Unknown Cash or Roblox Robux are phishing traps created to harvest your Gmail, Facebook, or Twitter credentials.
        - **Malicious Cheat Engines & Aimbots:** Free hacks and cheat tools on YouTube or Discord frequently conceal Trojan spyware, keyloggers, and crypto miners that steal passwords stored in your Chrome browser.
        - **Account Trading Scams:** Scammers convince students to trade high-tier accounts or skins, promise payment via UPI, and vanish once login credentials are transferred.
        """,
        "content_kn": """
        **ಗೇಮಿಂಗ್ ಜಗತ್ತಿನ ಸೈಬರ್ ಅಪಾಯಗಳು:**
        - **ಉಚಿತ UC / ಡೈಮಂಡ್ ಆಮಿಷ:** ಉಚಿತ ಗೇಮಿಂಗ್ ಕರೆನ್ಸಿ ನೀಡುವುದಾಗಿ ಹೇಳುವ ವೆಬ್‌ಸೈಟ್‌ಗಳು ನಿಮ್ಮ ಜಿಮೇಲ್ ಮತ್ತು ಫೇಸ್‌ಬುಕ್ ಪಾಸ್‌ವರ್ಡ್ ಕದಿಯುವ ಫಿಶಿಂಗ್ ಬಲೆಗಳು.
        - **ಮಾಲ್ವೇರ್ ಚೀಟ್ ಕೋಡ್‌ಗಳು:** ಡಿಸ್ಕಾರ್ಡ್ ಅಥವಾ ಯೂಟ್ಯೂಬ್‌ನಲ್ಲಿ ಸಿಗುವ ಉಚಿತ ಹ್ಯಾಕಿಂಗ್ ಟೂಲ್‌ಗಳಲ್ಲಿ ಕೀಲಾಗರ್‌ಗಳು ಅಡಗಿರುತ್ತವೆ.
        - **ಖಾತೆ ಮಾರಾಟದ ವಂಚನೆ:** ಗೇಮಿಂಗ್ ಐಡಿ ನೀಡಿದರೆ ಹಣ ಕಳುಹಿಸುತ್ತೇವೆ ಎಂದು ನಂಬಿಸಿ ಖಾತೆ ಕದ್ದು ಬ್ಲಾಕ್ ಮಾಡುತ್ತಾರೆ.
        """,
        "tips_en": [
            "Enable Two-Factor Authentication (Steam Guard, Google Authenticator) on all gaming portals.",
            "Never download modified game APKs or unauthorized third-party aimbot scripts.",
            "Never trade accounts outside officially sanctioned platform marketplaces."
        ],
        "tips_kn": [
            "ಎಲ್ಲಾ ಗೇಮಿಂಗ್ ಖಾತೆಗಳಿಗೆ 2FA (Steam Guard / Authenticator) ಆನ್ ಮಾಡಿ.",
            "ಅನಧಿಕೃತ ಗೇಮಿಂಗ್ ಹ್ಯಾಕ್ಸ್ ಅಥವಾ APK ಗಳನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡಬೇಡಿ.",
            "ಅಪರಿಚಿತರೊಂದಿಗೆ ಖಾತೆ ಅಥವಾ ಪಾಸ್‌ವರ್ಡ್ ವಿನಿಮಯ ಮಾಡಿಕೊಳ್ಳಬೇಡಿ."
        ]
    },
    {
        "id": "cyberbullying_harassment",
        "icon": "🛡️",
        "title_en": "Cyberbullying & Online Harassment Defense",
        "title_kn": "ಸೈಬರ್‌ಬುಲ್ಲಿಯಿಂಗ್ ಮತ್ತು ಆನ್‌ಲೈನ್ ಕಿರುಕುಳ ತಡೆ",
        "summary_en": "Protocols for dealing with online harassment, abusive group chats, revenge threats, and toxic gaming spaces.",
        "summary_kn": "ಆನ್‌ಲೈನ್ ನಿಂದನೆ, ವಾಟ್ಸಾಪ್ ಗ್ರೂಪ್‌ಗಳಲ್ಲಿ ಬೆದರಿಕೆ ಮತ್ತು ಮಾನಸಿಕ ಕಿರುಕುಳವನ್ನು ಎದುರಿಸುವ ಕ್ರಮಗಳು.",
        "content_en": """
        **Recognizing and Overcoming Cyberbullying:**
        - **Do Not Retaliate:** Engaging in angry arguments feeds the bully and can lead to counter-complaints. Stay calm and disconnect immediately.
        - **Preserve Digital Evidence:** Take uncropped screenshots of text chats, comments, sender usernames, and timestamps. Do not delete the conversation until documented.
        - **Block and Report:** Use the in-app reporting system on Instagram, WhatsApp, Discord, or Snapchat.
        - **Confide in a Trusted Adult:** Reach out to parents, college counselors, or teachers. You do not have to fight digital abuse alone.
        """,
        "content_kn": """
        **ಸೈಬರ್‌ಬುಲ್ಲಿಯಿಂಗ್ ಎದುರಿಸುವ ವಿಧಾನ:**
        - **ಪ್ರತ್ಯುತ್ತರ ನೀಡಬೇಡಿ:** ಕೋಪದಿಂದ ಜಗಳವಾಡಿದರೆ ಸಮಸ್ಯೆ ಉಲ್ಬಣಗೊಳ್ಳುತ್ತದೆ. ತಕ್ಷಣ ಆ ಸಂಭಾಷಣೆಯಿಂದ ಹೊರಬನ್ನಿ.
        - **ಸಾಕ್ಷ್ಯಗಳನ್ನು ಉಳಿಸಿಕೊಳ್ಳಿ:** ಕಿರುಕುಳ ನೀಡಿದ ಸಂದೇಶಗಳು, ಐಡಿ ಮತ್ತು ಸಮಯವನ್ನು ಸ್ಪಷ್ಟವಾಗಿ ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ತೆಗೆದಿಟ್ಟುಕೊಳ್ಳಿ.
        - **ಬ್ಲಾಕ್ ಮತ್ತು ರಿಪೋರ್ಟ್ ಮಾಡಿ:** ಆ್ಯಪ್‌ನಲ್ಲಿರುವ 'Report' ಆಯ್ಕೆ ಬಳಸಿ.
        - **ಪೋಷಕರು ಅಥವಾ ಶಿಕ್ಷಕರಿಗೆ ತಿಳಿಸಿ:** ಯಾವುದೇ ಕಿರುಕುಳವನ್ನು ಮುಚ್ಚಿಡದೆ ವಿಶ್ವಾಸಾರ್ಹ ಹಿರಿಯರಿಗೆ ತಿಳಿಸಿ.
        """,
        "tips_en": [
            "National Child Helpline: 1098 | National Cybercrime Helpline: 1930.",
            "Never engage with burner or anonymous troll accounts.",
            "Filter toxic comments automatically using Instagram/YouTube comment moderation tools."
        ],
        "tips_kn": [
            "ರಾಷ್ಟ್ರೀಯ ಮಕ್ಕಳ ಸಹಾಯವಾಣಿ: 1098 | ಸೈಬರ್ ಸಹಾಯವಾಣಿ: 1930.",
            "ಅನಾಮಧೇಯ ಖಾತೆಗಳೊಂದಿಗೆ ವಾದ ಮಾಡಬೇಡಿ.",
            "ಇನ್‌ಸ್ಟಾಗ್ರಾಮ್‌ನಲ್ಲಿ ಅಶ್ಲೀಲ ಕಮೆಂಟ್‌ಗಳನ್ನು ಫಿಲ್ಟರ್ ಮಾಡಲು ಸೆಟ್ಟಿಂಗ್ಸ್ ಬಳಸಿ."
        ]
    },
    {
        "id": "deepfake_sextortion",
        "icon": "⚠️",
        "title_en": "AI Deepfakes & Sextortion Awareness",
        "title_kn": "AI ಡೀಪ್‌ಫೇಕ್ ಮತ್ತು ಸೆಕ್ಸ್ಟಾರ್ಷನ್ ಜಾಗೃತಿ",
        "summary_en": "Recognize AI voice cloning, morphed photography blackmail, and know the vital rules: NEVER PAY.",
        "summary_kn": "AI ಮೂಲಕ ಧ್ವನಿ ಮತ್ತು ಫೋಟೋ ಮಾರ್ಫಿಂಗ್ ಮಾಡಿ ಬ್ಲ್ಯಾಕ್‌ಮೇಲ್ ಮಾಡುವ ಜಾಲದ ವಿರುದ್ಧ ಜಾಗೃತಿ.",
        "content_en": """
        **Understanding Modern Digital Extortion:**
        - **How the Trap Works:** Fraudsters send video call requests on Instagram or WhatsApp, play a pre-recorded revealing clip, screenshot your reaction, or morph your public face onto illicit media using AI software.
        - **The Threat:** They demand ₹10,000 to ₹50,000 within 30 minutes, threatening to forward the clip to your parents, college friends, or social media followers.
        - **THE GOLDEN RULE: NEVER SEND A SINGLE RUPEE.** Paying once guarantees they will ask for more money. Once you pay, they realize you are compliant and will never stop extorting you.
        """,
        "content_kn": """
        **ಡಿಜಿಟಲ್ ಬ್ಲ್ಯಾಕ್‌ಮೇಲ್ ತಡೆಗಟ್ಟುವಿಕೆ:**
        - **ವಂಚನೆಯ ವಿಧಾನ:** ವಾಟ್ಸಾಪ್ ವಿಡಿಯೋ ಕಾಲ್ ಮಾಡಿ ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ತೆಗೆಯುವುದು ಅಥವಾ AI ಬಳಸಿ ಸೋಷಿಯಲ್ ಮೀಡಿಯಾ ಫೋಟೋಗಳನ್ನು ಮಾರ್ಫ್ ಮಾಡಿ ಹಣಕ್ಕಾಗಿ ಬೆದರಿಕೆ ಹಾಕುವುದು.
        - **ಬೆದರಿಕೆ:** 30 ನಿಮಿಷಗಳಲ್ಲಿ ಹಣ ನೀಡದಿದ್ದರೆ ಕುಟುಂಬದವರಿಗೆ ಮತ್ತು ಸ್ನೇಹಿತರಿಗೆ ಕಳುಹಿಸುವುದಾಗಿ ಬೆದರಿಸುತ್ತಾರೆ.
        - **ಸುವರ್ಣ ನಿಯಮ: ಎಂದಿಗೂ ಒಂದು ರೂಪಾಯಿಯನ್ನೂ ನೀಡಬೇಡಿ!** ಒಮ್ಮೆ ಹಣ ನೀಡಿದರೆ ಅವರು ಮತ್ತೆ ಮತ್ತೆ ಹಣ ಕೇಳುತ್ತಾರೆ. ತಕ್ಷಣ 1930 ಗೆ ಕರೆ ಮಾಡಿ.
        """,
        "tips_en": [
            "Immediately disconnect and block video calls from unknown foreign numbers (+92, +63, etc.).",
            "Keep personal photos private on Instagram; avoid accepting video calls from strangers.",
            "Report immediately to cybercrime.gov.in under the 'Report Anonymous / Women & Child Crime' portal."
        ],
        "tips_kn": [
            "ಅಪರಿಚಿತ ಸಂಖ್ಯೆಗಳಿಂದ ಬರುವ ವಿಡಿಯೋ ಕಾಲ್‌ಗಳನ್ನು ಸ್ವೀಕರಿಸಬೇಡಿ.",
            "ನಿಮ್ಮ ಪ್ರೊಫೈಲ್ ಅನ್ನು ಪ್ರೈವೇಟ್ ಆಗಿ ಇಟ್ಟುಕೊಳ್ಳಿ.",
            "ತಕ್ಷಣ cybercrime.gov.in ನಲ್ಲಿ ದೂರು ದಾಖಲಿಸಿ."
        ]
    },
    {
        "id": "fake_internships",
        "icon": "💼",
        "title_en": "Fake Internships & Data Entry Traps",
        "title_kn": "ನಕಲಿ ಇಂಟರ್ನ್‌ಶಿಪ್ ಮತ್ತು ಡೇಟಾ ಎಂಟ್ರಿ ವಂಚನೆ",
        "summary_en": "Identify bogus work-from-home offers demanding upfront security deposits, registration fees, or typing penalties.",
        "summary_kn": "ಮುಂಗಡ ಠೇವಣಿ ಕೇಳುವ ಮತ್ತು ದಂಡದ ಬೆದರಿಕೆ ಹಾಕುವ ನಕಲಿ ವರ್ಕ್-ಫ್ರಮ್-ಹೋಮ್ ಇಂಟರ್ನ್‌ಶಿಪ್‌ಗಳ ವಿರುದ್ಧ ಎಚ್ಚರ.",
        "content_en": """
        **Spotting Fake College Internships:**
        - **Prepaid Fee Demand:** Any company asking a college student to pay ₹1,500 for an 'offer letter', 'training kit', or 'security clearance' is a scam. Legitimate internships pay YOU, not the other way around.
        - **Data Entry Agreement Scam:** Scammers get students to sign an online digital form, assign impossible OCR typing tasks, declare that errors occurred, and have a fake 'lawyer' call threatening legal action under the IT Act unless ₹15,000 in penalties is transferred.
        """,
        "content_kn": """
        **ನಕಲಿ ಇಂಟರ್ನ್‌ಶಿಪ್ ಗುರುತಿಸುವುದು:**
        - **ಶುಲ್ಕ ಕೇಳುವಿಕೆ:** ಇಂಟರ್ನ್‌ಶಿಪ್ ನೀಡಲು ಆಫರ್ ಲೆಟರ್ ಅಥವಾ ತರಬೇತಿ ಶುಲ್ಕವೆಂದು ಹಣ ಕೇಳಿದರೆ ಅದು 100% ಮೋಸ.
        - **ದಂಡದ ಬೆದರಿಕೆ:** ನಕಲಿ ಡೇಟಾ ಎಂಟ್ರಿ ಕೆಲಸ ನೀಡಿ, ನೀವು ತಪ್ಪು ಮಾಡಿದ್ದೀರಿ ಎಂದು ವಕೀಲರ ಹೆಸರಿನಲ್ಲಿ ಕರೆ ಮಾಡಿ ದಂಡ ಪಾವತಿಸಲು ಬೆದರಿಸುವುದು.
        """,
        "tips_en": [
            "Verify employer credentials on LinkedIn and MCA (Ministry of Corporate Affairs) portal.",
            "Never pay money to secure an internship or employment.",
            "Fake legal notices received via WhatsApp have zero legal validity. Do not panic."
        ],
        "tips_kn": [
            "ಕಂಪನಿಯ ನೈಜತೆಯನ್ನು LinkedIn ನಲ್ಲಿ ಪರಿಶೀಲಿಸಿ.",
            "ಉದ್ಯೋಗ ಅಥವಾ ಇಂಟರ್ನ್‌ಶಿಪ್ ಪಡೆಯಲು ಹಣ ನೀಡಬೇಡಿ.",
            "ವಾಟ್ಸಾಪ್‌ನಲ್ಲಿ ಬರುವ ನಕಲಿ ಲೀಗಲ್ ನೋಟಿಸ್‌ಗಳಿಗೆ ಹೆದರಬೇಡಿ."
        ]
    }
]


INTERACTIVE_CHALLENGES = [
    {
        "id": "sc1",
        "scenario_en": "You receive a Discord message: 'Hey bro, our Valorant tournament needs 1 more player. Join our roster here: http://val0rant-championship.gg-auth.net and verify your Steam inventory!'",
        "scenario_kn": "ಡಿಸ್ಕಾರ್ಡ್‌ನಲ್ಲಿ ಸಂದೇಶ ಬಂದಿದೆ: 'ನಮ್ಮ ವೇಲೋರೆಂಟ್ ಟೂರ್ನಮೆಂಟ್‌ಗೆ ನೀವೂ ಸೇರಿ: http://val0rant-championship.gg-auth.net ನಲ್ಲಿ ನಿಮ್ಮ ಸ್ಟೀಮ್ ಖಾತೆ ಲಿಂಕ್ ಮಾಡಿ!'",
        "is_scam": True,
        "explanation_en": "SCAM! The domain 'gg-auth.net' is a phishing trap built to steal your Steam session token and inventory skins.",
        "explanation_kn": "ಇದು ವಂಚನೆ! 'gg-auth.net' ಎಂಬುದು ನಿಮ್ಮ ಗೇಮಿಂಗ್ ಖಾತೆ ಮತ್ತು ಸ್ಕಿನ್‌ಗಳನ್ನು ಕದಿಯುವ ಫಿಶಿಂಗ್ ಸೈಟ್."
    },
    {
        "id": "sc2",
        "scenario_en": "You applied for an internship on Internshala. The verified HR sends an email from 'careers@infosys.com' asking for a 30-minute technical interview on Microsoft Teams. No money is requested.",
        "scenario_kn": "ಇಂಟರ್ನ್‌ಶಾಲಾದಲ್ಲಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಿದ್ದೀರಿ. ಇನ್ಫೋಸಿಸ್ ಅಧಿಕೃತ ಇಮೇಲ್ 'careers@infosys.com' ನಿಂದ ಟೆಕ್ನಿಕಲ್ ಇಂಟರ್ವ್ಯೂ ಆಹ್ವಾನ ಬಂದಿದೆ. ಯಾವುದೇ ಹಣ ಕೇಳಿಲ್ಲ.",
        "is_scam": False,
        "explanation_en": "LEGITIMATE! Sent from an official corporate domain (@infosys.com) with standard professional interview procedures and zero fee demands.",
        "explanation_kn": "ಇದು ನೈಜ ಆಹ್ವಾನ! ಅಧಿಕೃತ ಕಾರ್ಪೊರೇಟ್ ಇಮೇಲ್‌ನಿಂದ ಬಂದಿದ್ದು, ಯಾವುದೇ ಹಣ ಕೇಳಿಲ್ಲ."
    },
    {
        "id": "sc3",
        "scenario_en": "An Instagram account offers: 'DM me your college student ID to get Apple Student Discount MacBook for ₹15,000 only. Pay via Google Pay advance!'",
        "scenario_kn": "ಇನ್‌ಸ್ಟಾಗ್ರಾಮ್‌ನಲ್ಲಿ: 'ನಿಮ್ಮ ಕಾಲೇಜು ಐಡಿ ಕಳುಹಿಸಿ ಕೇವಲ ₹15,000 ಕ್ಕೆ ಹೊಸ ಆಪಲ್ ಮ್ಯಾಕ್‌ಬುಕ್ ಪಡೆಯಿರಿ. ಹಣವನ್ನು ಗೂಗಲ್ ಪೇ ಮೂಲಕ ಮುಂಗಡವಾಗಿ ಪಾವತಿಸಿ!'",
        "is_scam": True,
        "explanation_en": "SCAM! Apple student discounts are exclusively provided through authorized Apple stores and UNiDAYS. Nobody sells ₹1 Lakh laptops for ₹15,000.",
        "explanation_kn": "ವಂಚನೆ! ಆಪಲ್ ಸಂಸ್ಥೆ ಅಧಿಕೃತ ಸ್ಟೋರ್‌ನಲ್ಲಿ ಮಾತ್ರ ರಿಯಾಯಿತಿ ನೀಡುತ್ತದೆ. ₹1 ಲಕ್ಷದ ಲ್ಯಾಪ್‌ಟಾಪ್ ₹15,000 ಕ್ಕೆ ಸಿಗುವುದಿಲ್ಲ."
    }
]


def main():
    lang = get_current_language()
    title = t("student_title")
    subtitle = t("student_subtitle")
    render_page_header(title, subtitle, badge_text="STUDENT & GAMER HUB")

    user = get_active_user()

    # Interactive Challenge Section
    st.markdown(
        f"""
        <div class="cyber-card cyber-card-accent" style="margin-bottom: 25px;">
            <div style="display: flex; gap: 12px; align-items: center;">
                <span style="font-size: 30px;">🎮</span>
                <div>
                    <h3 style="margin: 0; color: #00f0ff;">
                        {'Interactive Challenge: Spot the Fake!' if lang == 'en' else 'ಸಂವಾದಾತ್ಮಕ ಸವಾಲು: ನಕಲಿಯನ್ನು ಗುರುತಿಸಿ!'}
                    </h3>
                    <p style="margin: 4px 0 0 0; color: #94a3b8; font-size: 14px;">
                        {'Examine these 3 real student scenarios. Decide whether each is Genuine or a Scam.' if lang == 'en' else 'ಈ ಮೂರು ಸನ್ನಿವೇಶಗಳನ್ನು ಓದಿ ಅದು ನೈಜವೇ ಅಥವಾ ವಂಚನೆಯೇ ಎಂದು ಗುರುತಿಸಿ.'}
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for c_idx, ch in enumerate(INTERACTIVE_CHALLENGES):
        sc_text = ch["scenario_en"] if lang == "en" else ch["scenario_kn"]
        st.markdown(
            f"""
            <div style="background: rgba(11, 19, 41, 0.8); border: 1px solid rgba(0, 240, 255, 0.2); border-radius: 12px; padding: 16px; margin-bottom: 15px;">
                <div style="font-size: 13px; color: #00f0ff; font-weight: 700; text-transform: uppercase;">CHALLENGE #{c_idx + 1}</div>
                <div style="color: #f8fafc; font-size: 15px; margin: 8px 0 12px 0;">"{sc_text}"</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_b1, col_b2 = st.columns(2)
        ans_key = f"chal_res_{ch['id']}"

        with col_b1:
            if st.button("🛡️ " + ("Looks Legitimate" if lang == "en" else "ನೈಜವಾಗಿದೆ"), key=f"legit_{ch['id']}"):
                st.session_state[ans_key] = False
        with col_b2:
            if st.button("🚨 " + ("It's a Cyber Scam!" if lang == "en" else "ಇದು ವಂಚನೆ!"), key=f"scam_{ch['id']}"):
                st.session_state[ans_key] = True

        if ans_key in st.session_state:
            user_eval = st.session_state[ans_key]
            correct = user_eval == ch["is_scam"]
            exp_text = ch["explanation_en"] if lang == "en" else ch["explanation_kn"]
            if correct:
                st.success(f"✅ {'CORRECT DECISION!' if lang == 'en' else 'ಸರಿಯಾದ ನಿರ್ಧಾರ!'} {exp_text}")
            else:
                st.error(f"❌ {'INCORRECT!' if lang == 'en' else 'ತಪ್ಪು!'} {exp_text}")

    st.markdown("---")

    # Core Curriculum Topics
    st.markdown(f"### 📚 {'Core Student Safety Curriculum' if lang == 'en' else 'ವಿದ್ಯಾರ್ಥಿ ಸುರಕ್ಷತಾ ಪಠ್ಯಕ್ರಮ'}")

    for idx, top in enumerate(STUDENT_TOPICS):
        t_id = top["id"]
        t_title = top["title_en"] if lang == "en" else top["title_kn"]
        t_sum = top["summary_en"] if lang == "en" else top["summary_kn"]
        t_content = top["content_en"] if lang == "en" else top["content_kn"]
        t_tips = top["tips_en"] if lang == "en" else top["tips_kn"]

        is_done = is_lesson_completed(user["id"], "student_zone", t_id)
        pill = (
            """<span class="badge-pill badge-green">✓ COMPLETED</span>"""
            if is_done
            else """<span class="badge-pill badge-cyan">STUDENT MODULE</span>"""
        )

        with st.expander(f"{top.get('icon', '🎓')} {t_title}", expanded=(idx == 0)):
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <div style="color: #00f0ff; font-weight: 600;">{t_sum}</div>
                    <div>{pill}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(t_content)

            st.markdown(
                f"""
                <div class="cyber-card cyber-card-success" style="padding: 16px; margin-top: 15px;">
                    <h5 style="color: #00ff9d; margin: 0 0 8px 0;">🛡️ {'Actionable Student Safety Tips' if lang == 'en' else 'ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ಸುರಕ್ಷತಾ ಸಲಹೆಗಳು'}</h5>
                    <ul style="color: #e2e8f0; font-size: 14px; margin: 0; padding-left: 20px;">
                        {''.join([f"<li>{tp}</li>" for tp in t_tips])}
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            if not is_done:
                if st.button(
                    f"✅ {t('mark_as_completed')}",
                    key=f"complete_student_{t_id}",
                ):
                    mark_lesson_completed(user["id"], "student_zone", t_id)
                    st.success(t("lesson_completed"))
                    st.rerun()
            else:
                st.info(f"✓ {t('already_completed')}")

    render_footer()


if __name__ == "__main__":
    main()
