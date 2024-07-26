import socket
import threading
import ssl
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import config

def handle_fingerprint_connection(conn):
    global fuzzy_fingerprints
    try:
        data = conn.recv(1024).decode('utf-8')
        fingerprints = data.split("\n")
        fuzzy_fingerprints.update(fingerprints)
        conn.sendall(b"Fingerprints received")
    except Exception as e:
        print(f"Error receiving fingerprints: {e}")
    finally:
        conn.close()

def handle_traffic_connection(conn, secret_key):
    try:
        encrypted_data = conn.recv(1024)
        cipher = AES.new(secret_key.encode('utf-8'), AES.MODE_CBC, iv=encrypted_data[:16])
        decrypted_data = unpad(cipher.decrypt(encrypted_data[16:]), AES.block_size).decode('utf-8')
        
        if detect_leakage(decrypted_data, fuzzy_fingerprints, M):
            print("Sensitive data detected!")
            conn.sendall(b"Sensitive data detected!")
        else:
            print("No sensitive data detected")
            conn.sendall(b"No sensitive data detected")
    except Exception as e:
        print(f"Error handling traffic data: {e}")
    finally:
        conn.close()

def handle_vm1_connection(client_socket, vm3_address, secret_key):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=config.certfile, keyfile=config.keyfile)

    with socket.create_connection(vm3_address) as sock:
        with context.wrap_socket(sock, server_hostname=vm3_address[0]) as ssock:
            ssock.sendall(secret_key.encode('utf-8'))
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                handle_traffic_connection(client_socket, secret_key)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(config.vm2_address)
    server_socket.listen(5)
    print("VM2 listening on", config.vm2_address)

    while True:
        client_socket, _ = server_socket.accept()
        threading.Thread(target=handle_connection, args=(client_socket,)).start()

def handle_connection(client_socket):
    try:
        # Determine if it's a fingerprint or data connection
        initial_data = client_socket.recv(1024).decode('utf-8')
        if initial_data.startswith("fingerprint"):
            handle_fingerprint_connection(client_socket)
        else:
            secret_key = initial_data.split("\n")[0]
            vm3_address = config.vm3_address
            handle_vm1_connection(client_socket, vm3_address, secret_key)
    except Exception as e:
        print(f"Error handling connection: {e}")
    finally:
        client_socket.close()

def rabin_fingerprint(shingle, p_x=31):
    # Simplified Rabin fingerprinting implementation
    p = 53
    m = 2**61 - 1
    hash_value = 0
    for char in shingle:
        hash_value = (hash_value * p_x + ord(char)) % m
    return hash_value

if __name__ == "__main__":
    start_server()
