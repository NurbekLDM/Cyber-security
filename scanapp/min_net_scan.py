import scapy.all as scapy
from scapy.all import sniff
from scapy.layers.http import HTTPRequest  # HTTP qatlamini to‘g‘ri import qilish

def sniff_packets(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def process_sniffed_packet(packet):
    if packet.haslayer(HTTPRequest):  # hasLayer o‘rniga haslayer
        print("[+] HTTP so‘rov aniqlandi:")
        print(packet.show())

        # URL ni olish
        host = packet[HTTPRequest].Host.decode() if packet[HTTPRequest].Host else ""
        path = packet[HTTPRequest].Path.decode() if packet[HTTPRequest].Path else ""
        url = f"http://{host}{path}"
        print(f"URL: {url}")


        if packet.haslayer(scapy.Raw):
            print("[+] Xom ma'lumotlar:")
            print(packet[scapy.Raw].load.decode(errors="ignore"))

# Windows uchun interfeysni tekshirib ishlatish
interface = "Wi-Fi"  # `Get-NetAdapter` orqali to‘g‘ri interfeys nomini tekshiring
sniff_packets(interface)
