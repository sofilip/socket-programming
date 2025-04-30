
from functions import *
import socket
import threading

HEADER = 64
PORT = 12346
HOST = "localhost"
ADDR = (HOST, PORT)
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

"""
this function creates the server socket and returns it
in the the main function 
"""
def create_server_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reuse of the address
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    return server_socket

"""
this function creates the server socket and returns it
in the the main function 
"""
def handle_client(conn, addr):
    print(f"New connection from address: {addr}")
    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                # print(f"[{addr}] {msg}")
            # conn.send("Msg received".encode(FORMAT))
        except Exception or connected == False as e:
            if Exception:
                print(e)
            break
        finally:
            conn.close()
            server_socket.close()

def start():
    while True:
        try: 
            server_socket = create_server_socket(HOST, PORT)
            print("Server started successfully !")
            
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
        except Exception as e:
            if e.errno == 98: 
                print("Error: Address already in use")
            else:
                print(f"An unexpected error occurred: {e}")
            return server_socket
        finally:
            conn.close()
            server_socket.close()
            return server_socket
            
if __name__ == "__main__":
    try:
        while True:
            print(f"Server is starting on {HOST}...")
            server_socket = start()
            break
    except Exception:
        print("Exiting...")
    finally:
        server_socket.close()