@echo off
echo Starting Frontend Server...
cd /d C:\Users\sebas\PycharmProjects\Full_Stack_Ai_Development\frontend
npm start
pause
@echo off
echo Starting Flask Backend...
cd /d C:\Users\sebas\PycharmProjects\Full_Stack_Ai_Development
call .venv\Scripts\activate.bat
python app.py
pause

