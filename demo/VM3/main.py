import socket
import lib.config as config

def receive_data_from_vm2():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(config.vm3_address)
    server_socket.listen(5) 
    print("VM3 listening on", config.vm3_address)

    while True:
        client_socket, _ = server_socket.accept()
        with client_socket:
            print("Connection established with VM2")
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                print(f"Data received from VM2: {data}")

if __name__ == "__main__":
    receive_data_from_vm2()
