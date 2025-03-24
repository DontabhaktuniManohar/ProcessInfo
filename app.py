# save this as client.py

import requests

def get_first_blue_object(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        if "list" in data and isinstance(data["list"], list):
            blue_item = next((item for item in data["list"] if item.get("bgflag") == "Blue"), None)
            return blue_item
        else:
            print("No 'list' found in response or 'list' is not a list.")
            return None

    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return None
    except ValueError as e:
        print(f"Invalid JSON response: {e}")
        return None

if __name__ == "__main__":
    api_url = "http://127.0.0.1:5000/api/deployment"
    result = get_first_blue_object(api_url)

    if result:
        print("First object with bgflag as 'Blue':")
        print(result)
    else:
        print("No object found with bgflag as 'Blue'")
