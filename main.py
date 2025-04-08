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

--------------------
import requests
import csv
import os

# Define your environments and the API URL template
environments = ['SIT1', 'PROD', 'CANARY']
api_url_template = "http://localhost:5000/api/deployment?environment={env}"

# Function to normalize the commit ID
def extract_commit_key(commit):
    if not commit or not isinstance(commit, str):
        return "N/A"
    commit = os.path.splitext(commit)[0]  # Remove .war/.jar/.zip
    parts = commit.split('-')
    return '-'.join(parts[:-1]) if len(parts) > 1 else commit

# Collect all data: {appname: {env: commit}}
all_data = {}

for env in environments:
    try:
        url = api_url_template.format(env=env)
        response = requests.get(url)
        result = response.json()
        
        if result.get("status") == "success":
            for item in result.get("data", []):
                app = item.get("artifact", "unknown")
                commit = extract_commit_key(item.get("commit"))

                if app not in all_data:
                    all_data[app] = {}

                all_data[app][env] = commit
        else:
            print(f"No success for env {env}")
    except Exception as e:
        print(f"Failed for {env}: {e}")

# Write to CSV
with open('commit_comparison.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['appname', *environments, 'commit', 'status'])

    for app, env_data in all_data.items():
        commits = [env_data.get(env, 'N/A') for env in environments]

        # Determine if all commit keys are the same
        unique = set([c for c in commits if c != 'N/A'])
        status = "same" if len(unique) == 1 else "differ"
        final_commit = commits[0] if commits[0] != 'N/A' else next((c for c in commits if c != 'N/A'), 'N/A')

        writer.writerow([app, *commits, final_commit, status])

print("✅ Commit comparison saved to 'commit_comparison.csv'")

##################
import requests
import csv
import os

# Base environment to compare against
base_env = 'SIT2'
compare_envs = ['PROD', 'CANARY', 'PRODE']
environments = [base_env] + compare_envs

# API template
api_url_template = "http://localhost:5000/api/deployment?environment={env}"

# Function to extract comparable part of the commit
def extract_commit_key(commit):
    if not commit or not isinstance(commit, str):
        return "N/A"
    commit = os.path.splitext(commit)[0]  # Remove extension
    parts = commit.split('-')
    return '-'.join(parts[:-1]) if len(parts) > 1 else commit

# Gather data
all_data = {}

for env in environments:
    try:
        response = requests.get(api_url_template.format(env=env))
        result = response.json()

        if result.get("status") == "success":
            for item in result.get("data", []):
                app = item.get("artifact", "unknown")
                commit = extract_commit_key(item.get("commit"))

                if app not in all_data:
                    all_data[app] = {}
                all_data[app][env] = commit
    except Exception as e:
        print(f"Error fetching for {env}: {e}")

# Write to CSV
with open('commit_comparison_detailed.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    header = ['appname', *environments, *[f"{env} STATUS" for env in compare_envs]]
    writer.writerow(header)

    for app, env_data in all_data.items():
        row = [app]
        base_commit = env_data.get(base_env, 'N/A')

        # Add commit IDs
        for env in environments:
            row.append(env_data.get(env, 'N/A'))

        # Add comparison statuses
        for env in compare_envs:
            cmp_commit = env_data.get(env, 'N/A')
            status = 'same' if base_commit == cmp_commit and cmp_commit != 'N/A' else 'differ'
            row.append(status)

        writer.writerow(row)

print("✅ Detailed commit comparison written to 'commit_comparison_detailed.csv'")

