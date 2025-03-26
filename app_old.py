import requests

def get_first_blue_object(api_url):
    try:
        response = requests.get(api_url, stream=True)  # stream=True to reduce memory if huge JSON
        response.raise_for_status()
        data = response.json()

        items = data.get("list", [])

        # Use a manual loop instead of generator for better control (tiny improvement)
        for item in data:
            if item["bgflag"] == "Blue" and item["deployby"] == "raj":
                return item

        return None

    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return None
    except ValueError as e:
        print(f"Invalid JSON response: {e}")
        return None

if __name__ == "__main__":
    api_url = "http://127.0.0.1:5000/api/deployment?bgflag=Blue&deployby=raj"
    result = get_first_blue_object(api_url)

    if result:
        print("First object with bgflag as 'Blue' and deployby as 'raj':")
        print(result)
    else:
        print("No object found with bgflag as 'Blue' and deployby as 'raj'")
