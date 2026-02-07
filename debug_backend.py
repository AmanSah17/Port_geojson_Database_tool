import os
from dotenv import load_dotenv
import requests
import sys
import json

# Load env directly to verify
load_dotenv(os.path.join(os.path.dirname(__file__), "port_visualization_api", ".env"))

print("--- Environment Check ---")
secret_key = os.getenv("SECRET_KEY")
print(f"SECRET_KEY loaded: {'Yes' if secret_key else 'NO'}")

url = "http://127.0.0.1:8000/auth/google"

print("\n--- 1. Simulating Frontend POST Request (Payload + CORS) ---")
headers = {
    "Origin": "http://127.0.0.1:8081",
    "Content-Type": "application/json"
}
payload = {
    "token": "fake.jwt.token.for.testing.purposes.only"
}

try:
    print(f"POST {url}")
    r = requests.post(url, json=payload, headers=headers)
    
    print(f"Status: {r.status_code}")
    print("Headers:")
    for key, val in r.headers.items():
        if "access-control" in key.lower():
            print(f"  {key}: {val}")
        
    print(f"Body: {r.text}")
    
    if r.status_code == 400:
        print("SUCCESS: Backend handled invalid token.")
    else:
        print(f"FAILURE: Unexpected status {r.status_code}")

except Exception as e:
    print(f"POST request failed: {e}")


print("\n--- 2. Simulating CORS Preflight (OPTIONS) ---")
try:
    headers_opt = {
        "Origin": "http://127.0.0.1:8081",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type"
    }
    print(f"OPTIONS {url}")
    r_opt = requests.options(url, headers=headers_opt)
    
    print(f"Status: {r_opt.status_code}")
    print("Headers:")
    for key, val in r_opt.headers.items():
        if "access-control" in key.lower():
             print(f"  {key}: {val}")
        
    if r_opt.status_code == 200:
         print("SUCCESS: Preflight handled.")
    else:
         print(f"FAILURE: Preflight failed with {r_opt.status_code}")

except Exception as e:
    print(f"OPTIONS request failed: {e}")
