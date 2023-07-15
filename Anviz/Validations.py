from datetime import datetime
import requests
import pymysql


def conexion() -> pymysql.connect:
    """
    Establece una conexión a la base de datos utilizando pymysql

    :return:
        pymysql.connect: Objeto de conexión a la base de datos

    raises:
        pymysql.err.OperationalError: Si ocurre un error al conectarse a la base de datos
    """
    try:
        conn = pymysql.connect(host='localhost',
                               user='root',
                               passwd='',
                               db='cumisystem',
                               charset='utf8mb4')
        return conn
    except pymysql.err.OperationalError as perr:
        print(f'Ocurrio un error mientras de conectaba a la base de datos {perr}')
        return None


def eloquent(conector_sql, mode=None,
           target_1=None, target_2=None, target_3=None) -> pymysql.Connection:
    """
    Ejecuta una consulta SQL en la base de datos utilizando un objeto de conexión
    Dependiendo del modo se debe pasar los parametros en orden
    para mode: None target_1=id, target_2=workday, target_3=None
    de lo contrario target_1=workday, target_2=aentrytime, target_3=id

    :param target_3: Tercer parametro para coincidencia, si es necesario.
    :param target_2: Segunda coincidencia para el where anidado.
    :param target_1: Primera coincidencia para la cláusula where.
    :param conector_sql: Objeto de conexión a la base de datos.
    :param mode: Modo de consulta. Unica o anidado Valor por defecto es None.
    :return: None si la consulta arroja error, de lo contrario todas las filas de la consulta.

    """
    cur = conector_sql.cursor()
    if mode is None:
        cur.execute(f""" 
                    SELECT * FROM attendances
                    WHERE attendances.employe_id = {target_1}
                    AND attendances.workday = '{target_2}'
                    ORDER BY employe_id DESC;
                    """)
        if cur:
            return cur.fetchone()
        else:
            return None
    else:
        cur.execute(f"""
                    SELECT * FROM attendances
                    WHERE attendances.workday = '{target_1}'
                    AND attendances.aentry_time = '{target_2}'
                    AND attendances.employe_id = {target_3}""")
        if cur:
            return True
        else:
            return False


if __name__ == '__main__':
    lastAttendance = eloquent(conexion(), target_1=3, target_2='2023-04-28')
    attendanceExists = eloquent(conexion(),mode='exists', target_1='2023-04-28', target_2='15:41:39', target_3=3)
    print(lastAttendance)
    print(attendanceExists)






