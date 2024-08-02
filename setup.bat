@echo off
REM Create a virtual environment
py -m venv django_app_venv

REM Change to the virtual environment directory
cd django_app_venv

REM Activate the virtual environment
Scripts\activate.bat

REM Create and change to the project directory
mkdir gradingProject
cd gradingProject

REM Initialize git repository
git init

REM Add the remote repository
git remote add origin https://github.com/fadiouz/django-project.git

REM Pull the project files from the remote repository
git pull origin master

REM Install the required packages from requirements.txt
pip install -r requirements.txt

REM Notify user that setup is complete
echo Setup complete.

REM Pause to keep the window open
pause