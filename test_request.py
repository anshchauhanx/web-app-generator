import requests
import json

# Replace this with YOUR secret from .env file
USER_SECRET = "ansh2014"

# This is test data
data = {
    "secret": USER_SECRET,
    "email": "your-email@example.com",
    "task": "my-test-app-001",
    "brief": "Create a simple HTML page with a blue heading that says 'Hello World' and a button that shows an alert when clicked",
    "round": 1,
    "nonce": "test-12345",
    "evaluation_url": "https://webhook.site/#!/view/your-unique-id",  # Optional: Get a real URL from webhook.site
    "checks": [
        "Must have a heading",
        "Must have a button",
        "Button must be interactive"
    ],
    "attachments": []
}

print("📤 Sending request to local server...")
print(f"Task: {data['task']}")
print(f"Brief: {data['brief']}")
print("-" * 50)

try:
    response = requests.post(
        "http://127.0.0.1:8000/api-endpoint",
        json=data,
        timeout=10
    )
    
    print(f"\n✅ Status Code: {response.status_code}")
    print(f"📨 Response:")
    print(json.dumps(response.json(), indent=2))
    
    if response.status_code == 200:
        print("\n🎉 SUCCESS! Your server accepted the request.")
        print("⏳ It's now processing in the background...")
        print("📂 Check your GitHub account in a few minutes for a new repo!")
        print(f"   Repo name will be: {data['task']}")
        
except requests.exceptions.ConnectionError:
    print("\n❌ ERROR: Cannot connect to server!")
    print("Make sure the server is running:")
    print("   uvicorn app.main:app --reload")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")