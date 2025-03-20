#Importaciones Internas // Internals Imports
from DB.client import get_sql_connection

#Variables de entorno // Environment variables
from dotenv import load_dotenv
import os

load_dotenv()

def generate_html(user_id: int) -> str:
    return f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Websocket chat Demo</title>
            <!-- Bootstrap CSS -->
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-3">
                <h1>Websocket chat Demo</h1>
                <h2>Your ID: <span id="ws-id">{user_id}</span></h2>
                <form action="" onsubmit="sendMessage(event)">
                    <input type="text" class="form-control" id="messageText" autocomplete="off"/>
                    <button class="btn btn-outline-primary mt-2">Send</button>
                </form>
                <ul id='messages' class="mt-5"></ul>
            </div>
            <script>
                var ws = new WebSocket(`ws://localhost:8000/ws/{user_id}`);
                ws.onmessage = function(event) {{
                    var messages = document.getElementById('messages');
                    var message = document.createElement('li');
                    var content = document.createTextNode(event.data);
                    message.appendChild(content);
                    messages.appendChild(message);
                }};
                function sendMessage(event) {{
                    var input = document.getElementById("messageText");
                    ws.send(input.value);
                    input.value = '';
                    event.preventDefault();
                }}
            </script>
        </body>
    </html>
    """

USERS = {}

list_env_var=[
    "db_sql_database","db_sql_host", "db_sql_user","on_dev","db_sql_password",
    ]

def check_environment_variables(required_vars: list):
    """
    ES:Verifica si las variables de entorno requeridas están definidas.
    :param required_vars: Lista de nombres de las variables de entorno requeridas.
    EN: Checks if the required environment variables are defined.
    :param required_vars: List of names of the required environment variables.
    """
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise EnvironmentError(
            f"The following environment variables are missing: {', '.join(missing_vars)}"
        )
    print("*---All Environment Variables its OK.---*")


def is_connected():
    """
    ES: Verificar Conexion con Base de datos.
    si esta OK: lanza por terminal: Successful connection to the database.
    si no esta OK: Error connecting to database: {error espesifico}
    EN: Check Database Connection
    If it's OK: launch the terminal: Successful connection to the database.
    If it's not OK: Error connecting to database: {specific error}
    """
    try:
        connection = get_sql_connection()
        print("Successful connection to the database.")
        connection.close()
    except Exception as e:
        print(f"Error connecting to database: {e}")


