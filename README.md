# Índice

**Nota**: Este documento está disponible en español (ES) e inglés (EN). Usa el índice para navegar entre las versiones.

---

## ES (Español)

1. [Descripción](#descripción)
2. [Tecnologías](#tecnologías)
3. [Bases de Datos](#bases-de-datos)
   - 3.1. [Esquema](#esquema)
   - 3.2. [Tabla `users`](#tabla-users)
   - 3.3. [Tabla `messages`](#tabla-messages)
4. [Endpoints](#endpoints)
   - 4.1. [`/telegram-webhook` (POST)](#telegram-webhook-post)
   - 4.2. [`/ws/{user_id}` (WebSocket)](#ws-user_id-websocket)
5. [Funcionamiento del Chat](#funcionamiento-del-chat)
6. [Variables de Entorno](#variables-de-entorno)
7. [Licencias](#licencias)

---

## EN (English)

1. [Description](#description)
2. [Technologies](#technologies)
3. [Database](#database)
   - 3.1. [Schema](#schema)
   - 3.2. [Table `users`](#table-users)
   - 3.3. [Table `messages`](#table-messages)
4. [Endpoints](#endpoints-en)
   - 4.1. [`/telegram-webhook` (POST)](#telegram-webhook-post-en)
   - 4.2. [`/ws/{user_id}` (WebSocket)](#ws-user_id-websocket-en)
5. [Chat Functionality](#chat-functionality)
6. [Environment Variables](#environment-variables)
7. [Licenses](#licenses-en)


## ES (Español)
### Descripción
Chat en simultaneo, global y en linea, para multiples usuarios previamente registrados.

Su desarrollo fue en el lenguaje Python, bajo la tecnologia de Fastapi, se opto por una base de datos Relacional, y el protocolo Websocket.

### Tecnologías / Technologies
- **Backend**: FastAPI (Python)
- **Base de Datos**: MySQL
- **Protocolo**: Websocket

### Bases de Datos

La Base de Datos fue confeccionada en MySQL, para garantizar la persistencia de los mensajes asi como la legitimidad de los usuarios del chat.

#### SCHEMA

#### Tabla `users`


| Columna       | Tipo         | Descripción / Description                          |
|---------------|--------------|----------------------------------------------------|
| id_user       | INT          | PK, NN, AI (Primary Key, Not Null, Auto Increment) |
| username      | VARCHAR(80)  | NN, UQ (Not Null, Unique)                          |
| rol           | INT          | NN (0: Cliente, 1: Vendedor)                       |
| disabled      | BOOLEAN      | NN (default: False)                                |
| phone         | VARCHAR(45)  | NN (default: "XXX-XXXXXXX")                        |
| email         | VARCHAR(80)  | NN, UQ                                             |
| password      | VARCHAR(120) | NN (hashed con bcrypt)                             |

#### Tabla `messages`

| Columna             | Tipo    | Descripción / Description                  |
|---------------------|---------|--------------------------------------------|
| id_message          | INT     | PK, AI (PRIMARY, KEY AUTO_INCREMENT)       |
| id_user             | INT     | NN (NOT NULL, FK= users.id_user)           |
| message             | TEXT    | NN (NOT NULL)                              |
| timestamp           |DATETIME | NN (NOT NULL, DEFAULT = CURRENT_TIMESTAMP) |


### Documentación Específica

Fastapi en su uso y coperacion con la tecnologia de Swagger UI nos facilita una documentación resumida y ordenada en {url_de_despliegue}/docs
o la opccion de ReDoc {url_de_despliegue}/redoc

### Endpoints 

#### **/** (GET)
- **Descripción:** Responde un modelo html utilizado para ejemplo de uso. Resaltar que el id del usuario predeterminado es el 1 quien es de rol Cliente
- **Responses:** plantilla html

#### **/2** (GET)
- **Descripción:** Responde un modelo html utilizado para ejemplo de uso. Resaltar que el id del usuario predeterminado es el 2 quien es de rol Vendedor
- **Responses:** plantilla html

#### **/ws/{user_id}** (websocket)
- **Descripción:** Este endpoint permite la comunicación en tiempo real entre clientes conectados.
- **Parámetros:**
  - `user_id`: Identificador único del usuario que se conecta al WebSocket.
- **Eventos:**
  - **Mensaje recibido:** `{username} (Client/Seller): {message}`
  - **Usuario conectado:** `(Client/Seller) {username} has joined the chat`
  - **Usuario desconectado:** `(Client/Seller) {username} has left the chat`


### Funcionamiento


Al ingresar en el chat el consulta al chache si el id esta vinculado a un usuario que ya haya ingresado recientemente.

de lo contrario consulta a base de datos si el usuario existe.

- si este no exite: Se te desconeca con el codigo 1000, detalle:"Unable to bind connection to database"

Se procede ha hacer la conexion, avisando por terminal de su conexion.

Se traen todo los mensajes en base de datos. (garantizando de esta forma la persistencia)

Al final del historial del chat se envia el mensaje "({rol}) {username} has joined the chat" señalando a todos en el chat de su conexion.

Cada mensaje que este envie o resiba tiene el siguiente formato: "{username} ({rol}): {mensaje}"

Ante la desconexion se notifica por terminal, y se envia un mensaje al global: "({rol}) {username} has left the chat"

Finalizando el bucle.


### Variables de Entorno
Crea un archivo `.env` con:
    ```env
    db_sql_database={NOMBRE_DE_LA_DATABASE}
    db_sql_host={HOST}
    db_sql_port={PUERTO}
    db_sql_password={CONTRASEÑA}
    db_sql_user={USUARIO}

    on_dev="Y" (O "N" EN CASO DE ESTAR EN PRODUCCION)

### Ejecucion

#### Entorno Local

1. Se recomienda ejecutar el proyecto en un entorno virtual para evitar conflictos con otras dependencias del sistema.

Si no tienes un entorno virtual configurado, puedes crearlo y activarlo con los siguientes comandos:
Crear un entorno virtual (si no lo tienes)
    python -m venv venv

Activar el entorno virtual
En Windows:
    venv\Scripts\activate

En Linux/Mac:
    source venv/bin/activate

elemplo en termial:
{ubicado en raiz del proyecto}>python -m venv venv
{ubicado en raiz del proyecto}>venv\Scripts\activate
(venv) {ubicado en raiz del proyecto}>

2. Instalación de dependencias:
    pip install -r requirements.txt

3. Inicio del servidor

comando de inicio del servidor:

{ubicado en raiz del proyecto}> uvicorn main:app --host 0.0.0.0 --port 8000 --reload


El archivo main.py contiene dos funciones importantes que verifican el entorno antes de iniciar el servidor:

4. Verificación del entorno
check_environment_variables()
    verifica que todas las variables de entorno esten correctamente definidas:
        - respuesta positiva: *---All Environment Variables its OK.---*
        - respuesta negativa: The following environment variables are missing: XXX, ZZZ, YYY

5. Verifica la conexión a la base de datos
is_connected()
    verifica la conexion a base de datos (en este caso mysql) 
        - respuesta positiva: Conexión exitosa a la base de datos
        - respuesta negativa: Error connecting to database:{error espesifico} 


6. Ejemplo de salida en la terminal
ejemplo de vision en terminal:
INFO:     Will watch for changes in these directories: ['{ubicado en raiz del proyecto}']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [14632] using WatchFiles
*---All Environment Variables its OK.---* 
Successful connection to the database.
INFO:     Started server process [14040]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

Una vez que el servidor esté en funcionamiento, puedes acceder a la API en tu navegador o mediante herramientas como curl o Postman o Thunder Client:

URL base: http://localhost:8000

y si la variable de entorno 'on_dev' == "Y":

Documentación interactiva (Swagger UI): http://localhost:8000/docs 

Documentación alternativa (ReDoc): http://localhost:8000/redoc

De lo contrario, es decir: 'on_dev' != "Y"

no sera visible; esto es espacialmente util para el despliegue del proyecto.

7. Cierre

Para cerrar el servidor: presione CTRL+C

y el entorno virtual: en la terminal que este sindo ejecutado: (venv) {ubicado en raiz del proyecto}> deactivate

### Licencias
- **Este proyecto**: MIT License (ver [LICENSE](LICENSE.md)).
- **Dependencias**: Ver [LICENSES.md](LICENSES.md).

### Comandos de creacion de Base de datos

#### Iniciar MySQL
mysql -u root -p

#### Crear el esquema
CREATE DATABASE IF NOT EXISTS chat_web;
USE chat_web;

#### Crear la tabla users
    
    ```SQL

    CREATE TABLE IF NOT EXISTS users (
        id_user INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(80) NOT NULL UNIQUE,
        rol INT NOT NULL DEFAULT 0,
        disabled BOOLEAN NOT NULL DEFAULT FALSE,
        phone VARCHAR(45) NOT NULL DEFAULT 'XXX-XXXXXXX',
        email VARCHAR(80) NOT NULL UNIQUE,
        password VARCHAR(120) NOT NULL
    );

#### Insertar usuarios

    ```SQL

    INSERT INTO users (username, rol, disabled, phone, email, password)
    VALUES 
    ('client_test', 0, 0, 'XXX-XXXXXXX', 'client_test@gmail.com', '$2b$12$iMNZkfrRAk3X53IFP6hnL.Qfv8GM8Q4/cnBvuiE1SQw0ebnlvmtSK'),
    ('seller_test', 1, 0, 'XXX-XXXXXXX', 'seller_test@gmail.com', '$2b$12$o9KM9nbujuBN2dadYJrme.nPvvZHecLtxWQMKjEHSl68upsTDmwSS');


#### Crear la tabla messages

    ```SQL

    CREATE TABLE IF NOT EXISTS messages (
        id_message INT AUTO_INCREMENT PRIMARY KEY,
        id_user INT NOT NULL,
        message TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_user) REFERENCES users(id_user)
    );

#### Insertar un mensaje de prueba

    ```SQL

    INSERT INTO messages (id_user, message)
    VALUES (1, 'Este es un mensaje de prueba del cliente.');

## EN (English)
### Description
Simultaneous, global, online chat for multiple pre-registered users.

Developed in Python, using Fastapi technology, we opted for a relational database and the Websocket protocol.

### Technologies
- **Backend**: FastAPI (Python)
- **Database**: MySQL
- **Protocol**: Websocket

### Databases

The database was built in MySQL to ensure message persistence and the legitimacy of chat users.

#### SCHEMA

#### `users` Table


| Columna       | Tipo         | Descripción / Description                          |
|---------------|--------------|----------------------------------------------------|
| id_user       | INT          | PK, NN, AI (Primary Key, Not Null, Auto Increment) |
| username      | VARCHAR(80)  | NN, UQ (Not Null, Unique)                          |
| rol           | INT          | NN (0: Cliente, 1: Vendedor)                       |
| disabled      | BOOLEAN      | NN (default: False)                                |
| phone         | VARCHAR(45)  | NN (default: "XXX-XXXXXXX")                        |
| email         | VARCHAR(80)  | NN, UQ                                             |
| password      | VARCHAR(120) | NN (hashed con bcrypt)                             |


#### `messages` Table

| Columna             | Tipo    | Descripción / Description                  |
|---------------------|---------|--------------------------------------------|
| id_message          | INT     | PK, AI (PRIMARY, KEY AUTO_INCREMENT)       |
| id_user             | INT     | NN (NOT NULL, FK= users.id_user)           |
| message             | TEXT    | NN (NOT NULL)                              |
| timestamp           |DATETIME | NN (NOT NULL, DEFAULT = CURRENT_TIMESTAMP) |

### Specific Documentation

Fastapi, in its use and cooperation with Swagger UI technology, provides summarized and organized documentation in {deployment_url}/docs
or the ReDoc option {deployment_url}/redoc

### Endpoints

#### **/** (GET)
- **Description:** Responds to an HTML template used for usage examples. Note that the default user ID is 1, which is the Client role.
- **Responses:** HTML template

#### **/2** (GET)
- **Description:** Responds to an HTML template used for usage examples. Note that the default user ID is 2, which is the Seller role.
- **Responses:** HTML template

#### **/ws/{user_id}** (websocket)
- **Description:** This endpoint enables real-time communication between connected clients.
- **Parameters:**
- `user_id`: Unique identifier of the user connecting to the WebSocket.
- **Events:**
- **Message received:** `{username} (Client/Seller): {message}`
- **User connected:** `(Client/Seller) {username} has joined the chat`
- **User disconnected:** `(Client/Seller) {username} has left the chat`

### How it Works

When you enter the chat, the chat queries the cache to see if the ID is linked to a user who has recently logged in.

Otherwise, it queries the database to see if the user exists.

If the user doesn't exist, you are disconnected with code 1000, detailing: "Unable to bind connection to database."

The connection is established, notifying the terminal of your connection.

All messages are retrieved from the database (thus ensuring persistence).

At the end of the chat history, the message "({role}) {username} has joined the chat" is sent, notifying everyone in the chat of your connection.

Each message sent or received has the following format: "{username} ({role}): {message}"

Upon disconnection, a notification is sent to the terminal, and a message is sent to the global server: "({role}) {username} has left the chat"

Ending the loop.

### Environment Variables
Create a `.env` file with:
    ```env

    db_sql_database={DATABASE_NAME}
    db_sql_host={HOST}
    db_sql_port={PORT}
    db_sql_password={PASSWORD}
    db_sql_user={USER}

    on_dev="Y" (OR "N" IF IN PRODUCTION)

### Execution

#### Local Environment

1. It is recommended to run the project in a virtual environment to avoid conflicts with other system dependencies.

If you don't have a virtual environment configured, you can create and activate it with the following commands:
Create a virtual environment (if you don't have one)
python -m venv venv

Activate the virtual environment
On Windows:
venv\Scripts\activate

On Linux/Mac:
source venv /bin/activate

Terminal example:
{located in project root}> python -m venv venv
{located in project root}> venv\Scripts\activate
(venv) {located in project root}>

2. Installing dependencies:
pip install -r requirements.txt

3. Starting the server

Server startup command:

{located in project root}> uvicorn main:app --host 0.0.0.0 --port 8000 --reload

The main.py file contains two important functions that check the environment before starting the server:

4. Environment Check
check_environment_variables()
Verifies that all environment variables are correctly defined:
- Positive response: *---All Environment Variables are OK.---*
- Negative response: The following environment variables are missing: XXX, ZZZ, YYY

5. Check the database connection
is_connected()
Verifies the database connection (in this case, MySQL)
- Positive response: Successful connection to the database
- Negative response: Error connecting to database: {specific error}

6. Terminal Output Example
Terminal output example:
INFO: Will watch for changes in these directories: ['{located in project root}']
INFO: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO: Started reloader process [14632] using WatchFiles
*---All Environment Variables are OK OK.---*
Successful connection to the database.
INFO: Started server process [14040]
INFO: Waiting for application startup.
INFO: Application startup complete.

Once the server is up and running, you can access the API in your browser or using tools like curl, Postman, or Thunder Client:

Base URL: http://localhost:8000

And if the environment variable 'on_dev' == "Y":

Interactive documentation (Swagger UI): http://localhost:8000/docs

Alternative documentation (ReDoc): http://localhost:8000/redoc

Otherwise, i.e., 'on_dev' != "Y"

It will not be visible; this is especially useful for project deployment.

7. Shutdown

To shut down the server: press CTRL+C

and the virtual environment: in the terminal where it's running: (venv) {located in the project root} > deactivate

### Licenses
- **This project**: MIT License (see [LICENSE](LICENSE.md)).
- **Dependencies**: See [LICENSES.md](LICENSES.md).

### Database Creation Commands

#### Start MySQL
mysql -u root -p

#### Create the Schema

    ```SQL

    CREATE DATABASE IF NOT EXISTS chat_web;
    USE chat_web;

#### Create the users table

    ```SQL

    CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    role INT NOT NULL DEFAULT 0,
    disable BOOLEAN NOT NULL DEFAULT FALSE,
    phone VARCHAR(45) NOT NULL DEFAULT 'XXX-XXXXXXX',
    email VARCHAR(80) NOT NULL UNIQUE,
    password VARCHAR(120) NOT NULL
    );

#### Insert users

    ```SQL
    INSERT INTO users (username, role, disabled, phone, email, password)
    VALUES
    ('client_test', 0, 0, 'XXX-XXXXXXX', 'client_test@gmail.com', '$2b$12$iMNZkfrRAk3X53IFP6hnL.Qfv8GM8Q4/cnBvuiE1SQw0ebnlvmtSK'),
    ('seller_test', 1, 0, 'XXX-XXXXXXX', 'seller_test@gmail.com', '$2b$12$o9KM9nbujuBN2dadYJrme.nPvvZHecLtxWQMKjEHSl68upsTDmwSS');

#### Create the messages table

    ```SQL

    CREATE TABLE IF NOT EXISTS messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_user) REFERENCES users(id_user)
    );

#### Insert a test message

    ```SQL
    INSERT INTO messages (id_user, message)
    VALUES (1, 'This is a test message from the client.');
