import socket
import threading
import lib.config as config
import lib.detect as detect
import re

fuzzy_fingerprints = []

def handle_fingerprint_connection(conn):
    global fuzzy_fingerprints
    try:
        data = conn.recv(1024).decode('utf-8')
        fingerprints = data.split("\n")
        fuzzy_fingerprints.extend(fingerprints)
        conn.sendall(b"Fingerprints received")
        print(f"Fingerprints received: {fuzzy_fingerprints}")
    except Exception as e:
        print(f"Error receiving fingerprints: {e}")
    finally:
        conn.close()

def forward_to_vm3(data, address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(address)
        sock.sendall(data.encode('utf-8'))
    except Exception as e:
        print(f"Error forwarding data to VM3: {e}")
    finally:
        sock.close()


def handle_connection(client_socket):
    try:
        initial_data = client_socket.recv(1024).decode('utf-8')
        if initial_data.startswith("type=fingerprint"):
            handle_fingerprint_connection(client_socket)
        else:
            parts = initial_data.split(";")
            address_part = parts[0].split("=")[1].strip()
            address_part = address_part[3:-1]
            host, port = address_part.split(", ")
            vm3_host = host.strip("'")
            vm3_port = int(port.strip())
            vm3_address = (vm3_host, vm3_port)

            data = parts[1].split("=")[1].strip()

            forward_to_vm3(data, vm3_address)

            T_hat = detect.detect_traffic(data, fuzzy_fingerprints, config.M)

            response = ""
            if len(fuzzy_fingerprints) == 0:
                response = "No sensitive data detected!"
            elif len(T_hat) / len(fuzzy_fingerprints) > config.threshold:
                response = "Sensitive data detected!"
            else:
                response = "No sensitive data detected!"

            client_socket.sendall(response.encode('utf-8'))

    except Exception as e:
        print(f"Error handling connection: {e}")
    finally:
        client_socket.close()



def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(config.vm2_address)
    server_socket.listen(5)
    print("VM2 listening on", config.vm2_address)

    while True:
        client_socket, _ = server_socket.accept()
        threading.Thread(target=handle_connection, args=(client_socket,)).start()
        

if __name__ == "__main__":
    start_server()