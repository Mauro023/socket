import pyodbc
from datetime import datetime, timedelta


def conexion() -> pyodbc.Connection | None:
    """
    Establece una conexión a la base de datos utilizando pyodbc

    :return: pyodbc.connect Objeto de conexión a la base de datos
    :raises pyodbc.err.OperationalError: Si ocurre un error al conectarse a la base de datos
    """
    try:
        conn = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=localhost;'
            'DATABASE=cumisystem;'
            'UID=sa;'
            'PWD=Sistemas2023;'
        )
        return conn
    except pyodbc.Error as error:
        print(f'Ocurrió un error mientras de conectaba a la base de datos {error}')
        return None


def last_attendance(id_empleado: int, dia: datetime, entry_time: datetime.time) -> any:
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
                    SELECT TOP 1 * FROM attendances
                    WHERE attendances.employe_id = {id_empleado}
                    AND attendances.workday = '{dia}'
                    AND attendances.aentry_time < '{entry_time}'
                    AND attendances.adeparture_time IS Null
                    ORDER BY attendances.id DESC;
                        """)
        if cursor:
            return cursor.fetchone()
        else:
            return None
    except pyodbc.Error as e:
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
    except pyodbc.Error as e:
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
    except pyodbc.Error as e:
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
            VALUES (?, ?, ?, ?)
            """
            cursor.execute(sql, (usuario['workday'], usuario['aentry_time'],
                                 usuario['adeparture_time'], usuario['employe_id']))
        conn.commit()
        print('Entrada registrada')
    except pyodbc.Error as e:
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
    except pyodbc.Error as e:
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

            SELECT TOP 1 * FROM attendances a
                JOIN employes e ON a.employe_id = e.id 
                WHERE e.id = ?
                AND a.workday = ?
                AND a.adeparture_time IS NULL
                AND e.unit = 'Asistencial'
                ORDER BY a.workday DESC;
            """

            cursor.execute(sql, (employe_id, previous_day))
            result = cursor.fetchone()
            return result
    except pyodbc.Error as e:
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
    except pyodbc.Error as e:
        raise Exception(f'Revise lo datos a ingresar error {e}')
    finally:
        conn.close()

