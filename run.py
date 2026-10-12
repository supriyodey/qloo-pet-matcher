import uvicorn
import os
import sys

if __name__ == "__main__":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    port = int(os.getenv("PORT", 8080))
    print(f"Starting PawVibe server on http://localhost:{port}")
    uvicorn.run("app:app", host="127.0.0.1", port=port, reload=False)

