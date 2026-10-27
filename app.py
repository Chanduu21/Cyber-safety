from flask import Flask, render_template, request, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).with_name('quiz_results.db')

SCAMS = [
    {'title': 'UPI payment fraud', 'category': 'Payments', 'icon': '💸', 'description': 'Scammers may send fake collect requests or claim you must enter a UPI PIN to receive money.', 'warning': 'You never need to enter your UPI PIN to receive money.', 'action': 'Decline unexpected collect requests and verify payments inside your official banking app.'},
    {'title': 'Phishing messages', 'category': 'Links', 'icon': '🎣', 'description': 'Fake emails or messages imitate banks, delivery services, colleges, or popular websites.', 'warning': 'Urgent threats, prizes, and suspicious links are common warning signs.', 'action': 'Do not tap the link. Open the official website or app yourself.'},
    {'title': 'OTP and account scams', 'category': 'Account safety', 'icon': '🔐', 'description': 'Someone may pretend to be a bank employee or support agent and ask for your OTP.', 'warning': 'Never share an OTP, password, PIN, or recovery code.', 'action': 'End the conversation and contact the organisation using its official contact details.'},
    {'title': 'Fake job offers', 'category': 'Jobs', 'icon': '💼', 'description': 'Fraudsters promise easy work or high pay but demand registration fees or personal data.', 'warning': 'A demand for money to guarantee a job is a major red flag.', 'action': 'Research the employer and never pay to unlock a promised job.'},
    {'title': 'Impersonation scams', 'category': 'Social media', 'icon': '🎭', 'description': 'A scammer may use a copied profile or pretend to be a friend or relative asking for money.', 'warning': 'A familiar profile does not prove the message is genuine.', 'action': 'Verify through a separate call or trusted contact method before sending money.'},
    {'title': 'Fake shopping websites', 'category': 'Shopping', 'icon': '🛍️', 'description': 'Fraudulent stores advertise unbelievable discounts and may never deliver products.', 'warning': 'Check the domain, reviews, return policy, and payment options.', 'action': 'Use trusted sellers and avoid unfamiliar payment links.'},
]
QUESTIONS = [
    {'question': 'A caller asks for your bank OTP to stop a transaction. What should you do?', 'options': ['Share it quickly', 'Never share it; contact your bank through official channels', 'Send it to a friend'], 'answer': 1, 'explanation': 'Banks do not need you to reveal your OTP over a call.'},
    {'question': 'Someone sends a UPI collect request and says you must enter your PIN to receive money. Is this safe?', 'options': ['Yes, always', 'Only if they sound trustworthy', 'No, a UPI PIN is not needed to receive money'], 'answer': 2, 'explanation': 'Entering a UPI PIN authorises a payment; do not use it to receive money.'},
    {'question': 'What is the safest response to an unexpected prize link?', 'options': ['Open it immediately', 'Avoid the link and verify through an official source', 'Forward it to everyone'], 'answer': 1, 'explanation': 'Unexpected prizes and urgent links can be phishing attempts.'},
    {'question': 'A person claiming to be your friend urgently asks for money from a new number. What should you do?', 'options': ['Send it immediately', 'Verify by calling your friend on a known number', 'Post your bank details'], 'answer': 1, 'explanation': 'Verify requests using a separate, trusted channel.'},
    {'question': 'If you suspect online financial fraud in India, what should you do?', 'options': ['Wait several days', 'Delete all evidence', 'Contact your bank immediately and report it at 1930 / cybercrime.gov.in'], 'answer': 2, 'explanation': 'Act quickly: contact your bank and report financial cyber fraud through official channels.'},
]

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS quiz_results (id INTEGER PRIMARY KEY AUTOINCREMENT, score INTEGER NOT NULL, total INTEGER NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')

@app.route('/')
def home():
    return render_template('index.html', scams=SCAMS, question_count=len(QUESTIONS))

@app.route('/api/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'GET':
        return jsonify([{ 'question': q['question'], 'options': q['options'] } for q in QUESTIONS])
    payload = request.get_json(silent=True) or {}
    answers = payload.get('answers', [])
    score = sum(1 for i, q in enumerate(QUESTIONS) if i < len(answers) and answers[i] == q['answer'])
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('INSERT INTO quiz_results (score, total) VALUES (?, ?)', (score, len(QUESTIONS)))
    return jsonify({'score': score, 'total': len(QUESTIONS), 'message': 'Great effort! Keep practising safe digital habits.' if score == len(QUESTIONS) else 'Review the safety tips and try again.', 'explanations': [q['explanation'] for q in QUESTIONS]})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
