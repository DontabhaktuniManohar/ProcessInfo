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
# Compare environments endpoint
@app.route('/compare-env', methods=['GET', 'POST'])
@login_required
def compare_env():
    config = load_config()
    env1 = request.form.get('env1') if request.method == 'POST' else None
    env2 = request.form.get('env2') if request.method == 'POST' else None
    noofday = request.form.get('noofdays') if request.method == 'POST' else 1

    payload = {}
    headers = {}
    result_table = []
    response_status = None
    response_message = None

    if request.method == 'POST' and env1 and env2:
        try:
            if not env1 or not env2:
                raise ValueError('Both env1 and env2 must be specified.')
            url1 = config.get(env1)
            url2 = config.get(env2)
            if not url1 or not url2:
                raise ValueError('Invalid environment selection.')

            # Append required paths
            url1 = url1.rstrip('/') + '/V1/CrossEnvDssCompare'
            url2 = url2.rstrip('/') + '/V1/getDssDetails'

            user = session['user']
            password = session['password']

            # Prepare headers
            headers = {
                'envtocompare': url2,
                'noofday': str(noofday)
            }

            # Prepare payload for first env
            payload = {}  # Customize as needed

            # Send POST to first environment with headers
            response1 = requests.post(url1, json=payload, auth=(user, password), headers=headers, timeout=15)

            # Parse response
            data1 = response1.json() if response1.status_code == 200 else {}

            # Build table using only env1 response
            rows = []
            dss_list1 = data1.get('DSS List', [])
            for d1 in dss_list1:
                rows.append({
                    'name': d1.get('Name of DSS'),
                    'env1_value': d1.get('Value'),
                    'env2_value': d1.get('Compared Env Value'),
                    'env1_updated': d1.get('Updated Date Time'),
                    'env2_updated': d1.get('Compared Env Updated Time'),
                    'env1_operator': d1.get('Updated Operator'),
                    'env2_operator': d1.get('Compared Env Updated Operator')
                })
            result_table = rows
        except Exception as e:
            response_status = 500
            response_message = str(e)

    return render_template(
        "compare_env.html",
        config=config,
        env1=env1,
        env2=env2,
        noofday=noofday,
        payload=payload,
        headers=headers,
        result_table=result_table,
        response_status=response_status,
        response_message=response_message,
        year=2025
    )
@app.route('/getdssdetail', methods=['GET', 'POST'])
@login_required
def get_dss_detail():
    config = load_config()
    environment = request.form.get('environment') if request.method == 'POST' else None
    noofday = request.form.get('noofdays') if request.method == 'POST' else 1
    custom_header = request.form.get('customHeader') if request.method == 'POST' else None

    user = session.get('user')
    password = session.get('password')
    dss_data = []
    response_status = None
    response_message = None

    if request.method == 'POST' and environment:
        try:
            url = config.get(environment)
            if not url:
                raise ValueError("Invalid environment selected.")

            url = url.rstrip('/') + '/dummy-dss'
            headers = {'noofday': str(noofday)}
            if custom_header:
                headers['customHeader'] = custom_header
            payload = {}

            response = requests.post(url, json=payload, auth=(user, password), headers=headers, timeout=15)
            response_status = response.status_code
            if response.status_code == 200:
                dss_data = response.json()
                response_message = "Success"
            else:
                response_message = f"Failed: {response.text}"
        except Exception as e:
            response_message = f"Exception: {str(e)}"
            response_status = 500

    return render_template(
        'getdssdetail.html',
        config=config,
        selected_env=environment,
        noofday=noofday,
        custom_header=custom_header,
        dss_data=dss_data,
        response_status=response_status,
        response_message=response_message,
        year=datetime.now().year
    )
@app.route('/dummy-dss', methods=['GET','POST'])
def dummy_dss():
    mock_response = {
        "Total DSS Count": 5,
        "DSS List": [
            {
                "Owning Ruleset": "Pega-RULES",
                "Name of DSS": "EnableOneClickUpgradeforChatbot",
                "Value": "true",
                "Updated Date Time": "20250724T093500.000 GMT",
                "Updated Operator": "admin"
            },
            {
                "Owning Ruleset": "Pega-SearchEngine",
                "Name of DSS": "aessetting/RuleUpdatesChange",
                "Value": "https://pdcan1.pegacloud.com/prweb/PRRestService/_BunIF",
                "Updated Date Time": "20250724T093600.000 GMT",
                "Updated Operator": "system"
            },
            {
                "Owning Ruleset": "Pega-RULES",
                "Name of DSS": "VzUp_EnableADM",
                "Value": "True",
                "Updated Date Time": "20250724T093700.000 GMT",
                "Updated Operator": "admin"
            },
            {
                "Owning Ruleset": "Pega-SearchEngine",
                "Name of DSS": "aessetting/ChannelLastSnapshotTime",
                "Value": "19700101T000000.000 GMT",
                "Updated Date Time": "20250724T093800.000 GMT",
                "Updated Operator": "system"
            },
            {
                "Owning Ruleset": "Pega-RULES",
                "Name of DSS": "Notifications_GetCases_Switch",
                "Value": "true",
                "Updated Date Time": "20250724T093900.000 GMT",
                "Updated Operator": "admin"
            }
        ]
    }
    return jsonify(mock_response)
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
