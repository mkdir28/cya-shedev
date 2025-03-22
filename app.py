from flask import Flask, render_template, request, jsonify, redirect, url_for
import os

app = Flask(__name__)

# Store participants' scores
user_scores = {}

# Theoretical questions (with correct answers)
theoretical_questions = {
    "q1": {"question": "What is the command to connect securely to remote server via SSH?", "correct_answer": "ssh username@remote_host"},
    "q2": {"question": "How can you check which users are currently logged into a Linux system?", "correct_answer": "who"},
    "q3": {"question": "What is the purpose of the cat command, and how can it be used to display the contents of a file in Linux?", "correct_answer": "cat filename"},
    "q4": {"question": "How do you check the current network interfaces and their IP addresses on a Linux system?", "correct_answer": "ifconfig"},
    "q5": {"question": "How do you use Nmap to scan a remote host for open ports?","correct_answer": "nmap target_ip"}

}

# Practical CTF challenges (flags and tasks)
ctf_challenges = {
    "escalate_privileges": {
        "task": "To escalate privileges and retrieve the flag, use commands like `sudo` or `su`. The flag is in /root/flag.txt.",
        "steps": [
            {"prompt": "Use SSH to connect to the server (IP: 192.168.1.100, Password: password123)", "correct_answer": "ssh user@192.168.1.100"},
            {"prompt": "Scan the users using Nmap", "correct_answer": "nmap -p- 192.168.1.100"},
            {"prompt": "Use Gobuster to enumerate directories", "correct_answer": "gobuster dir -u http://192.168.1.100 -w /usr/share/wordlists/dirb/common.txt"},
            {"prompt": "Change file permissions to gain access", "correct_answer": "chmod 777 /root/flag.txt"},
            {"prompt": "Gain root access", "correct_answer": "sudo su"},
            {"prompt": "Read the flag file", "correct_answer": "cat /root/flag.txt"}
        ],
        "flag": "CTF{privilege_escalation_successful}"
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/theoretical_questions')
def theoretical_questions_page():
    username = request.args.get("username")
    return render_template('theoretical_questions.html', questions=theoretical_questions, username=username)

@app.route('/submit_theoretical', methods=['POST'])
def submit_theoretical():
    data = request.json
    username = data.get("username")
    answers = data.get("answers")

    # Initialize user score if not exists
    if username not in user_scores:
        user_scores[username] = {'theoretical': 0, 'practical': 0}

    # Check answers and update theoretical score
    for qid, user_answer in answers.items():
        correct_answer = theoretical_questions[qid]["correct_answer"]
        if user_answer.lower() == correct_answer.lower():
            user_scores[username]['theoretical'] += 5  # Add 5 points per correct answer

    return jsonify({"message": "Answers submitted!", "score": user_scores[username]['theoretical']})

@app.route('/practical_challenges')
def practical_challenges():
    username = request.args.get("username")
    return render_template('challenge_page.html', challenges=ctf_challenges, username=username)


@app.route('/score_dashboard')
def score_dashboard():
    username = request.args.get("username")
    theoretical_score = user_scores.get(username, {}).get("theoretical", 0)
    practical_score = user_scores.get(username, {}).get("practical", 0)
    final_score = theoretical_score + practical_score
    return render_template('score_dashboard.html', username=username, theoretical_score=theoretical_score, practical_score=practical_score, final_score=final_score)

@app.route('/final_dashboard')
def final_dashboard():
    return render_template('final_dashboard.html', user_scores=user_scores)

if __name__ == "__main__":
    app.run(debug=True)
