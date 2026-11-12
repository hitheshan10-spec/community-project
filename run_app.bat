@echo off
echo ========================================================
echo   CYBERSHIELD: Your Digital Safety Companion
echo   Launching local Streamlit web application...
echo ========================================================
cd /d "%~dp0CyberShield"
if exist "..\.venv\Scripts\streamlit.exe" (
    ..\.venv\Scripts\streamlit.exe run app.py
) else (
    streamlit run app.py
)
pause
