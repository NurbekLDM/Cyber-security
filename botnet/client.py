import socket
import json
import os
import psutil
import time
import logging
# Logging sozlamalari
logging.basicConfig(filename='client_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
# Client sozlamalari
HOST = '127.0.0.1'
PORT = 9999
def execute_command(command):
	cmd_type = command.get("type")
	if cmd_type == "create_file":
		filename = command.get("filename")
		content = command.get("content")
		try:
			with open(filename, 'w') as f:
				f.write(content)
			logging.info(f"Fayl yaratildi: {filename}")
			return f"Fayl yaratildi: {filename} (Ransomware simulyatsiyasi)"
		except Exception as e:
			logging.error(f"Fayl yaratishda xato: {str(e)}")
			return f"Fayl yaratishda xato: {str(e)}"
	elif cmd_type == "send_message":
		message = command.get("message")
		logging.info(f"Xabar qabul qilindi: {message}")
		return f"Xabar qabul qilindi: {message}"
	elif cmd_type == "check_status":
		cpu_usage = psutil.cpu_percent()
		memory = psutil.virtual_memory().percent
		disk = psutil.disk_usage('/').percent
		status = f"Bot holati: CPU={cpu_usage}%, Xotira={memory}%, Disk={disk}%"
		logging.info(status)
		return status + " (Ma’lumot o‘g‘irlash simulyatsiyasi)"
	elif cmd_type == "simulate_ddos":
		target = command.get("target")
		count = command.get("count")
		logging.info(f"DDoS simulyatsiyasi: {count} so‘rov {target} ga")
		return f"DDoS simulyatsiyasi: {count} so‘rov {target} ga (Haqiqiy hujum emas)"
	return "Noma‘lum buyruq"
def main():
	global client
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	while True:
		try:
			client.connect((HOST, PORT))
			logging.info(f"Ulandi: {HOST}:{PORT}")
			print(f"[Ulandi] Server: {HOST}:{PORT}")
			break
		except:
			logging.warning("Ulanish xatosi, qayta urinish...")
			print("[Ulanish xatosi] Qayta urinish...")
			time.sleep(2)

	while True:
		try:
			message = client.recv(1024).decode('utf-8')
			if message:
				command = json.loads(message)
				result = execute_command(command)
				client.send(result.encode('utf-8'))
		except:
			logging.error("Server bilan aloqa uzildi")
			print("[Xato] Server bilan aloqa uzildi")
			client.close()
			break

if __name__ == "__main__":
	main()
