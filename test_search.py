import urllib.request
import json
import sys
import time

def test_search():
    url = "http://127.0.0.1:8000/search"
    payload = {"query": "What is Playwright python?"}
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    # Retry logic for server startup
    for i in range(10):
        try:
            print(f"Attempt {i+1} to connect...")
            with urllib.request.urlopen(req, timeout=60) as response:
                if response.status == 200:
                    body = response.read().decode('utf-8')
                    json_response = json.loads(body)
                    if "html_content" in json_response and len(json_response["html_content"]) > 0:
                        print("Test Passed: Received HTML content.")
                        print(f"Content preview: {json_response['html_content'][:200]}")
                        return
                    else:
                        print("Test Failed: Response missing 'html_content' or empty.")
                        sys.exit(1)
                else:
                    print(f"Test Failed: Status Code {response.status}")
                    sys.exit(1)
        except Exception as e:
            print(f"Connection failed: {e}")
            time.sleep(2)
    
    print("Test Failed: Could not connect to server after multiple attempts.")
    sys.exit(1)

if __name__ == "__main__":
    test_search()
