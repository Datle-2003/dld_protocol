import lib.preprocess
import socket
import lib.config as config
import time

def read_data(file_name):
    sensitive_data = ""
    with open(file_name, "r") as file:
        for line in file:
            sensitive_data += line
    return sensitive_data

def send_data(data, address, vm3_address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(address)
        message = f"type=to{vm3_address};data={data}"
        print(f"Sending message to VM2: {message}")
        sock.sendall(message.encode('utf-8'))
        
        # Wait for response from VM2
        response = sock.recv(1024)
        print(f"Response from VM2: {response.decode('utf-8')}")
    except Exception as e:
        print(f"Error sending data to VM2: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    data_file = "data.csv"
    data = read_data(data_file)
    send_data(data, config.vm2_address, config.vm3_address)
