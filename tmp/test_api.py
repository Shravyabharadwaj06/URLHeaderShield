import requests
import json

def test_analyze():
    url = "http://127.0.0.1:8000/analyze/"
    payload = {"url": "google.com"}
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_analyze()
