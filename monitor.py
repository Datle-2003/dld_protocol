from scapy.all import sniff, IP, TCP, Raw

def packet_callback(packet):
    if packet.haslayer(IP) and packet.haslayer(TCP):
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport

        print(f"IP {ip_src}:{src_port} -> {ip_dst}:{dst_port}")

        if packet.haslayer(Raw):
            payload = packet[Raw].load
            try:
                print("Payload (as string):")
                print(payload.decode('utf-8', errors='ignore'))  # Attempt to decode payload as UTF-8
            except UnicodeDecodeError:
                print("Payload (raw):")
                print(payload)
        else:
            print("No payload found.")

# Bắt các gói tin đi ra từ mạng (interface là tên của card mạng)
sniff(filter="tcp", prn=packet_callback, iface="lo", store=0) #enp2s0, lo, wlp3s0
