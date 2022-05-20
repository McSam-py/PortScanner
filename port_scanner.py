import socket 
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
open_ports = []
closed_ports = []


def port_analysis_display():
	print(f'''
[+] OPEN PORT(S): {len(open_ports)}\n------------------------------------''')
	for i in open_ports:
		try:
			service_name = socket.getservbyport(int(i),"tcp")
		except OSError:
			service_name = "UNKOWN"
		print(f"PORT ==> {i}, SERVICE ==> {service_name}")

	print(f'''
		\n[-] CLOSED PORT(S): {len(closed_ports)}\n---------------------------------''')
	for i in closed_ports:
		print(i)

def portscanner(host, port_number):
	global open_ports, closed_ports
	try:
		sock.settimeout(1)
		if sock.connect_ex((host, port_number)):
			closed_ports.append(str(port_number))
		else:
			open_ports.append(str(port_number))



	except OverflowError:
		print("\nPORT number is out of range.")


def get_port_number(lhost, port):
	if "-" in port:
		portmax = int(port.split("-")[1])
		portmin = int(port.split("-")[0])
		print("[+] Scanning target.....")
		threads = []

		for i in range(portmin, portmax+1):
			thread = threading.Thread(target=portscanner, args=(lhost, i),)
			threads.append(thread)

		for i in range(len(threads)):
			threads[i].start()
		port_analysis_display()

	else:
		portscanner(lhost, int(port))
		port_analysis_display()

def main():
	print("Enter Host IP address.")
	host = str(input(" > "))

	print("Enter PORT number or range (Example: 1-200).")
	port = str(input(" > "))
	get_port_number(host, port)



main()
