import requests
import json

def test_analyze():
    url = "http://127.0.0.1:8000/analyze/"
    payload = {"url": "google.com"}
    print(f"Sending POST request to {url} with payload {payload}...")
    try:
        response = requests.post(url, json=payload, timeout=15)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_analyze()
