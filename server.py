import socket
import threading
import time
import math 

PORT = 12346
HOST = "localhost"

SERVER_SOCKET = None
LAST_ACTIVITY_TIME = time.time()
INACTIVITY_TIMEOUT = 300 # 5 minutes * 60 seconds/minute

"""
Creates the server socket
and returns it to the main function
"""
def create_SERVER_SOCKET():
    try:
        SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SERVER_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        SERVER_SOCKET.bind((HOST, PORT))
        SERVER_SOCKET.listen()
        return SERVER_SOCKET
    except Exception as e:
        print(f"Error creating server socket: {e}")
        return None

"""
Handles multiple client requests
"""
def handle_client(client_socket, address):
    global LAST_ACTIVITY_TIME
    print(f"New connection from address: {address}")
    LAST_ACTIVITY_TIME = time.time() # update activity time when a new connection is handled
    connected = True
    try:
        while connected:
            command = client_socket.recv(1024).decode()
            if not command:
                print(f"Connection closed by client: {address}")
                break
            
            LAST_ACTIVITY_TIME = time.time() # update activity time for every command received

            if command == "1":  # multiplication
                data = client_socket.recv(1024).decode()
                set0 = list(map(int, data.split(',')))
                product = math.prod(set0)
                result = f"Multiplication: {product}"
            elif command == "2":  # average
                data = client_socket.recv(1024).decode()
                set0 = list(map(int, data.split(',')))
                if set0:
                    average = sum(set0) / len(set0)
                    result = f"Average: {average}"
                else:
                    result = "Error: set0 is empty !"
            elif command == "3":  # set subtraction
                set0_data = client_socket.recv(1024).decode()
                set1_data = client_socket.recv(1024).decode()
                set0 = list(map(int, set0_data.split(',')))
                set1 = list(map(int, set1_data.split(',')))
                
                if len(set0) == len(set1):
                    difference = [a - b for a, b in zip(set0, set1)]
                    result = f"Difference: {difference}"
                else:
                    result = "Error: Sets must have the same number of elements for subtraction !"
            else:
                result = "Error: Invalid command"

            client_socket.send(result.encode())
    
    except socket.timeout:
        print(f"Client {address} timed out due to inactivity !")
    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        try:
            client_socket.close()
            print(f"Client socket closed for {address}")
        except Exception as e:
            print(f"Error closing client socket: {e}")

"""
Starts the server and manages its lifecycle
"""
def start_server_with_timeout():
    global SERVER_SOCKET
    global LAST_ACTIVITY_TIME

    SERVER_SOCKET = create_SERVER_SOCKET()
    if SERVER_SOCKET is None:
        print("Failed to start server ! Exiting...")
        return False # indicate failure to start

    print(f"Server started successfully on {HOST}:{PORT}")
    LAST_ACTIVITY_TIME = time.time() # initialize activity time

    while True:
        try:
            SERVER_SOCKET.settimeout(1.0) # check every 1 second
            
            client_socket, address = SERVER_SOCKET.accept()
            LAST_ACTIVITY_TIME = time.time()
            thread = threading.Thread(target=handle_client, args=(client_socket, address))
            thread.daemon = True
            thread.start()
        except socket.timeout:
            if time.time() - LAST_ACTIVITY_TIME > INACTIVITY_TIMEOUT:
                print(f"No activity for {INACTIVITY_TIMEOUT} seconds. Shutting down server...")
                break
        except Exception as e:
            if isinstance(e, OSError) and e.errno == 98:
                print("Error: Address already in use. Please wait or choose a different port")
                break
            else:
                print(f"An unexpected error occurred during server operation: {e}")
                break
    
    # this part will be reached if the loop breaks (due to inactivity or other error)
    if SERVER_SOCKET:
        print("Closing server socket due to inactivity or error...")
        SERVER_SOCKET.close()
    return True # indicate successful shutdown or that server was running

# main execution block
if __name__ == "__main__":
    print(f"Server is starting on {HOST}:{PORT}...")
    try:
        start_server_with_timeout()
    except KeyboardInterrupt:
        print("\nShutting down server gracefully...")
        # ensure the server socket is closed if it's still open
        if SERVER_SOCKET:
            SERVER_SOCKET.close()
            print("Server socket closed")
    except Exception as e:
        print(f"An unhandled error occurred in the main block: {e}")
    finally:
        print("Server has shut down !")
