# import ssl
# import socket
# import lib.config as config
# import os
# import hashlib
# import hmac

# def create_ssl_context(certfile, keyfile, cafile):
#     context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=cafile)
#     context.load_cert_chain(certfile, keyfile)
#     context.load_verify_locations(cafile)
#     return context

# def main():
#     client_cert = config.client_cert
#     client_key = config.client_key
#     server_cert = config.server_cert

#     sock = socket.socket()
#     client_context = create_ssl_context(client_cert, client_key, server_cert)
#     conn = client_context.wrap_socket(sock, server_hostname=config.server_hostname)

#     conn.connect('vm2-address', 443)


#     #generate a pre-master secret
#     pre_master_secret = os.urandom(48)

#     conn.send(pre_master_secret)

#     session_key = hmac.new(pre_master_secret, b'session key derivation', hashlib.sha256).digest()
#     print(f'Derived session key: {session_key.hex()}')

#     # Securely receive data
#     data = conn.recv(1024)
#     print(f'Received: {data}')

#     conn.close()

# if __name__ == "__main__":
#     main()