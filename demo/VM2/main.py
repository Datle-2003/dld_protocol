import socket
import threading
from pybloom_live import BloomFilter
import lib.config as config
import lib.detect as detect

fuzzy_fingerprints = []
bf = BloomFilter(capacity=10000, error_rate=0.001)

def handle_fingerprint_connection(data, conn):
    global fuzzy_fingerprints, bf
    try:
        # Extract the part after 'data='
        if 'data=' in data:
            data_part = data.split('data=')[1]
            fingerprints = data_part.split("\n")
            # Convert each element to a number
            fingerprints = [int(fp) for fp in fingerprints if fp.strip() != ""]
            fuzzy_fingerprints.extend(fingerprints)
            conn.sendall(b"Fingerprints received")
            # print(f"Fingerprints received: {fuzzy_fingerprints}")
            for fingerprint in fuzzy_fingerprints:
                bf.add(fingerprint)
        else:
            print("No data found in the message")
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
        print(f"Error forwarding data to server: {e}")
    finally:
        sock.close()


def handle_connection(client_socket):
    try:
        initial_data = client_socket.recv(110000).decode('utf-8')
        if initial_data.startswith("type=fingerprint"):
            # print(len(initial_data))
            # print(initial_data)
            print("Received fingerprints")
            handle_fingerprint_connection(initial_data, client_socket)
        else:

            parts = initial_data.split(";")
            address_part = parts[0].split("=")[1].strip()
            address_part = address_part[3:-1]
            host, port = address_part.split(", ")
            vm3_host = host.strip("'")
            vm3_port = int(port.strip())
            vm3_address = (vm3_host, vm3_port)

            data = parts[1].split("=")[1].strip()

            # print(vm3_address)
            
            is_sensitive = False if len(fuzzy_fingerprints) == 0 else detect.detect_traffic(data.encode('utf-8'), bf, len(fuzzy_fingerprints), threshold=0.6)
            
            if is_sensitive:
                client_socket.sendall("Data is sensitive".encode('utf-8'))
            else:
                forward_to_vm3(data, vm3_address)
                client_socket.sendall(b"Data sent to server")

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