import lib.preprocess as preprocess
import socket
import lib.config as config
from pybloom_live import BloomFilter

def read_data(file_name):
    sensitive_data = ""
    with open(file_name, "rb") as file:
        sensitive_data = file.read()
    return sensitive_data


def send_to_vm2(data, address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(address)
        sock.sendall(data.encode('utf-8'))
        response = sock.recv(4096)
        print(f"Response from vm2: {response.decode('utf-8')}")
    except Exception as e:
        print(f"Error sending data to vm2: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    sensitive_data = read_data("sensitive_data.csv")
    # print(f"Sensitive data: {sensitive_data}")
    _, fingerprint_count, fuzzy_fingerprints = preprocess.preprocess_sensitive_data(sensitive_data)
    print(f"Fuzzy fingerprints: {fuzzy_fingerprints}")
    print(f"Count fingerprints: {fingerprint_count}")

    _, original_fingerprints = preprocess.generate_original_fingerprints(sensitive_data)
    # print(f"Original fingerprints: {original_fingerprints}")

    file_name = "original_fingerprints.txt"
    # original_fingerprints = list(original_fingerprints)

    with open(file_name, "w") as file:
        for fingerprint in original_fingerprints:
            file.write(f"{fingerprint}\n")
        
    fuzzy_fingerprints_str = "\n".join(map(str, fuzzy_fingerprints)) 
    # print(f"Fuzzy fingerprints string: {fuzzy_fingerprints_str}")
    message = f"type=fingerprint;data={fuzzy_fingerprints_str}"

    print(f"Message: {message}")
    print(f"Message length: {len(message)}")

    vm2_address = config.vm2_address
    # print(f"VM2 address: {vm2_address}")
    send_to_vm2(message, vm2_address)

