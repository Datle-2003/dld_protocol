import socket
import lib.config as config
import sys
import lib.preprocess as preprocess
import lib.detect as detect
from pybloom_live import BloomFilter

def send_data(data, vm2_address, vm3_address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(vm2_address)
        message = f"type=to{vm3_address};data=".encode('utf-8') + data    
        print(f"Sending message to VM2: {message}")
        sock.sendall(message)
        
        # Wait for response from VM2
        response = sock.recv(4096)
        print(f"Response from VM2: {response.decode('utf-8')}")

        if response == b"Data sent to server":
            print("Data sent to server")
        else:
            print("Error sending data to server")
            # detect.postprocess_traffic(response, original_fingerprints, 0.6)
    except Exception as e:
        print(f"Error sending data to VM2: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    # get the first arg as the file name
    traffic_data = ""
    filename = sys.argv[1]
    with open(filename, "rb") as file:
        traffic_data = file.read()
    
    print("Send traffic data: ", traffic_data, " to DLD provider")

    send_data(traffic_data, config.vm2_address, config.vm3_address)
