@echo off
echo Activating virtual environment...
call .venv\Scripts\activate

echo Starting FastAPI backend...
start cmd /k "uvicorn app.main:app --reload"

echo Waiting for backend to start...
timeout /t 2 >nul

echo Starting Streamlit frontend...
start cmd /k "streamlit run streamlit_app.py"

echo Application launched successfully.
pause
