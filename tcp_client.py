import socket

def tcp_client(host, port, payload):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        client_socket.connect((host, port))
        print(f"Connected to {host}:{port}")

        # Send the plaintext payload
        client_socket.sendall(payload.encode('utf-8'))
        print(f"Sent: {payload}")

        # Receive the response from the server
        response = client_socket.recv(4096)
        print(f"Received: {response.decode('utf-8')}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the socket
        client_socket.close()

# Example usage
host = "0.0.0.0"  # Replace with the server's hostname or IP address
port = 12345  # Replace with the server's port
payload = "Hello, this is a plaintext payload."

tcp_client(host, port, payload)
