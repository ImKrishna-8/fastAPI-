from fastapi import FastAPI, WebSocketDisconnect
from fastapi.websockets import WebSocket

app = FastAPI()

class ConnectionManager():
     
    def __init__(self):
        self.active_connection = []

    async def connect(self,websocket:WebSocket):
        await websocket.accept()
        self.active_connection.append(websocket)
    
    async def disconnect(self,websocket:WebSocket):
         self.active_connection.remove(websocket)

    async def broadcast(self,msg:str):
         for connection in self.active_connection:
              await connection.send_text(msg)
            

manager = ConnectionManager()

@app.websocket('/ws')
async def websocket_endpoint(websocket:WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        print("client Disconnected")
    
