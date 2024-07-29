import psutil

# Lấy thông tin về các card mạng
network_interfaces = psutil.net_if_addrs()

# Hiển thị danh sách các card mạng và địa chỉ IP tương ứng
for interface_name, interface_addresses in network_interfaces.items():
    print(f"Interface: {interface_name}")
