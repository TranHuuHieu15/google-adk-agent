# How to Run This Project

## Step 1 — Install dependencies
Run:
```bash
uv sync
```

## Step 2 — Create the `.env` environment file
Create a file named `.env` in the project root with the following content:
```env
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=your_key
```

## Step 3 — Activate the virtual environment

### macOS / Linux
```bash
source .venv/bin/activate
```

### Windows
```powershell
.venv\Scripts\activate
```

## Final Step — Start the web app
Run:
```bash
adk web ./agents
```

The web server will start on port **8000** by default.
