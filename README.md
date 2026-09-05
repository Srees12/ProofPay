# ProofPay

Evidence. Intelligence. Resolution.

Enterprise-style prototype of an AI-powered payment dispute intelligence and resolution platform.

## Live Demo

**Public deployment:** Pending deployment on Render.

Once deployed, replace the line above with the public frontend URL so judges can open ProofPay directly. The GitHub repository contains the source code and deployment configuration; the live site is hosted separately.

## One-click start on Windows

Double-click `start-proofpay.bat` after cloning the repository. It creates `.venv` if needed, installs frontend dependencies if needed, waits for both services, and opens the dashboard at `http://127.0.0.1:5173/`.

GitHub cannot directly launch a local application from a repository page. The batch file is the local one-click entrypoint after the repository has been cloned.

## Backend

```powershell
cd backend
python -m pip install -r requirements.txt
cd ..
python -m uvicorn backend.main:app --reload --port 8000
```

API docs: `http://localhost:8000/docs`

## Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open `http://127.0.0.1:5173`. The console starts in demo mode and switches to live API data when the backend is available. Set `frontend/.env` from `frontend/.env.example` to configure the API origin.

## Tests and benchmark

```powershell
python -m pytest
python -c "import asyncio; from backend.eval.benchmark import run_benchmark; print(asyncio.run(run_benchmark()))"
```

The policy guardrail is deliberately isolated from all model and network code. The current implementation uses deterministic mock tools; LiteLLM can be introduced behind the agent modules without weakening the final policy gate.

## Publish a judge-ready demo

GitHub hosts the source code; it does not run the FastAPI backend. For a clickable public demo, deploy the two services with Render using [`render.yaml`](render.yaml), or deploy the frontend to Vercel and the backend to Render.

For Render:

1. Create a new Blueprint from this repository.
2. Set `VITE_API_URL` on `proofpay-console` to the public `proofpay-api` URL, for example `https://proofpay-api.onrender.com`.
3. Set `SENTINEL_CORS_ORIGINS` on `proofpay-api` to the public frontend URL, for example `https://proofpay-console.onrender.com`.
4. Share the frontend URL with judges. They do not need to open the API URL.

The local one-click launcher remains [`start-proofpay.bat`](start-proofpay.bat). Never commit real credentials; use hosted-service environment variables for secrets and production configuration.
