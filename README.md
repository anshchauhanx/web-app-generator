🚀 LLM Code Deployment System
An automated web application generator that receives project briefs, uses AI to generate code, deploys to GitHub Pages, and handles iterative improvements - all without manual intervention.
📋 Overview
This system acts as a bridge between project requirements and live deployments. Send a JSON request with your app requirements, and it will:

✨ Generate complete web applications using OpenAI GPT
📦 Create GitHub repositories automatically
🌐 Deploy to GitHub Pages instantly
🔄 Handle revisions and improvements (Round 2+)
📨 Notify evaluation servers with deployment details

Perfect for automated testing, rapid prototyping, or managing multiple small web projects at scale.

🎯 Features

Intelligent Code Generation: Uses GPT-5/GPT-4o to create production-ready HTML/CSS/JS applications
Automated GitHub Integration: Creates repos, commits code, and enables Pages automatically
Round-Based Improvements: Support for iterative development (Round 1: build, Round 2: enhance)
Attachment Support: Handles CSV, JSON, images, and other file attachments
Duplicate Detection: Prevents reprocessing of identical requests
Retry Logic: Robust notification system with exponential backoff
Background Processing: Non-blocking API responses for better performance


🏗️ Architecture
┌─────────────┐
│   Client    │ ──── POST /api-endpoint ────┐
└─────────────┘                             │
                                            ▼
┌──────────────────────────────────────────────────┐
│              FastAPI Server                      │
│  ┌────────────────────────────────────────────┐ │
│  │  1. Verify Secret                          │ │
│  │  2. Return HTTP 200 (immediate)            │ │
│  │  3. Queue Background Task                  │ │
│  └────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────┐
│           Background Processing                  │
│  ┌────────────────────────────────────────────┐ │
│  │  1. Decode attachments                     │ │
│  │  2. Call OpenAI GPT for code generation    │ │
│  │  3. Create/Update GitHub repo              │ │
│  │  4. Enable GitHub Pages                    │ │
│  │  5. Notify evaluation server               │ │
│  └────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
                    │
                    ├─────► GitHub Repository
                    ├─────► GitHub Pages (Live URL)
                    └─────► Evaluation Server

🚀 Quick Start
Prerequisites

Python 3.12.3+
GitHub account with Personal Access Token
OpenAI API key with GPT-5/GPT-4o access
Git installed

Installation

Clone the repository

bash   git clone https://github.com/yourusername/web-app-generator.git
   cd web-app-generator

Create virtual environment

bash   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate

Install dependencies

bash   pip install -r requirements.txt

Configure environment variables
Create a .env file in the root directory:

env   # GitHub Configuration
   GITHUB_TOKEN=ghp_your_token_here
   GITHUB_USERNAME=your_github_username
   
   # OpenAI Configuration
   OPENAI_API_KEY=sk-proj-your_key_here
   
   # Security
   USER_SECRET=your_strong_password_here

Test your setup

bash   python test_github.py
You should see:
   👤 GitHub Authenticated as: your_username
   ✅ OpenAI Authenticated. Available models: ...

Run the server

bash   uvicorn app.main:app --reload
Server will start at http://127.0.0.1:8000

📡 API Usage
Endpoint
POST /api-endpoint
Content-Type: application/json
Request Schema
json{
  "email": "user@example.com",
  "secret": "your_user_secret",
  "task": "unique-task-id",
  "round": 1,
  "nonce": "unique-request-id",
  "brief": "Create a todo list app with add, delete, and mark complete features",
  "checks": [
    "Must have input field for new todos",
    "Must have delete button for each item",
    "Must persist data in localStorage"
  ],
  "evaluation_url": "https://your-server.com/callback",
  "attachments": [
    {
      "name": "data.csv",
      "url": "data:text/csv;base64,..."
    }
  ]
}
Response
Immediate (HTTP 200):
json{
  "status": "accepted",
  "note": "processing round 1 started"
}
Later to evaluation_url (within 10 minutes):
json{
  "email": "user@example.com",
  "task": "unique-task-id",
  "round": 1,
  "nonce": "unique-request-id",
  "repo_url": "https://github.com/username/unique-task-id",
  "commit_sha": "abc123...",
  "pages_url": "https://username.github.io/unique-task-id/"
}
Example: cURL
bashcurl -X POST http://localhost:8000/api-endpoint \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "secret": "your_secret",
    "task": "todo-app-001",
    "round": 1,
    "nonce": "12345",
    "brief": "Create a simple todo list with Bootstrap styling",
    "checks": ["Must have add button", "Must have task list"],
    "evaluation_url": "https://webhook.site/your-unique-id",
    "attachments": []
  }'
Example: Python
pythonimport requests

response = requests.post("http://localhost:8000/api-endpoint", json={
    "email": "test@example.com",
    "secret": "your_secret",
    "task": "calculator-app-001",
    "round": 1,
    "nonce": "abc-123",
    "brief": "Create a calculator with +, -, *, / operations",
    "checks": ["Must have number buttons", "Must display results"],
    "evaluation_url": "https://your-callback.com/notify",
    "attachments": []
})

print(response.json())
# {"status": "accepted", "note": "processing round 1 started"}

🔄 Round-Based Development
Round 1: Initial Build

Creates new GitHub repository
Generates complete application from brief
Adds MIT License
Creates comprehensive README.md
Deploys to GitHub Pages

Round 2+: Improvements

Updates existing repository
Maintains git history
Enhances code based on new requirements
Updates README with changes
Redeploys to GitHub Pages

Example Round 2 Request:
json{
  "email": "test@example.com",
  "secret": "your_secret",
  "task": "todo-app-001",
  "round": 2,
  "nonce": "67890",
  "brief": "Add dark mode toggle and filter by completed/incomplete",
  "checks": ["Dark mode button exists", "Filter buttons work"],
  "evaluation_url": "https://your-callback.com/notify",
  "attachments": []
}

📁 Project Structure
web-app-generator/
├── app/
│   ├── __init__.py           # Package initialization
│   ├── main.py               # FastAPI app & request handling
│   ├── github_utils.py       # GitHub API operations
│   ├── llm_generator.py      # OpenAI code generation
│   ├── notify.py             # Evaluation server callbacks
│   └── signature.py          # (Future: request signing)
│
├── evaluation_tests/         # Local testing scripts
│   ├── test_round1_flow.py   # Test Round 1 complete flow
│   ├── test_round2_flow.py   # Test Round 2 updates
│   └── test_playwright_checks.py  # Browser automation tests
│
├── .env                      # Environment variables (not in git)
├── .gitignore               # Git ignore rules
├── LICENSE                  # MIT License
├── README.md                # This file
├── requirements.txt         # Python dependencies
├── runtime.txt             # Python version specification
└── test_github.py          # Setup verification script

🧪 Testing
1. Basic Setup Test
bashpython test_github.py
2. Round 1 Integration Test
bashpython evaluation_tests/test_round1_flow.py
3. Round 2 Integration Test
bashpython evaluation_tests/test_round2_flow.py
4. Browser Automation Test
bash# Install Playwright first
pip install playwright
python -m playwright install chromium

# Run tests
python evaluation_tests/test_playwright_checks.py
