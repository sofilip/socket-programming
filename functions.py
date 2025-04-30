import socket
import threading
import time
import functions

HOST = 'localhost'
PORT = 12346

""" 
input_validation() function
  takes as input: 
      i) a prompt
      ii) the input type
      iii) a min value if theres one
      iv) a max value if theres one 
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
      i) user_socket
      ii) an input: client or server 
"""
def test_connection(user_socket, input):
    while True:
        if input == "client":
            try:
                user_socket.connect((HOST, PORT))
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
      i) user_socket
      ii) an operation: 
          1: multiply   
          2: average  
          3: subtraction  
"""
def sending_data(user_socket, operation, set0, set1):
    try:
        flag = test_connection(user_socket)
        print(flag)
        if flag == 0:
            # start a thread to receive messages from the server
            print("Sending data to Server..")
            return
            # send_request(operation, numbers)
        elif flag == 1:
            print("Server's Down...Exiting..")
            return
    except Exception:
            print("Exiting...")
            return
    finally:
        user_socket.close()
        return
    
def operations(set0, set1, operation):
    if operation == 1:
        return eval('*'.join(map(str, set0)))
    elif operation == 2:
        return sum(set0) / len(set0)
    else:
        return [a - b for a, b in zip(set0, set1)]