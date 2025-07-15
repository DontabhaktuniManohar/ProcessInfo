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

### added dc suite###
from flask import Flask, request, render_template_string, redirect, url_for
import json
import os

app = Flask(__name__)
CONFIG_FILE = 'config.json'

# -----------------------
# Data‑layer helpers
# -----------------------

def load_config():
    """Return a dict shaped as {suite: {app: [dc, ...], ...}, ...}."""
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, 'r') as f:
        try:
            return json.load(f)
        except ValueError:
            return {}

def save_config(cfg):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(cfg, f, indent=2)

# -----------------------
# Routes
# -----------------------

@app.route('/')
def index():
    cfg = load_config()
    return render_template_string(TEMPLATE, cfg=cfg)

# Suite operations -----------------------------------------------------------

@app.route('/add_suite', methods=['POST'])
def add_suite():
    suite = request.form.get('suite', '').strip()
    cfg = load_config()
    if suite and suite not in cfg:
        cfg[suite] = {}
        save_config(cfg)
    return redirect(url_for('index'))

@app.route('/delete_suite/<suite>')
def delete_suite(suite):
    cfg = load_config()
    if suite in cfg:
        del cfg[suite]
        save_config(cfg)
    return redirect(url_for('index'))

# App operations -------------------------------------------------------------

@app.route('/add_app/<suite>', methods=['POST'])
def add_app(suite):
    appname = request.form.get('appname', '').strip()
    cfg = load_config()
    if suite in cfg and appname and appname not in cfg[suite]:
        cfg[suite][appname] = []
        save_config(cfg)
    return redirect(url_for('index'))

@app.route('/delete_app/<suite>/<appname>')
def delete_app(suite, appname):
    cfg = load_config()
    if suite in cfg and appname in cfg[suite]:
        del cfg[suite][appname]
        save_config(cfg)
    return redirect(url_for('index'))

# DC operations --------------------------------------------------------------

@app.route('/add_dc/<suite>/<appname>', methods=['POST'])
def add_dc(suite, appname):
    dc = request.form.get('dc', '').strip()
    cfg = load_config()
    if suite in cfg and appname in cfg[suite] and dc and dc not in cfg[suite][appname]:
        cfg[suite][appname].append(dc)
        save_config(cfg)
    return redirect(url_for('index'))

@app.route('/remove_dc/<suite>/<appname>/<dc>')
def remove_dc(suite, appname, dc):
    cfg = load_config()
    if suite in cfg and appname in cfg[suite] and dc in cfg[suite][appname]:
        cfg[suite][appname].remove(dc)
        save_config(cfg)
    return redirect(url_for('index'))

# -----------------------
# Page template (HTMX‑style auto refresh)
# -----------------------
TEMPLATE = """
<!doctype html>
<title>Suite / App / DC Config Editor</title>
<h2 class="title">🛠 Suite → App → DC Configuration</h2>
<style>
  body{font-family: Arial, sans-serif; margin:2rem; background:#f8f9fa}
  input,button{padding:0.3rem 0.6rem; margin:0.2rem}
  ul{list-style-type:none; padding-left:1rem}
  li{margin:0.2rem 0}
  .suite{border:1px solid #ccd; border-radius:8px; padding:1rem; background:#fff; margin-bottom:1.2rem}
  .app{margin-left:1rem; border-left:3px solid #77a; padding-left:0.7rem}
</style>

<!-- Add Suite -->
<form method="post" action="/add_suite">
  <input name="suite" placeholder="New Suite Name">
  <button type="submit">➕ Add Suite</button>
</form>
<hr>

{% for suite, apps in cfg.items() %}
  <div class="suite">
    <h3>{{ suite }}
      <a href="/delete_suite/{{ suite }}" style="color:red; float:right;">🗑 Delete Suite</a>
    </h3>
    <!-- Add App to Suite -->
    <form method="post" action="/add_app/{{ suite }}">
      <input name="appname" placeholder="Add App to {{ suite }}">
      <button type="submit">➕ Add App</button>
    </form>

    {% for app, dcs in apps.items() %}
      <div class="app">
        <strong>{{ app }}</strong>
        <a href="/delete_app/{{ suite }}/{{ app }}" style="color:red;">🗑 Remove App</a>
        <ul>
          {% for dc in dcs %}
            <li>{{ dc }}
              <a href="/remove_dc/{{ suite }}/{{ app }}/{{ dc }}" style="color:gray;">❌</a>
            </li>
          {% endfor %}
        </ul>
        <form method="post" action="/add_dc/{{ suite }}/{{ app }}">
          <input name="dc" placeholder="Add DC to {{ app }}">
          <button type="submit">➕ Add DC</button>
        </form>
      </div>
    {% endfor %}
  </div>
{% endfor %}
"""

if __name__ == '__main__':
    app.run(debug=True, port=5050)


########################

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



##  If you want to trigger collection for a specific app and dc (e.g., manually or via API), you can extend your Flask app to support this.
@app.route('/collect/<app>/<dc>', methods=['POST', 'GET'])
def collect_one(app, dc):
    input_file = f'abc-{app}-{dc}.txt'
    output_file = f'abc-{app}-{dc}.csv'

    try:
        result = subprocess.run(
            ['python3', 'main.py', '-f', input_file, '-dc', dc, '-r', output_file],
            timeout=120, capture_output=True, text=True
        )
        COLLECT_ERR.labels(app=app, dc=dc).set(0 if result.returncode == 0 else 1)
    except subprocess.TimeoutExpired:
        COLLECT_ERR.labels(app=app, dc=dc).set(1)
        return f"⏱️ Timed out for {app}-{dc}", 504

    if not os.path.exists(output_file):
        return f"❌ Output file {output_file} not found.", 404

    try:
        with open(output_file, newline='') as f:
            reader = csv.DictReader(f)
            # Remove existing metrics for this app-dc
            for label in list(STATUS._metrics):
                if label[0] == app and label[1] == dc:
                    STATUS.remove(*label)
            for row in reader:
                STATUS.labels(
                    app=app,
                    dc=dc,
                    appname=row['appname'].strip(),
                    url=row['service url'].strip(),
                    version=row['version'].strip()
                ).set(1 if row['status'].strip().upper() == 'UP' else 0)
    except Exception as e:
        return f"❌ Failed to process CSV for {app}-{dc}: {e}", 500

    return f"✅ Metrics collected for {app}-{dc}", 200

#i have given only appname and it needs to run on all dcs which should take form config.json

@app.route('/collect/<app>', methods=['POST', 'GET'])
def collect_app(app):
    # Load from config.json
    try:
        with open(CONFIG_FILE) as f:
            config = json.load(f)
    except Exception as e:
        return f"❌ Failed to load config: {e}", 500

    dcs = config.get(app)
    if not dcs:
        return f"⚠️ App '{app}' not found in config.json", 404

    success = []
    failed = []

    for dc in dcs:
        input_file = f'abc-{app}-{dc}.txt'
        output_file = f'abc-{app}-{dc}.csv'

        try:
            result = subprocess.run(
                ['python3', 'main.py', '-f', input_file, '-dc', dc, '-r', output_file],
                timeout=120, capture_output=True, text=True
            )
            COLLECT_ERR.labels(app=app, dc=dc).set(0 if result.returncode == 0 else 1)
        except subprocess.TimeoutExpired:
            COLLECT_ERR.labels(app=app, dc=dc).set(1)
            failed.append(dc)
            continue

        if not os.path.exists(output_file):
            failed.append(dc)
            continue

        try:
            # Optional cleanup of existing metrics for app+dc
            for label in list(STATUS._metrics):
                if label[0] == app and label[1] == dc:
                    STATUS.remove(*label)

            with open(output_file, newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    STATUS.labels(
                        app=app,
                        dc=dc,
                        appname=row['appname'].strip(),
                        url=row['service url'].strip(),
                        version=row['version'].strip()
                    ).set(1 if row['status'].strip().upper() == 'UP' else 0)
            success.append(dc)
        except Exception as e:
            failed.append(dc)

    return {
        "app": app,
        "success": success,
        "failed": failed,
        "status": "✅ Complete" if not failed else "⚠️ Partial"
    }, 200 if not failed else 207
