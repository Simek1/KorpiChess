import socket
import threading
from requests import get

def start_server(port, serverip):
	global serverThread, server, sport, sip
	print(port, serverip)
	sport=int(port)
	sip=serverip
	print("Tworzenie serwera")
	server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((serverip, sport))
	serverThread=threading.Thread(target=start)
	serverThread.start()

def start():
	global runn
	print("Server został uruchomiony i czeka na połączenie")
	server.listen()
	runn=True
	while runn:
		try:
			con, addres= server.accept()
			print(f"{addres} połączył się")
			users.append(con)
			addreses.append(addres)
			cn= threading.Thread(target=connection, args=(con, addres))
			cn.start()
		except:
			break