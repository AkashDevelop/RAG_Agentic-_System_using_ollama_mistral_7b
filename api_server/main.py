from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn
import os

from api_server.websocket_handler import handle_websocket_chat  # updated import

app = FastAPI()

# WebSocket endpoint
@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await handle_websocket_chat(websocket)

# Health check
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

# Serve frontend
if os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
else:
    print(" Warning: 'frontend' directory not found. StaticFiles not mounted.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
