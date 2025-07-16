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
def log_payload(environment, payload, response_text, status_code):
    print("💾 Logging payload to file...", flush=True)
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "environment": environment,
        "entries": payload,
        "response_status": status_code,
        "response_text": response_text
    }
    with open("sent_payloads_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

@app.route('/', methods=['GET', 'POST'])
def index():
    config = load_config()

    if request.method == 'POST':
        print("📝 Received POST request", flush=True)
        environment = request.form['environment']
        url = config.get(environment)

        if not url:
            flash("Invalid environment selected", "error")
            return redirect(url_for('index'))

        if 'jsonPayload' not in request.form:
            flash("Missing payload.", "error")
            return redirect(url_for('index'))

        try:
            wrapper  = json.loads(request.form['jsonPayload'])

            print("Sending payload to Pega:", flush=True)
            print(json.dumps(wrapper, indent=2), flush=True)

            response = requests.post(url, json=wrapper, auth=('pega_user', 'pega_pass'))
            #log_payload(environment, wrapper, response.text, response.status_code)

            if response.status_code == 200:
                flash("✅ DSS values updated successfully", "success")
            else:
                flash(f"❌ Failed: {response.status_code} - {response.text}", "error")

            # Log only after successful or failed post (not earlier!)
            log_payload(environment, wrapper, response.text, response.status_code)

        except Exception as e:
            flash(f"❌ Exception: {str(e)}", "error")

        return redirect(url_for('index'))  # 🛑 POST-Redirect-GET

    return render_template('index.html', environments=list(config.keys()), config=config)
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
