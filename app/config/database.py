import mysql.connector

def connection_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Cristopher0812",
            database="Pinares_del_norte"
        )
        # print("Conexión exitosa a la base de datos.")
        return connection
    except mysql.connector.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()
        print("Conexión cerrada.")
