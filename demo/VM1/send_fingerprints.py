import lib.preprocess as preprocess
import socket
import lib.config as config

def read_data(file_name):
    sensitive_data = ""
    with open(file_name, "r") as file:
        for line in file:
            sensitive_data += line
    return sensitive_data


def send_to_vm2(data, address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(address)
        sock.sendall(data.encode('utf-8')) # convert string to bytes
        response = sock.recv(1024)
        print(f"Response from vm2: {response.decode('utf-8')}")
    except Exception as e:
        print(f"Error sending data to vm2: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    sensitive_data = read_data("sensitive_data.csv")
    fuzzy_fingerprints = preprocess.preprocess_sensitive_data(sensitive_data)

    # Convert fuzzy fingerprints to a format suitable for sending
    fuzzy_fingerprints_str = "\n".join(map(str, fuzzy_fingerprints)) # convert list to string
    message = f"type=fingerprint;data={fuzzy_fingerprints_str}"

    # print(f"Sending message to VM2: {message}")
    vm2_address = config.vm2_address
    send_to_vm2(message, vm2_address)

