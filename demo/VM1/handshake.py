import ssl
import socket
import config

def ssl_handshake(vm3_address, certfile, keyfile, vm2_address):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    
    # this one is sending to vm2, then vm2 will send to vm3
    handshake_request = f"handshake;address={vm3_address}"

    with socket.create_connection(vm2_address) as sock:
        with context.wrap_socket(sock, server_hostname=vm2_address[0]) as ssock:
            ssock.sendall(handshake_request.encode('utf-8'))
            response = ssock.recv(1024).decode('utf-8')
            print(f"Response from vm2: {response}")
            return response

def main():
    vm3_address = config.vm3_address
    vm2_address = config.vm2_address
    certfile = "path_to_vm1_cert.pem" # cert
    keyfile = "path_to_vm1_key.pem" # private key

    secret_key = ssl_handshake(vm3_address, certfile, keyfile, vm2_address)

    # save the secret key to a file
    with open("secret_key.txt", "w") as file:
        file.write(secret_key)
