
# 📘 Commit Comparison Report Tool

A Python-based tool to **compare artifact versions across environments** and generate a **color-coded HTML report** showing which deployments are in sync and which differ. Optional timestamps provide deployment history context.

## 🚀 Features

- ✅ CLI-like argument parsing (e.g., `group=myapp base_env=dev flag=blue`)
- ✅ Compares artifacts across `dev-blue`, `dev-green`, `stage`, `prod`
- ✅ Outputs a beautiful HTML report
- ✅ Shows `SAME` (🟢), `DIFF` (🔴), `BASE`, and `N/A`
- ✅ Optionally shows deployment timestamps
- ✅ Customizable environment expansion (e.g., blue/green split)

## 📦 Project Structure

```
project/
├── main.py
├── input.json
├── utils.py
├── comparison_report.html
└── README.md
```

## 🧰 Requirements

- Python 3.6+
- `requests`

Install with:

```bash
pip install requests
```

## 🧾 Example Usage

```bash
python main.py group=myapp base_env=dev flag=blue timestamp=true
```

## 📄 Input JSON Format

```json
{
  "myapp-blue": {
    "dev-blue": { "artifact": "abc123", "deploymenttime": "1716102000000" }
  },
  "myapp-green": {
    "dev-green": { "artifact": "abc456", "deploymenttime": "1716102100000" }
  },
  "myapp": {
    "stage": { "artifact": "abc123", "deploymenttime": "1716102200000" },
    "prod": { "artifact": "abc789", "deploymenttime": "1716102300000" }
  }
}
```

## 🎨 HTML Output Example

| APP NAME   | dev-blue     | dev-green (BASE) | stage         | prod          |
|------------|--------------|------------------|----------------|----------------|
| myapp      | abc123 🟢     | abc123 🔵         | abc123 🟢       | abc789 🔴       |

🕒 Timestamp shown below each value if `timestamp=true` is passed.

## 📥 Output

- A file named `commit_comparison_report.html` is generated.
- You can open it in any browser.

## ⚙️ CLI Parameters

| Param         | Description                                      | Example         |
|---------------|--------------------------------------------------|-----------------|
| `group`       | Group name or app identifier                     | `myapp`         |
| `base_env`    | Base environment name (e.g., `dev`)              | `dev`           |
| `flag`        | Flag to distinguish blue/green environments      | `blue` or `green` |
| `timestamp`   | Show deployment timestamp (`true`/`false`)       | `true`          |
