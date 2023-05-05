import os
import sys
import time
import socket
import pymysql

host = os.environ.get("MYSQL_HOST")
port = int(os.environ.get("MYSQL_TCP_PORT"))

def is_db_ready(host, port):
    try:
        sock = socket.create_connection((host, port), timeout=1)
        sock.close()
        return True
    except socket.error:
        return False

def main():
    host = os.environ.get("MYSQL_HOST")
    port = int(os.environ.get("MYSQL_TCP_PORT"))

    print(f"Esperando a que la base de datos esté lista en {host}:{port}...")

    while not is_db_ready(host, port):
        print("La base de datos no está lista todavía, reintentando en 5 segundos...")
        time.sleep(5)

    print("La base de datos está lista.")

if __name__ == "__main__":
    main()
