@echo off
:: Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python first.
    pause
    exit /b
)

:: Check if the virtual environment already exists
IF EXIST venv (
    echo Virtual environment already exists. Activating...
) ELSE (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate the virtual environment
call venv\Scripts\activate

:: Check if requirements.txt exists
IF NOT EXIST requirements.txt (
    echo requirements.txt not found. Please ensure it is in the same directory.
    pause
    exit /b
)

:: Install the required packages
echo Installing required packages from requirements.txt...
pip install -r requirements.txt

:: Pause the command prompt to keep it open
echo Setup is complete. Press any key to exit.
pause
