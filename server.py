"""
Description: A simple HTTP Server

python ./server --directory serverstorage
"""

import socket
import threading
import argparse
from variables import *
from HTTPRequest import *
from HTTPResponse import *

parser = argparse.ArgumentParser(description="A simple HTTP Server")
parser.add_argument("--directory", help="The directory to host in")
args = parser.parse_args()


def handle_client(client_socket, addr):
    print("(Received connection)", addr)

    try:
        request = client_socket.recv(BUFFER_SIZE)
        Client_HTTPRequest = HTTPRequest(request.decode("utf-8"))
        
        Server_HTTPResponse = Client_HTTPRequest.getResponse()
        client_socket.send(Server_HTTPResponse)
    finally:
        client_socket.close()


ServerConfig = {
    "Content-Encoding": ["gzip"],
    "directory": "./"
}


def main():
    print("Starting server...")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(CONNECTION_BACKLOG)

    ServerConfig["directory"] = args.directory or "./"

    print("Listening for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()


if __name__ == "__main__":
    main()
