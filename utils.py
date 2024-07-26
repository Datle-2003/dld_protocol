import psutil

network_interfaces = psutil.net_if_addrs()

for interface_name, interface_addresses in network_interfaces.items():
    print(f"Interface: {interface_name}")
