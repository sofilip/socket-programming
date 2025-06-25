# Network Protocols Assignment

This project is part of a laboratory session. The task involves designing and implementing a custom communication protocol between a server and multiple clients.

## Description

The task involves the development of a communication protocol between a server and multiple clients, designed to facilitate basic arithmetic operations. The server acts as a computational engine that can perform three specific tasks: multiplication of signed integers, calculation of the average of integers, and subtraction of two sets of integers.

### Supported Operations

The server supports the following three operations:

1. **Multiplication**
   - Multiplies `N` signed integers.
   - `N` must be between 2 and 10.
   - Each integer must be in the range **-5 to 5**.
   - Returns a single integer as the product.

2. **Average**
   - Calculates the average of `N` unsigned integers.
   - `N` must be between 2 and 20.
   - Each integer must be in the range **0 to 200**.
   - Returns a float or integer as the average result.

3. **Set Subtraction**
   - Accepts two sets of `N` unsigned integers.
   - `N` must be between 2 and 10.
   - Each integer must be in the range **0 to 60000**.
   - Returns a new set of `N` integers, where each value is the result of subtracting the corresponding value of the second set from the first.

### Client Behavior

- Sends a command to the server specifying the operation and the required input numbers.
- Receives:
  - The result of the operation, or
  - An error message describing the type of input validation failure (e.g., out-of-range values).

### 🖥️ Server Behavior

- Accepts multiple client connections simultaneously (multithreaded or multiprocessing based on lab session 3).
- Validates inputs and responds accordingly.
- Maintains communication using a custom protocol with structured headers and payloads.

## Virtual Environment Setup

To keep dependencies isolated and consistent across environments, use a Python virtual environment:

### 1. Create the virtual environment

```bash
python3 -m venv venv
```

### 2. Activate the virtual environment
On Windows:
```bash
venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

### 3. Install dependencies (if any)
```bash
pip install -r requirements.txt
```
> Create requirements.txt by running pip freeze > requirements.txt after installing any needed packages.

## Deliverables
1. Executable Python code for the Server.
2. Executable Python code for the Client.

## 🔧 Technical Guidelines
- Number range examples:
    - 1-byte unsigned = 0 to 255
    - 2-byte unsigned = 0 to 65535
    - 4-byte unsigned = 0 to 4294967295
    - 1-byte signed = -128 to 127
    - 2-byte signed = -32768 to 32767
    - 4-byte signed = -2147483648 to 2147483647

## Execution
You can test the application by running both the server and multiple clients. Inputs can be:
- Read from the keyboard
- Randomly generated using built-in Python functions

#

Course: Network Protocols

Institution: University of Piraeus

> Let me know if you'd like to include a `.gitignore` template for `venv` as well.







