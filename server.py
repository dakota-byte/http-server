"""
Description: A simple HTTP Server

python ./server --directory serverstorage
"""

import signal
import socket
import sys
import threading
import argparse
import time
import config
from variables import *
from HTTPRequest import *
from HTTPResponse import *

parser = argparse.ArgumentParser(description="A simple HTTP Server")
parser.add_argument("--directory", help="The directory to host in")
parser.add_argument("--port", help="The port to host on")
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
        print("(Connection closed)", addr)


def main():
    port = args.port or PORT  # use cmdline arg, or default to variables.py
    config.ServerConfig["directory"] = args.directory or "./"

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, int(port)))
    server_socket.listen(CONNECTION_BACKLOG)

    print("(Starting server) " + HOST + ":" + str(port), "with PID", os.getpid())
    print("Managing resources in " + config.ServerConfig["directory"])
    print("Listening for connections...")

    server_socket.setblocking(False)  # Set the socket to non-blocking

    while True:
        try:
            client_socket, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, addr)).start()
        except BlockingIOError:
            time.sleep(0.1)  # Sleep to prevent busy-waiting

def signal_handler(sig, frame):
    print("Exiting...")
    os.kill(os.getpid(), signal.SIGTERM)
    sys.exit(0)

# Set up signal handler for graceful shutdown
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    main()
