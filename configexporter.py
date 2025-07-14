from flask import Flask, request, render_template_string, redirect, url_for
import json
import os

app = Flask(__name__)
CONFIG_FILE = 'config.json'

# Load or initialize config
def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

@app.route('/')
def index():
    config = load_config()
    return render_template_string(TEMPLATE, config=config)

@app.route('/add_app', methods=['POST'])
def add_app():
    appname = request.form.get('appname').strip()
    config = load_config()
    if appname and appname not in config:
        config[appname] = []
        save_config(config)
    return redirect(url_for('index'))

@app.route('/delete_app/<appname>')
def delete_app(appname):
    config = load_config()
    if appname in config:
        del config[appname]
        save_config(config)
    return redirect(url_for('index'))

@app.route('/add_dc/<appname>', methods=['POST'])
def add_dc(appname):
    dc = request.form.get('dc').strip()
    config = load_config()
    if dc and dc not in config.get(appname, []):
        config[appname].append(dc)
        save_config(config)
    return redirect(url_for('index'))

@app.route('/remove_dc/<appname>/<dc>')
def remove_dc(appname, dc):
    config = load_config()
    if appname in config and dc in config[appname]:
        config[appname].remove(dc)
        save_config(config)
    return redirect(url_for('index'))

TEMPLATE = """
<!doctype html>
<title>App/DC Config Editor</title>
<h2>🛠 App & DC Configuration</h2>
<form method="post" action="/add_app">
  <input name="appname" placeholder="New App Name">
  <button type="submit">➕ Add App</button>
</form>
<hr>
{% for app, dcs in config.items() %}
  <h3>{{ app }}
    <a href="/delete_app/{{ app }}" style="color:red; float:right;">🗑 Delete App</a>
  </h3>
  <ul>
    {% for dc in dcs %}
      <li>{{ dc }} <a href="/remove_dc/{{ app }}/{{ dc }}" style="color:gray;">❌</a></li>
    {% endfor %}
  </ul>
  <form method="post" action="/add_dc/{{ app }}">
    <input name="dc" placeholder="Add DC">
    <button type="submit">➕ Add DC</button>
  </form>
  <hr>
{% endfor %}
"""

if __name__ == '__main__':
    app.run(debug=True, port=5050)



from flask import Flask, Response
from prometheus_client import Gauge, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST
import subprocess
import csv
import os

app = Flask(__name__)
registry = CollectorRegistry()

service_status_gauge = Gauge(
    'service_up_status',
    '1 if service is UP, 0 otherwise',
    ['app', 'dc', 'appname', 'url', 'version'],
    registry=registry
)

# Central config: app → list of DCs
APP_DC_CONFIG = {
    'bapp': ['awseast', 'europe'],
    'capp': ['awswest'],
    'dapp': ['apac', 'awseast', 'awswest'],
    # Easily extendable
}

def collect_all_metrics():
    service_status_gauge.clear()

    for app_name, dc_list in APP_DC_CONFIG.items():
        for dc in dc_list:
            input_file = f'abc-{app_name}-{dc}.txt'
            output_file = f'abc-{app_name}-{dc}.csv'

            try:
                subprocess.run(
                    ['python3', 'main.py', '-f', input_file, '-dc', dc, '-r', output_file],
                    check=True,
                    capture_output=True,
                    text=True
                )
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] main.py failed for {app_name}-{dc}: {e.stderr}")
                continue

            if not os.path.exists(output_file):
                print(f"[WARN] Missing output file: {output_file}")
                continue

            with open(output_file, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    appname = row.get('appname', '').strip()
                    url = row.get('service url', '').strip()
                    version = row.get('version', '').strip()
                    status = 1 if row.get('status', '').strip().upper() == 'UP' else 0

                    service_status_gauge.labels(
                        app=app_name,
                        dc=dc,
                        appname=appname,
                        url=url,
                        version=version
                    ).set(status)

@app.route('/metrics')
def metrics():
    collect_all_metrics()
    return Response(generate_latest(registry), mimetype=CONTENT_TYPE_LATEST)

@app.route('/')
def index():
    return 'Dynamic Multi-App Multi-DC Exporter is running. Visit /metrics.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
