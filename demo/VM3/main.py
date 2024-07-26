import socket
import ssl
import config

def receive_data_from_vm1():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=config.certfile, keyfile=config.keyfile)
    context.load_verify_locations(cafile=config.cafile)
    context.verify_mode = ssl.CERT_REQUIRED

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(config.vm3_address)
        sock.listen(5)
        print("VM3 listening on", config.vm3_address)

        while True:
            conn, _ = sock.accept()
            with context.wrap_socket(conn, server_side=True) as ssock:
                print(f"Connection established with VM1")

                # Receive secret key from VM1 via VM2
                secret_key = ssock.recv(1024).decode('utf-8')
                print(f"Secret key received: {secret_key}")

                # Continuously receive and decrypt data from VM1
                while True:
                    encrypted_data = ssock.recv(1024)
                    if not encrypted_data:
                        break
                    print(f"Encrypted data received: {encrypted_data}")

                    # Decrypt the data (ensure VM1 and VM3 use the same encryption parameters)
                    decrypted_data = decrypt_data(encrypted_data, secret_key)
                    print(f"Decrypted data: {decrypted_data}")

def decrypt_data(encrypted_data, secret_key):
    # Replace with the actual decryption logic using the secret key
    # This is a placeholder function
    return encrypted_data  # Modify this with actual decryption steps

if __name__ == "__main__":
    receive_data_from_vm1()
