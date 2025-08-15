@echo off
echo 🚀 Starting Ledger of Legends...
echo ==================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo ❌ requirements.txt not found
    echo Please run this script from the project directory
    pause
    exit /b 1
)

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

REM Run the application
echo 🌐 Starting the Ledger of Legends web application...
echo 📱 The app will open in your default browser
echo 🔗 If it doesn't open automatically, go to: http://localhost:8501
echo ==================================================

streamlit run enhanced_app.py --server.port 8501 --server.address localhost

pause
