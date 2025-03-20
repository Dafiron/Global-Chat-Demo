#Importacion Externa // External Import
from fastapi import WebSocket
import pymysql

#Variables de entorno // Environment variables
from dotenv import load_dotenv
import os

load_dotenv()

sql_pass = os.getenv("db_sql_password")
sql_user = os.getenv("db_sql_user")
sql_host = os.getenv("db_sql_host")
sql_port = os.getenv("db_sql_port")
sql_database = os.getenv("db_sql_database")

def get_sql_connection():
    try:
        connection = pymysql.connect(
            host=sql_host,
            port=int(sql_port),
            user=sql_user,
            password=sql_pass,
            database=sql_database,
            connect_timeout=10,
            cursorclass=pymysql.cursors.DictCursor  # Opcional: devuelve los resultados como diccionarios // Optional: Returns results as dictionaries
        )
        return connection
    except pymysql.MySQLError as err:
        if err.args[0] == 1045:  # Código de error para acceso denegado // Error code for access denied
            print("Error: Usuario o contraseña incorrectos.")
        elif err.args[0] == 1049:  # Código de error para base de datos no existente // Error code for non-existent database
            print("Error: La base de datos no existe.")
        else:
            print(f"Error inesperado: {err}")
        raise


class ConnectionManager:
    def __init__(self):
        self.active_connection = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connection[websocket] = user_id
        print(f"Usuario {user_id} conectado.")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connection:
            user_id = self.active_connection[websocket]
            del self.active_connection[websocket]
            print(f"Usuario {user_id} desconectado.")

    async def broadcast(self, message:str ):
        for connection in self.active_connection:
            await connection.send_text(message)
