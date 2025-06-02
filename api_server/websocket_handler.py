from fastapi import WebSocket
from agent.core import execute_agent
import asyncio

async def handle_websocket_chat(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            user_msg = await websocket.receive_text()

            response = await execute_agent(user_msg)

            # send response in chunks
            chunk_size = 200
            for i in range(0, len(response), chunk_size):
                await websocket.send_text(response[i:i+chunk_size])
                await asyncio.sleep(0.01)

        except Exception as e:
            await websocket.send_text(f"error: {str(e)}")
            await websocket.close()
            break
