
from functions import *

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if __name__ == "__main__":
    try:
        while True:
            flag = test_connection(client_socket, "client")
            # user chooses operation 
            operation = int(input_validation("Choose operation: (1) MULTIPLY, (2) AVERAGE, (3) SUBTRACT or (0) EXIT to exit: ", int, min_val=0, max_val=4))
            if operation == 0:
                break
            
            # if the user chooses subtraction then they should enter from 2 to 20 integers
            if operation == 2:
                N_integers = int(input_validation("Enter the number of inetegers (from 2 to 20): ", int, min_val=2, max_val=20))
            # else the user should choose from 2 to 10 integers
            else:
                N_integers = int(input_validation("Enter the number of inetegers (from 2 to 10): ", int, min_val=2, max_val=10))
            set0 = []
            set1 = []
            
            # input
            for i in range(N_integers):
                # if MULTIPLY then input > -5 and input < 5 => 1 byte signed integer
                if operation == 1:
                    set0.append(int(input_validation(f"Enter the {i}{'th'*(10<i%100<20)or' stndrd'[i%10*2:]} integer: ", int, min_val=0, max_val=60000)))                    
                    continue
                # if AVERAGE then input > 0 and input < 200 => 1 byte unsigned integer
                elif operation == 2:
                    set0.append(int(input_validation(f"Enter the {i}{'th'*(10<i%100<20)or' stndrd'[i%10*2:]} integer: ", int, min_val=0, max_val=200)))
                    continue
                # if SUBTRACT then input > 0 and input < 60000 => 4 byte signed integer
                else:
                    set0.append(int(input_validation(f"Enter the {i}{'th'*(10<i%100<20)or' stndrd'[i%10*2:]} integer for the 1st set: ", int, min_val=0, max_val=60000)))
                    set1.append(int(input_validation(f"Enter the {i}{'th'*(10<i%100<20)or' stndrd'[i%10*2:]} integer for the 2nd set: ", int, min_val=0, max_val=60000)))
                    if len(set0) != len(set1):
                        print("The sets should have the same length !")
                        break
                    continue
                
            if operation == 1:
                sending_data(client_socket, "1", set0, [])

            elif operation == 2:
                sending_data(client_socket, "2", set0, [])

            elif operation == 3 and (len(set0) == len(set1)):
                sending_data(client_socket, "3", set0, set1)
            else:
                print("Unknown Error..")
                break
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        client_socket.close()
