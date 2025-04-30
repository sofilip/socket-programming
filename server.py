
from functions import *
import socket
import threading

HEADER = 64
PORT = 12346
HOST = "localhost"
ADDR = (HOST, PORT)
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server_socket = None

"""
this function creates the server socket and returns it
in the the main function 
"""
def create_server_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    return server_socket

"""
this function handles client requests 
in a separate thread
"""
def handle_client(client_socket, address):
    print(f"New connection from address: {address}")
    connected = True
    try:
        while connected:
            command = client_socket.recv(1024).decode()
            if not command:
                print(f"Connection closed by client: {address}")
                break
            
            command = int(command)  
            
            if command == 3: 
                set0 = client_socket.recv(1024).decode()
                set1 = client_socket.recv(1024).decode()
                result = operations(command, (list(map(int, set0.split(','))), list(map(int, set1.split(',')))))
            else:
                data = client_socket.recv(1024).decode()
                result = operations(command, list(map(int, data.split(','))))
            
            client_socket.send(result.encode())
    
    except Exception as e:
        print(f"Error handling client {address}: {e}")
    
    finally:
        client_socket.close()  # Close the client socket when done
        print(f"Connection closed for address: {address}")

def start():
    while True:
        try:
            server_socket = create_server_socket()
            if server_socket is not None:
                print("Server started successfully !")
                client_socket, address = server_socket.accept()
                thread = threading.Thread(target=handle_client, args=(client_socket, address))
                thread.start()
            else:
                return
        except Exception as e:
            if e.errno == 98: 
                print("Error: Address already in use")
            else:
                print(f"An unexpected error occurred: {e}")
            return
        finally:
            return server_socket
            
if __name__ == "__main__":
    try:
        while True:
            print(f"Server is starting on {HOST}...")
            server_socket = start()
            break
    except Exception as e:
        print("Something went wrong...")
    finally:
        if server_socket is not None:
            server_socket.close()
        else:
            print("Couldnt find server socket")