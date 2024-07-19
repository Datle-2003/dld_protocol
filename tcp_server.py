import socket

def tcp_server(host, port):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the address and port
    server_socket.bind((host, port))
    
    # Listen for incoming connections
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        # Accept a connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Receive the data from the client
        data = client_socket.recv(4096)
        print(f"Received: {data.decode('utf-8')}")

        # Send a response back to the client
        response = "Payload received."
        client_socket.sendall(response.encode('utf-8'))

        # Close the connection
        client_socket.close()

# Example usage
host = "0.0.0.0"  # Listen on all available interfaces
port = 12345  # Use the same port as the client

tcp_server(host, port)
