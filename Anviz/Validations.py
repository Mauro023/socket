from datetime import datetime
import requests
import pymysql


def conexion() -> pymysql.connect:
    """
    Establece una conexión a la base de datos utilizando pymysql

    :return:
        pymysql.connect: Objeto de conexión a la base de datos

    :raises
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


def querys(conector_sql, mode=None,
           table=None, column=None, target=None) -> None:
    """
    Ejecuta una consulta SQL en la base de datos utilizando un objeto de conexión.

    :param conector_sql: Objeto de conexión a la base de datos.
    :param mode: Modo de consulta. Valor por defecto es None.
    :param table: Nombre de la tabla en la base de datos. Valor por defecto es None.
    :param column: Nombre de la columna en la tabla. Valor por defecto es None.
    :param target: Valor objetivo para filtrar los resultados de la consulta. Valor por defecto es None.
    :return: None si la consulta arroja error, de lo contrario todas las filas de la consulta

    """
    cur = conector_sql.cursor()
    if mode is None:
        cur.execute(f""" 
                    SELECT * FROM {table}
                    WHERE {table}.{column} = {target}
                    """)
    if cur:
        print(f'Existen resultados {type(cur)}')
        for row in cur:
            print(row)
        return cur
    else:
        print('No existen resultados')
        return None


if __name__ == '__main__':
    querys(conexion(), table='attendances', column='employe_id', target=4)






