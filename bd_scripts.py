import mysql.connector, json

# Función para conectar a la base de datos
def db_connect():
    return mysql.connector.connect(
        host="tu_host",
        user="tu_usuario",
        password="tu_contraseña",
        database="mi_bot_db"
    )

# Función para actualizar o insertar el estado de un usuario
def update_user_state(chat_id, username, state):
    db = db_connect()
    cursor = db.cursor()
    query = """
    INSERT INTO users (chat_id, username, current_state) VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE username=%s, current_state=%s
    """
    cursor.execute(query, (chat_id, username, state, username, state))
    db.commit()
    db.close()

# Función para guardar o actualizar una alerta
def update_alert(chat_id, alert_type, is_active, settings):
    db = db_connect()
    cursor = db.cursor()
    query = """
    INSERT INTO alerts (chat_id, alert_type, is_active, settings) VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE is_active=%s, settings=%s
    """
    cursor.execute(query, (chat_id, alert_type, is_active, json.dumps(settings), is_active, json.dumps(settings)))
    db.commit()
    db.close()

def get_user_state(chat_id):
    db = db_connect()
    cursor = db.cursor(dictionary=True)  # Usar `dictionary=True` para obtener los resultados como diccionarios

    try:
        # Prepara y ejecuta la consulta SQL
        query = "SELECT * FROM users WHERE chat_id = %s"
        cursor.execute(query, (chat_id,))
        result = cursor.fetchone()  # Obtiene el primer resultado

        return result  # Este será un diccionario con los datos del usuario o None si no se encontró nada

    except mysql.connector.Error as err:
        print("Error al consultar la base de datos:", err)
        return None  # Devuelve None en caso de error

    finally:
        db.close()  # Asegúrate de cerrar la conexión a la base de datos