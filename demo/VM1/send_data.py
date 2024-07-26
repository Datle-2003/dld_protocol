from send_fingerprints import read_data
import socket
import config
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import ssl

def encrypt_data(data, secret_key):
    cipher = AES.new(secret_key.encode('utf-8'), AES.MODE_CBC) # use cipher block chaining
    ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    return cipher.iv + ct_bytes


def send_to_vm2(data, secret_key, address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(address)
        message = f"{secret_key}\n{data}"
        sock.sendall(message.encode('utf-8'))
        response = sock.recv(1024)
        print(f"Response from vm2: {response.decode('utf-8')}")
    except Exception as e:
        print(f"Error sending data to vm2: {e}")
    finally:
        sock.close()

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
    data_file = "data_to_send.txt"
    data = read_data(data_file)
    
    # Perform SSL handshake with VM3 to obtain the secret key
    vm3_address = config.vm3_address
    certfile = "path_to_vm1_cert.pem"
    keyfile = "path_to_vm1_key.pem"
    secret_key = ssl_handshake(vm3_address, certfile, keyfile, config.vm2_address)
    print(f"Obtained secret key: {secret_key}")

    #save the secret key to a file
    with open("secret_key.txt", "w") as file:
        file.write(secret_key)

    # Encrypt the data using the obtained secret key
    encrypted_data = encrypt_data(data, secret_key)

    # Send the encrypted data and secret key to VM2
    vm2_address = config.vm2_address
    send_to_vm2(encrypted_data.hex(), secret_key, vm2_address)

if __name__ == "__main__":
    main()
