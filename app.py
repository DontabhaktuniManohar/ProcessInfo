from flask import Flask, render_template, request, redirect, url_for, flash
import json
import requests
import os
from datetime import datetime
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'your-secret-key'
CONFIG_FILE = 'config.json'

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)
def log_payload(environment, payload):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "environment": environment,
        "entries": payload
    }
    with open("sent_payloads_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

@app.route('/', methods=['GET', 'POST'])
def index():
    config = load_config()
    environments = config

    if request.method == 'POST':
        environment = request.form['environment']
        url = config.get(environment)
        if not url:
            flash("Invalid environment selected", "error")
            return redirect(url_for('index'))

        if 'jsonPayload' not in request.form:
            flash("Missing payload.", "error")
            return redirect(url_for('index'))

        try:
            dss_entries = json.loads(request.form['jsonPayload'])
            print("Sending payload to Pega:",flush=True)
            print(json.dumps(dss_entries, indent=2),flush=True)
            log_payload(environment, dss_entries)
            response = requests.post(url, json=dss_entries, auth=('pega_user', 'pega_pass'))
            if response.status_code == 200:
                flash("DSS values updated successfully", "success")
            else:
                flash(f"Failed: {response.status_code} - {response.text}", "error")

        except Exception as e:
            flash(f"Exception: {str(e)}", "error")

    return render_template('index.html', environments=environments)
@app.route('/logs')
def view_logs():
    logs = []
    try:
        with open("sent_payloads_log.jsonl", "r") as f:
            for line in f:
                logs.append(json.loads(line))
    except FileNotFoundError:
        pass
    return render_template('logs.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True)
