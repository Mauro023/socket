# -*- coding=utf-8 -*-

"""
    anviz-sync real-time
    ~~~~~~~~~~~~~~~~~~~~

    Software that listen on socket connection for Anviz A300 device request and store data in db.

    :copyright: (c) 2022 by Augusto Roccasalva
    :license: BSD, see LICENSE for more details.
"""

import socket
import struct
import requests
import json
import time as t

from configparser import ConfigParser
from datetime import datetime

from anviz_sync import anviz


TYPES = {
    0: "Entrada",
    1: "Salida",
    2: "BREAK",
}


def get_record(raw_data):
    crc_ok = anviz.crc16(raw_data[:23]) == raw_data[-2:]
    if not crc_ok:
        raise ValueError("CRC verificaton failed")
    stx, dev_id, ack, ret, length = struct.unpack(">BLBBH", raw_data[:9])
    record = anviz.parse_record(raw_data[9 : 9 + length])
    return dev_id, record


def show_data(dev_id, record):
    time = datetime.now()
    hora = record.datetime.time()
    fecha = record.datetime.date()
    print(
        "[", 
            "IDU:", record.code, 
            "Date:", fecha, 
            "Time:", hora, 
            "Action:", record.type,
        "]"
    )

     # Crear el objeto de datos para enviar
    data = {
        "workday": str(fecha),
        "aentry_time": str(hora),
        "adeparture_time": None,
        "employe_id": record.code,
        "action": record.type,
    }

    # Configurar la URL de la API Laravel
    url = "http://127.0.0.1:8000/api/updateEntrance/"

    print(data)
    # Enviar la solicitud POST a la API de Laravel
    response = requests.post(url, json=data)

    print ('REGISTRO EXITOSO')


def main():
    config = ConfigParser()
    config.read("anviz-sync.ini")

    # config device
    dev_id = config.getint('anviz', 'device_id')
    ip_addr = config.get("anviz", "ip_address")
    ip_port = config.getint("anviz", "ip_port")

    reconnect = True
    no_data_time = 0
    max_no_data_time = 60  # umbral de tiempo sin recibir datos en segundos

    while reconnect:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect(('10.1.4.182', 5010))
            print("Intentando conectar socket")

            time = datetime.now()
            print(f"[{time}] Connected")
            s.settimeout(None)
            try:
                while True:
                    data = s.recv(1024)
                    if not data:
                        no_data_time += 1
                        if no_data_time > max_no_data_time:
                            print(f"No se han recibido datos en {max_no_data_time} segundos. Cerrando conexión.")
                            s.close()
                            reconnect = False
                            break
                        continue
                    else:
                        no_data_time = 0
                    
                    if len(data) < 24:
                        continue
                    dev_id, record = get_record(data)
                    show_data(dev_id, record)
                if not reconnect:
                    reconnect = True 
                    continue

            except ConnectionResetError as err:
                time = datetime.now()
                print(f"[{time}] Connection reset by peer, closing socket and retrying...")
                s.close()
                break
            except socket.timeout as err:
                time = datetime.now()
                print(f"[{time}] Socket timeout, retrying...")
                s.close()
                break
            except KeyboardInterrupt as err:
                print("Quit")
                break
            except:
                print(f"Error en la conexión. Reintentando en {max_no_data_time} segundos...")
                t.sleep(max_no_data_time)
    s.close()

if __name__ == "__main__":
    main()
