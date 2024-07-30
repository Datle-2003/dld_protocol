import lib.preprocess as preprocess
import socket
import lib.config as config
from pybloom_live import BloomFilter

def send_to_vm2(data, address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(address)
        sock.sendall(data.encode('utf-8'))
        response = sock.recv(4096)
        print(f"Response from DLD: {response.decode('utf-8')}")
    except Exception as e:
        print(f"Error sending data to vm2: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    sensitive_data = bytes()
    with open("sensitive_data.csv", "rb") as file:
        sensitive_data = file.read()
    fuzzy_fingerprints, fingerprint_count = preprocess.preprocess_sensitive_data(sensitive_data)
    # print(f"Fuzzy fingerprints: {fuzzy_fingerprints}")
    # print(f"Count fingerprints: {fingerprint_count}")

    print("Calc fingerprinters and send to DLD provider")

    fuzzy_fingerprints_str = "\n".join(map(str, fuzzy_fingerprints))
    # print(f"Fuzzy fingerprints string: {fuzzy_fingerprints_str}")
    message = f"type=fingerprint;data={fuzzy_fingerprints_str}"

    # print(f"Message: {message}")
    # print(f"Message length: {len(message)}")

    vm2_address = config.vm2_address
    # print(f"VM2 address: {vm2_address}")
    send_to_vm2(message, vm2_address)

