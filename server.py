
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
            
            if command == "1":  # For multiplication
                data = client_socket.recv(1024).decode()
                set0 = list(map(int, data.split(',')))
                product = math.prod(set0)
                result = f"Multiplication: {product}"
                
            elif command == "2":  # For average
                data = client_socket.recv(1024).decode()
                set0 = list(map(int, data.split(',')))
                if set0:
                    average = sum(set0) / len(set0)
                    result = f"Average: {average}"
                else:
                    result = "Error: set0 is empty."
                
            elif command == "3":  # For subtraction
                set0_data = client_socket.recv(1024).decode()
                set1_data = client_socket.recv(1024).decode()
                set0 = list(map(int, set0_data.split(',')))
                set1 = list(map(int, set1_data.split(',')))
                
                if len(set0) != len(set1):
                    result = "Error: set0 and set1 must be of the same length."
                else:
                    difference = [a - b for a, b in zip(set0, set1)]
                    result = f"Difference: {difference}"
            else:
                result = "Error: Invalid command."

            client_socket.send(result.encode())
    
    except Exception as e:
        print(f"Error handling client {address}: {e}")
        connected = False  # Set connected to False to exit the loop
    
    finally:
        try:
            client_socket.close()  # Close the client socket when done
        except Exception as e:
            print(f"Error closing socket: {e}")

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