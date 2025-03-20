"""            Demo-chat              """


#Importacion Externa // External Import
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

#Importacion Interna // Internal Import
from DB.client import ConnectionManager
from Components.Constants import generate_html, USERS, is_connected, check_environment_variables, list_env_var
from Components.Querys import search_user, save_message, get_messages

#Variables de entorno // Environment variables
from dotenv import load_dotenv
import os

load_dotenv()


app = FastAPI(
    title= "Demo-chat",
    version="0.1 BETA",
    description= "demostración de chat con websocket",
    docs_url="/docs" if os.getenv("on_dev") == "Y" else None,
    redoc_url="/redoc" if os.getenv("on_dev") == "Y" else None,
    openapi_url="/openapi.json" if os.getenv("on_dev") == "Y" else None,
)

check_environment_variables(list_env_var)

is_connected()

manager = ConnectionManager()

@app.get("/")
async def root():
    """
    ES:Responde un modelo html utilizado para ejemplo de uso. Resaltar que el id del usuario predeterminado es el 1 quien es de rol Cliente
    EN:
    """
    return HTMLResponse(generate_html(1))

@app.get("/2")
async def root_2():
    """
    ES: Responde un modelo html utilizado para ejemplo de uso. Resaltar que el id del usuario predeterminado es el 2 quien es de rol Vendedor
    EN: 
    """
    return HTMLResponse(generate_html(2))


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket:WebSocket, user_id:int):
    if user_id in USERS:
        user_data = USERS[user_id]
    else:
        res = search_user(user_id)
        if res:
            USERS[user_id] = res  # Almacenar en caché usando el ID como clave // Caching using the ID as a key
            user_data = res
        else:
            raise WebSocketDisconnect(
                code=1000,
                reason="Unable to bind connection to database"
            )
    username = user_data["username"]
    rol = user_data["rol"]

    await manager.connect(websocket,user_id)

    messages = get_messages()
    for msg in messages:
        formatted_message = f"{msg['username']} ({'Client' if msg['rol'] == 0 else 'Seller'}): {msg['message']}"
        await websocket.send_text(formatted_message)

    await manager.broadcast(f"({'Client' if rol == 0 else 'Seller'}) {username} has joined the chat")

    try:
        while True:
            data = await websocket.receive_text()

            # Guardar el mensaje en la base de datos //Save the message to the database
            save_message(user_id, data)

            # Formatear el mensaje // Format the message
            formatted_message = f"{username} ({'Client' if rol == 0 else 'Seller'}): {data}"

            # Difundir el mensaje a todos los clientes // Spread the message to all customers
            await manager.broadcast(formatted_message)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"({'Client' if rol == 0 else 'Seller'}) {username} has left the chat")



