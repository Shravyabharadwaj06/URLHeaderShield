import urllib.request
import json

url = "https://api.hackertarget.com/httpheaders/?q=https://google.com"

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8')
        print(content)
except Exception as e:
    print(f"Error: {e}")
