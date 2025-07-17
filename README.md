# 🛠️ Pega DSS Update Tool

A lightweight Flask web interface to update DSS (Dynamic System Settings) in your Pega environments using REST APIs. Supports JSON payload preview, mock testing, request logging, and detailed API response display.

---

## ✨ Features

- ✅ Web form to construct DSS payloads
- 🔄 Real-time JSON payload preview
- 📤 Submit DSS updates to selected environment
- 📁 View all previously submitted payloads and responses
- 💾 Download JSON payload
- 🧪 Send mock requests to [httpbin.org](https://httpbin.org) for testing
- 🔐 Flash messaging for success/failure
- 📜 Logging of all submitted requests and responses

---

## 📦 Project Structure

```
pega_dss/
├── app.py                 # Main Flask application
├── config.json            # Environment-to-URL mapping
├── sent_payloads_log.jsonl  # Logs of submitted DSS requests (JSONL format)
├── templates/
│   ├── index.html         # UI for DSS form and preview
│   └── logs.html          # Table view for past logs
└── static/                # (optional) static assets like CSS/JS if added
```

---

## 🚀 How to Run

### ✅ 1. Clone the Repository

```bash
git clone https://github.com/your-org/pega-dss-tool.git
cd pega-dss-tool
```

### ✅ 2. Set Up a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### ✅ 3. Install Dependencies

```bash
pip install flask requests
```

### ✅ 4. Prepare Config

Edit `config.json` to add your Pega environments:

```json
{
  "Dev": "https://dev-pega.example.com/prweb/api/v1/dss/update",
  "QA": "https://qa-pega.example.com/prweb/api/v1/dss/update",
  "mock": "https://httpbin.org/post"
}
```

### ✅ 5. Run the App

```bash
python app.py
```

Visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🔐 Security Note

Make sure you replace this line in `app.py` with a secure method in production:

```python
app.secret_key = 'your-secret-key'
```

Instead, load from an environment variable:

```python
import os
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'fallback-dev-key')
```

---

## 📖 Usage Guide

### 1. Open `http://localhost:5000`
- Select environment
- Add one or more DSS entries:
  - OwningRuleSet
  - Setting
  - Value
- See the real-time JSON preview
- Click **"🛡️ Reconfirm & Submit"** to push the data

### 2. To Test with Mock:
- Choose environment `"mock"` (or use `Send` button under "SendToMock")

### 3. To View Logs:
- Go to: [http://localhost:5000/logs](http://localhost:5000/logs)
- Shows:
  - Timestamp
  - Environment
  - DSS Payload
  - Response Status
  - Response Body (pretty-printed)

---

## 📂 Logging Format (`sent_payloads_log.jsonl`)

Each log entry is stored as a single line JSON object:

```json
{
  "timestamp": "2025-07-16T12:22:17.873378",
  "environment": "mock",
  "entries": {
    "DSSList": [
      {
        "OwningRuleSet": "abcd",
        "Setting": "wd",
        "Value": "de"
      }
    ]
  },
  "response_status": 200,
  "response_text": "{... full API response ...}"
}
```

---

## ✅ Optional Enhancements

- 🧪 Add unit tests with `pytest`
- 🔐 Secure with basic auth or login page
- 📦 Dockerize for containerized deployment
- 📧 Add email alerts on failure
- 🛡️ Integrate with Pega authentication/token APIs

---

## 🧑‍💻 Author

**Your Name / Team**  
Contact: `your.email@example.com`

---

## 📄 License

MIT License — free to use, modify, and distribute.