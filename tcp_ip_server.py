
import socket
import threading
import time

file_path = "aaa.txt"

def handle_client(client_socket, address):
    print(f"Accepted connection from {address}")
    message_old = ''
    a = 0
    while True:
        with open(file_path, 'r') as file:
            file_contents = file.read()
            if file_contents != a:
                client_socket.sendall(file_contents.encode())
                time.sleep(0.1)
                temp = '\n'
                data = temp.encode()
                client_socket.send(data)
                print(f"Sent file contents to {address}: {file_contents}")
                a = file_contents

def start_server():
    host = "192.168.1.39"
    port = 2000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server is listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    start_server()
