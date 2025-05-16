{
  "A_GROUP": {
    "APP1": ["subapp1", "subapp2"],
    "APP2": ["subapp1", "subapp3"]
  },
  "B_GROUP": {
    "APP1": ["subapp3", "subapp4"],
    "APP2": ["subapp4", "subapp5"]
  }
}
import json

def load_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def get_subapps(data, group, app):
    try:
        subapps = data[group][app]
        print(f"Subapps in {group} > {app}: {subapps}")
        return subapps
    except KeyError:
        print(f"❌ Invalid group '{group}' or app '{app}'")
        return []

if __name__ == "__main__":
    # Load JSON data
    data = load_data("apps.json")

    # Get user input (or hardcode for test)
    group = input("Enter group name (e.g., A_GROUP): ").strip()
    app = input("Enter app name (e.g., APP1): ").strip()

    # Get and display subapps
    get_subapps(data, group, app)

