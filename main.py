import requests
import pandas as pd

# API URL
API_URL = "http://127.0.0.1:5000/api/deployment"

# List of environments to compare
environments = ["SIT1", "SIT2", "SIT3", "SIT4", "SIT5", "PROD", "CANARY", "PRODE"]

# Fetch data from API
response = requests.get(API_URL)
data = response.json()  # Assuming API returns {"status": "success", "data": [...]}

# if data.get("status") != "success" or "data" not in data:
#     print("Error fetching data from API")
#     exit()

# Convert response data into a dictionary for easy lookup
env_commit_map = {}

for item in data:
    env = item["environment"]
    commit = item["commit"]
    env_commit_map[env] = commit

# Create a table to compare commits
table_data = []
base_commit = env_commit_map.get("SIT1", "N/A")  # Use SIT1 as a reference for comparison

for env in environments:
    commit = env_commit_map.get(env, "N/A")
    status = "Same" if commit == base_commit else "Different"
    table_data.append([env, commit, status])

# Convert to DataFrame for better visualization
df = pd.DataFrame(table_data, columns=["Environment", "Commit", "Status"])
print(df.to_string(index=False))  # Print table without index

###########################
import requests
import pandas as pd

# API URL (Replace with actual API endpoint)
API_URL_TEMPLATE = "http://your-api-endpoint.com/api/deployment?environment={env}"

# List of environments to compare
environments = ["SIT1", "SIT2", "SIT3", "SIT4", "SIT5", "PROD", "CANARY", "PRODE"]

# Dictionary to store commit values
env_commit_map = {}

# Fetch commit data for each environment
for env in environments:
    api_url = API_URL_TEMPLATE.format(env=env)
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "success" and "data" in data and len(data["data"]) > 0:
            env_commit_map[env] = data["data"][0]["commit"]  # Only first record needed
        else:
            env_commit_map[env] = "N/A"
    else:
        env_commit_map[env] = "Error"

# Reference commit (SIT1)
base_commit = env_commit_map.get("SIT1", "N/A")

# Prepare table data
table_data = []
for env in environments:
    commit = env_commit_map[env]
    status = "Same" if commit == base_commit else "Different"
    table_data.append([env, commit, status])

# Convert to DataFrame and display results
df = pd.DataFrame(table_data, columns=["Environment", "Commit", "Status"])
print(df.to_string(index=False))  # Print table without index
###############################################
###############################################
###############################################
import requests
import pandas as pd

# API URL Template (Replace with actual API endpoint)
API_URL_TEMPLATE = "http://your-api-endpoint.com/api/deployment?environment={env}"

# List of environments to compare
environments = ["SIT1", "SIT2", "SIT3", "SIT4", "SIT5", "PROD", "CANARY", "PRODE"]

# Dictionary to store commit values
env_commit_map = {}

# Function to extract meaningful commit ID (ignoring last part)
def extract_commit_key(commit):
    parts = commit.split('-')
    return '-'.join(parts[:2]) if len(parts) >= 2 else commit  # Keep only first 2 parts

# Fetch commit data for each environment
for env in environments:
    api_url = API_URL_TEMPLATE.format(env=env)
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "success" and "data" in data and len(data["data"]) > 0:
            original_commit = data["data"][0]["commit"]  # Only first record needed
            env_commit_map[env] = extract_commit_key(original_commit)
        else:
            env_commit_map[env] = "N/A"
    else:
        env_commit_map[env] = "Error"

# Reference commit (SIT1)
base_commit = env_commit_map.get("SIT1", "N/A")

# Prepare table data
table_data = []
for env in environments:
    commit = env_commit_map[env]
    status = "Same" if commit == base_commit else "Different"
    table_data.append([env, commit, status])

# Convert to DataFrame and display results
df = pd.DataFrame(table_data, columns=["Environment", "Commit (Prefix)", "Status"])
print(df.to_string(index=False))  # Print table without index

