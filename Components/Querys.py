#importaciones internas // Internal imports
from DB.client import get_sql_connection, sql_database
from fastapi import HTTPException, status
import pymysql

DATABASE = sql_database


def search_user(id_user:int):
    try:
        with get_sql_connection () as connection:
            with connection.cursor() as cursor:
                query=f"""
                SELECT * FROM {DATABASE}.users
                WHERE id_user = %s
                """
                cursor.execute(query,(id_user,))
                result = cursor.fetchall()
                if not result:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User with id {id_user} not found."
                    )
                return result[0]  # Devuelve el primer (y único) usuario encontrado // Returns the first (and only) user found
    except pymysql.MySQLError as e:
        print(f"Error en la consulta a la base de datos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

def save_message(id_user: int, message: str):
    try:
        with get_sql_connection() as connection:
            with connection.cursor() as cursor:
                query = f"""
                INSERT INTO {DATABASE}.messages (id_user, message)
                VALUES (%s, %s)
                """
                cursor.execute(query, (id_user, message))
                connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error al guardar el mensaje en la base de datos: {e}")
        raise


def get_messages():
    try:
        with get_sql_connection() as connection:
            with connection.cursor() as cursor:
                query = """
                SELECT u.username, u.rol, m.message, m.timestamp
                FROM messages m
                JOIN users u ON m.id_user = u.id_user
                ORDER BY m.timestamp ASC
                """
                cursor.execute(query)
                result = cursor.fetchall()
                return result
    except pymysql.MySQLError as e:
        print(f"Error al recuperar mensajes de la base de datos: {e}")
        raise