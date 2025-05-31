import socket
import threading
import time
import math # Make sure to import math for math.prod if it's not in 'functions'

PORT = 12346
HOST = "localhost"

server_socket = None
last_activity_time = time.time()
INACTIVITY_TIMEOUT = 300 # 5 minutes * 60 seconds/minute

"""
This function creates the server socket
and returns it to the main function
"""
def create_server_socket():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        return server_socket
    except Exception as e:
        print(f"Error creating server socket: {e}")
        return None

"""
This function handles
multiple client requests
"""
def handle_client(client_socket, address):
    global last_activity_time
    print(f"New connection from address: {address}")
    last_activity_time = time.time() # Update activity time when a new connection is handled
    connected = True
    try:
        while connected:
            command = client_socket.recv(1024).decode()
            if not command:
                print(f"Connection closed by client: {address}")
                break
            
            last_activity_time = time.time() # Update activity time for every command received

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
                    result = "Error: set0 is empty."
            elif command == "3":  # set subtraction
                set0_data = client_socket.recv(1024).decode()
                set1_data = client_socket.recv(1024).decode()
                set0 = list(map(int, set0_data.split(',')))
                set1 = list(map(int, set1_data.split(',')))
                
                if len(set0) == len(set1):
                    difference = [a - b for a, b in zip(set0, set1)]
                    result = f"Difference: {difference}"
                else:
                    result = "Error: Sets must have the same number of elements for subtraction."
            else:
                result = "Error: Invalid command"

            client_socket.send(result.encode())
    
    except socket.timeout:
        print(f"Client {address} timed out due to inactivity")
    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        try:
            client_socket.close()
            print(f"Client socket closed for {address}")
        except Exception as e:
            print(f"Error closing client socket: {e}")

"""
This function starts the server and manages its lifecycle
"""
def start_server_with_timeout():
    global server_socket
    global last_activity_time

    server_socket = create_server_socket()
    if server_socket is None:
        print("Failed to start server. Exiting.")
        return False # Indicate failure to start

    print(f"Server started successfully on {HOST}:{PORT}")
    last_activity_time = time.time() # Initialize activity time

    while True:
        try:
            server_socket.settimeout(1.0) # Check every 1 second
            
            client_socket, address = server_socket.accept()
            last_activity_time = time.time()
            thread = threading.Thread(target=handle_client, args=(client_socket, address))
            thread.daemon = True
            thread.start()
        except socket.timeout:
            if time.time() - last_activity_time > INACTIVITY_TIMEOUT:
                print(f"No activity for {INACTIVITY_TIMEOUT} seconds. Shutting down server...")
                break
        except Exception as e:
            if isinstance(e, OSError) and e.errno == 98:
                print("Error: Address already in use. Please wait or choose a different port")
                break
            else:
                print(f"An unexpected error occurred during server operation: {e}")
                break
    
    # This part will be reached if the loop breaks (due to inactivity or other error)
    if server_socket:
        print("Closing server socket due to inactivity or error...")
        server_socket.close()
    return True # Indicate successful shutdown or that server was running

# Main execution block
if __name__ == "__main__":
    print(f"Server is starting on {HOST}:{PORT}...")
    try:
        start_server_with_timeout()
    except KeyboardInterrupt:
        print("\nShutting down server gracefully...")
        # Ensure the server socket is closed if it's still open
        if server_socket:
            server_socket.close()
            print("Server socket closed.")
    except Exception as e:
        print(f"An unhandled error occurred in the main block: {e}")
    finally:
        print("Server has shut down")