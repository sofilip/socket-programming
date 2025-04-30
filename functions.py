import socket
import threading
import time
import functions
import math

HOST = 'localhost'
PORT = 12346

""" 
input_validation() function
  takes as input: 
      i) a prompt
      ii) the input type
      iii) a min value if theres one
      iv) a max value if theres one
    output: 
"""
def input_validation(prompt, input_type, min_val=None, max_val=None):
    while True:
        try:
            value = input_type(input(prompt))
            
            if min_val is not None and value < min_val:
                print(f"Invalid Input..")
                continue

            if max_val is not None and value > max_val:
                print(f"Invalid Input..")
                continue
            return value
        except ValueError:
            print(f"Error: Please enter a valid {input_type.__name__} number")

""" 
test_connection() function
  takes as input: 
      i) client_socket
      ii) an input: client or server 
    output: 
"""
def test_connection(client_socket, input):
    while True:
        if input == "client":
            try:
                client_socket.connect((HOST, PORT))
                break  # exit the loop if the connection is successful
            except ConnectionRefusedError:
                print("Server's Not Responding..")
                time.sleep(7)
                continue
            except Exception as e:
                # if server the is connected then return 0 => continue
                if e.errno == 106:
                    return 0
                # else the server is down so return 1 => exit
                else:
                    return 1              

""" 
sending_data() function
  takes as input: 
      i) client_socket
      ii) an operation: 
          1: multiply   
          2: average  
          3: subtraction  
    returns: 
"""
def sending_data(client_socket, operation, set0, set1=None):
    try:
        # Test the connection
        flag = test_connection(client_socket, "client")
        print(flag)
        
        if flag == 0:
            # Send the operation type to the server
            client_socket.send(str(operation).encode())
            print(f"Sent operation: {operation}")
            
            # Send the data sets to the server
            if operation == "3":  # For subtraction
                # Ensure set1 is provided when operation is 3
                if set1 is None:
                    print("Error: set1 must be provided for subtraction.")
                    return
                
                client_socket.send(','.join(map(str, set0)).encode())
                client_socket.send(','.join(map(str, set1)).encode())
                print(f"Sent set0: {set0} and set1: {set1}")
            else:
                client_socket.send(','.join(map(str, set0)).encode())
                print(f"Sent set0: {set0}")
            
            # Receive the response from the server
            response = client_socket.recv(1024).decode()
            print("Response from server:", response)
            return
        
        elif flag == 1:
            print("Server's Down...Exiting..")
            return
            
    except Exception as e:
        print(f"Error: {e}")
        print("Exiting...")
        return
    
    finally:
        client_socket.close()  # Close the client socket when done

""" 
operations(set0, set1, operation) function
  takes as input: 
      i) client_socket
      ii) an operation: 
          1: multiply   
          2: average  
          3: subtraction  
    returns: 
"""  
def operations(operation, set0, set1):
    # set0, set1 = sets  
    if operation == "1": 
        return math.prod(set0)
    elif operation == "2": 
        return math.sumprod(set0)/int(len(set0))
    else:
        return str([a - b for a, b in zip(set0, set1)])