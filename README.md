# CyberWise — Cyber Safety & Digital Fraud Awareness

A beginner-friendly college project that teaches students and senior citizens to recognise online scams and practise safe digital habits.

## Features
- Responsive, professional dashboard
- Searchable scam awareness library
- Interactive safety checklist with progress tracking
- Five-question quiz scored by a Flask backend
- SQLite storage for quiz results
- Link to India's official cybercrime reporting portal

## Technology
- Frontend: HTML, CSS, JavaScript
- Backend: Python Flask
- Database: SQLite (created automatically when the app starts)

## Run in VS Code (Windows)
1. Install Python 3.10 or later and VS Code.
2. Extract the ZIP file.
3. In VS Code, choose **File → Open Folder** and open the `cyber-safety-app` folder.
4. Open **Terminal → New Terminal** and run:

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```

5. Open `http://127.0.0.1:5000` in your browser.

If `py` is not recognised, try `python -m venv .venv`. If PowerShell blocks activation, run `python -m pip install -r requirements.txt` and then `python app.py` without activating the environment.

## Project structure
```text
cyber-safety-app/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── css/style.css
    └── js/script.js
```

## Safety note
This is an educational prototype, not a banking or security product. Never enter real passwords, OTPs, or financial information into a demo application. In India, suspected financial cyber fraud should be reported promptly through official channels such as 1930 and https://cybercrime.gov.in/.
