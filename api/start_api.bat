@echo off
echo ============================================================
echo LinkedIn Post Intelligence API - Startup Script
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "..\venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run this from the project root:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call ..\venv\Scripts\activate.bat

REM Install API dependencies
echo.
echo Installing API dependencies...
pip install -r requirements.txt

REM Check if models exist
if not exist "..\src\models\engagement_model.pkl" (
    echo.
    echo ERROR: ML models not found!
    echo Please run the Jupyter notebook to train and save models:
    echo   notebooks/02_engagement_prediction_model.ipynb
    pause
    exit /b 1
)

REM Start the API server
echo.
echo ============================================================
echo Starting Flask API Server...
echo ============================================================
echo Server will be available at: http://localhost:5000
echo API Documentation: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python app.py

pause
