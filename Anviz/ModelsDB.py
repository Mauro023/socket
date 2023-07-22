import pymysql
from datetime import datetime, timedelta


def conexion() -> pymysql.connect | None:
    """
    Establece una conexión a la base de datos utilizando pymysql

    :return: pymysql.connect Objeto de conexión a la base de datos
    :raises pymysql.err.OperationalError: Si ocurre un error al conectarse a la base de datos
    """
    try:
        conn = pymysql.connect(host='localhost',
                               user='root',
                               passwd='',
                               db='cumisystem',
                               charset='utf8mb4')
        return conn
    except pymysql.err.OperationalError as error:
        print(f'Ocurrió un error mientras de conectaba a la base de datos {error}')
        return None


def last_attendance(id_empleado: int, dia: datetime) -> any:
    """
    Función encargada de extraer el registro de la última entrada
    para un usuario en específico.

    :param id_empleado: Id del usuario.
    :param dia: Fecha de trabajo en formato 'YYYY-MM-DD'.
    :return: Una tuple que contiene la información del último registro de asistencia correspondiente,
    o None si no se encuentra ningún registro.
    :raises errorhandler: Error relacionado con la consulta a la BD.
    """
    cursor = conexion().cursor()
    try:
        cursor.execute(f""" 
                    SELECT * FROM attendances
                    WHERE attendances.employe_id = {id_empleado}
                    AND attendances.workday = '{dia}'
                    ORDER BY employe_id DESC;
                        """)
        if cursor:
            return cursor.fetchone()
        else:
            return None
    except pymysql.err.OperationalError as e:
        raise Exception(f'Ocurrió un error {e}')
    finally:
        cursor.close()


def attendance_exists(dia: datetime, hora: datetime.time, id_empleado: int) -> bool:
    """
    Verifica si existe un registro de asistencia para un empleado en una fecha y hora específicas.

    :param dia: Fecha de trabajo.
    :param hora: Hora de entrada.
    :param id_empleado: ID del empleado.
    :return: True si existe un registro de asistencia que cumple con los criterios especificados
             False de lo contrario.
    """
    cursor = conexion().cursor()
    try:
        cursor.execute(f"""
                            SELECT * FROM attendances
                            WHERE attendances.workday = '{dia}'
                            AND attendances.aentry_time = '{hora}'
                            AND attendances.employe_id = {id_empleado}
                            """)
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False
    except pymysql.err.OperationalError as e:
        raise Exception(f'Ocurrió un error {e}')
    finally:
        cursor.close()


def employe_exists(id_empleado: int) -> bool:
    """
    Verifica si existe un registro de asistencia para un empleado en una fecha y hora específicas.

    :param id_empleado: ID del empleado.
    :return: True si existe un registro de asistencia que cumple con los criterios especificados
             False de lo contrario.
    """
    cursor = conexion().cursor()
    try:
        cursor.execute(f""" SELECT * FROM employes  WHERE id = {id_empleado} """)
        result = cursor.fetchone()
        if result and result[0] > 0:
            return True
        else:
            return False
    except pymysql.err.OperationalError as e:
        raise Exception(f'Ocurrió un error {e}')
    finally:
        cursor.close()


def attendance_repository(usuario: dict) -> None:
    """
    Registra una nueva asistencia en la base de datos.

    :param usuario: Diccionario con los datos a ingresar.
    :return: None
    :raises Exception: Se produce una excepción si ocurre algún error durante la inserción.
    """
    conn = conexion()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO attendances (workday, aentry_time, adeparture_time, employe_id) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (usuario['workday'], usuario['aentry_time'],
                                 usuario['adeparture_time'], usuario['employe_id']))
        conn.commit()
        print('Entrada registrada')
    except pymysql.err.OperationalError as e:
        raise Exception(f'Ocurrió un error en la inserción {e}')
    finally:
        conn.close()


def find_attendance_by_day(dia: datetime, id_empleado: int) -> tuple | None:
    """
    Busca un registro de asistencia para un empleado en un día específico.

    :param dia: Fecha de trabajo.
    :param id_empleado: ID del empleado.
    :return: Una tupla que contiene la información del registro de asistencia correspondiente,
             o None si no se encuentra ningún registro.
    :raises Exception: Se produce una excepción si ocurre algún error durante la consulta.
    """
    cursor = conexion().cursor()
    try:
        cursor.execute(f"""
                        SELECT * FROM attendances 
                        WHERE workday = '{dia}'
                        AND attendances.employe_id = {id_empleado}
                        AND attendances.adeparture_time IS NULL
                        ORDER BY workday DESC;
                        """)
        if cursor:
            return cursor.fetchone()
        else:
            return None
    except pymysql.err.OperationalError as e:
        raise Exception(f'Ocurrió un error en la consulta {e}')
    finally:
        cursor.close()


def find_attendance_by_previous_day(employe_id, entry_date, entry_time) -> tuple | None:
    """
    Busca un registro de asistencia para un empleado en el día anterior, y si no existe una entrada para ese día o si
    existe una entrada, pero la hora de entrada es mayor que la hora actual, devuelve el registro que cumpla con esas
    condiciones.

    :param employe_id: ID del empleado.
    :param entry_date: Fecha de trabajo en formato 'YYYY-MM-DD'.
    :param entry_time: Hora de entrada en formato 'HH:mm:ss'.
    :return: Una tupla que contiene la información del registro de asistencia correspondiente,
             o None si no se encuentra ningún registro.
    """
    conn = conexion()
    try:
        with conn.cursor() as cursor:
            previous_day = (datetime.strptime(entry_date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
            sql = """
            SELECT * FROM attendances
            WHERE employe_id = %s
            AND (DATE(workday) = %s AND TIME(aentry_time) > %s)
            OR (DATE(workday) = %s AND adeparture_time IS NULL)
            ORDER BY workday DESC
            LIMIT 1
            """
            cursor.execute(sql, (employe_id, previous_day, entry_time, previous_day))
            result = cursor.fetchone()
            return result
    except pymysql.err.OperationalError as e:
        raise Exception(f'Ocurrió un error en la consulta {e}')
    finally:
        conn.close()


def update_attendance_by_day(record: list) -> None:
    conn = conexion()
    try:
        with conn.cursor() as cursor:
            query = f"UPDATE attendances SET adeparture_time = '{record[3]}' WHERE id = '{record[0]}'"
            cursor.execute(query)
            conn.commit()
    except pymysql.err.OperationalError as e:
        raise Exception(f'Revise lo datos a ingresar error {e}')
    finally:
        conn.close()


