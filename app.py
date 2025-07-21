# Also serve landing page at /index.html
from flask import Flask, render_template, request,redirect, url_for, session, flash,jsonify
import json
import requests
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key'
CONFIG_FILE = 'config.json'
USERS_FILE = "users.json"

def load_allowed_users():
    try:
        with open(USERS_FILE,"r") as f:
            return json.load(f).get("allowed_users", [])
    except Exception:
        return []

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def log_payload(user,environment, payload, response_text, status_code):
    print("📦 Log written for:", environment or "(none)")
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user": user,
        "environment": environment or "UNKNOWN",
        "entries": payload or {},
        "response_status": status_code,
        "response_text": response_text or "No response"
    }
    with open("sent_payloads_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        allowed_users = load_allowed_users()
        if username in allowed_users:
            session['user'] = username
            session['password'] = password
            return redirect('/index.html')
        else:
            error = "Access denied. Unauthorized user."
            return render_template('login.html', error=error)

    return render_template('login.html', error=None)



@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    from datetime import datetime
    return render_template('index.html', year=datetime.now().year)
@app.route('/index.html', methods=['GET', 'POST'])
@login_required
def index_html():
    from datetime import datetime
    return render_template('index.html', year=datetime.now().year)
# New route for config update
@app.route('/update-config', methods=['GET', 'POST'])
@login_required
def update_config():
    config = load_config()
    user = session['user']
    password = session['password']

    if request.method == 'POST':
        print("📝 Received POST request", flush=True)

        data = request.form or request.get_json()
        environment = data.get('environment')
        payload_raw = data.get('jsonPayload')

        wrapper = None
        response_text = ''
        status_code = None

        try:
            if not environment or not payload_raw:
                raise ValueError("Missing environment or payload")

            url = config.get(environment)
            if not url:
                raise ValueError("Invalid environment")

            wrapper = json.loads(payload_raw)

            print("Sending payload to Pega:")
            print(json.dumps(wrapper, indent=2), flush=True)
            print("user:", user, "password:", password, flush=True)

            response = requests.post(url, json=wrapper, auth=(user, password), timeout=15)

            response_text = response.text
            status_code = response.status_code

            if response.status_code == 200:
                success = True
                message = "✅ DSS updated"
            else:
                success = False
                message = f" Failed {response.status_code}"

        except Exception as e:
            success = False
            message = f" Exception: {str(e)}"
            response_text = str(e)
            status_code = 500

        finally:
            log_payload(user,environment, wrapper, response_text, status_code)

        return jsonify({"success": success, "message": message, "response": response_text}), status_code

    return render_template('updateDSSConfig.html', environments=list(config.keys()), config=config)

@app.route('/logs')
def view_logs():
    logs = []
    try:
        with open("sent_payloads_log.jsonl", "r") as f:
            for line in f:
                logs.append(json.loads(line))
        logs.reverse()
    except FileNotFoundError:
        pass
    return render_template('logs.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True)
