import urllib.request
import urllib.error
import json
import time

class ApiClient:
    def __init__(self, base_url="http://localhost:8080/api"):
        self.base_url = base_url

    def request(self, method, endpoint, data=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        if headers is None:
            headers = {}
        
        headers['Content-Type'] = 'application/json'
        
        encoded_data = None
        if data:
            encoded_data = json.dumps(data).encode('utf-8')

        req = urllib.request.Request(url, data=encoded_data, headers=headers, method=method)
        
        try:
            with urllib.request.urlopen(req) as response:
                if response.status >= 200 and response.status < 300:
                    if response.status != 204: # No content
                        return json.loads(response.read().decode())
                    return {}
                return None
        except urllib.error.HTTPError as e:
            # 400 often means already exists in our API, allow caller to handle
            if e.code != 400:
                print(f"Request failed: {e.code} {e.reason} for {url}")
            return None
        except Exception as e:
            print(f"Connection error: {e}")
            return None
