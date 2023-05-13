import socket
import threading
from requests import get

users=[]
addreses=[]
nicks={}

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
			if len(users)<2:
				con, addres= server.accept()
				print(f"{addres} połączył się")
				users.append(con)
				addreses.append(addres)
				cn= threading.Thread(target=connection, args=(con, addres))
				cn.start()
		except:
			break

#######
def connection(con, addres):
    connected=True
    nick_seted=0
    while connected:
        bytes_of_msg=con.recv(64).decode('utf-8') #Ile bajtów będzie miala wiadomosc którą otrzymamy
        if bytes_of_msg and len(users)>0: #pominiecie pierwszej pustej "wiadomosci"
            if nick_seted:#pierwsza "wiadomoscia" ma byc nick uzytkownika
                nick=nicks[addreses[users.index(con)]]
                print(nick)
                msg=con.recv(int(bytes_of_msg)).decode('utf-8')
                if msg=="!@#disc#@!": #Rozlaczenie clienta z serverem
                    connected=False
                    disc_msg="!@#disc#@!"
                    disc_msg=disc_msg.encode('utf-8')
                    disc_length=str(len(disc_msg)).encode("utf-8")
                    disc_length+= b' '*(64-len(disc_length))
                    con.send(disc_length)
                    con.send(disc_msg)
                    msg="ROZŁĄCZYŁ SIĘ"
                    delindex=users.index(con)
                    del(users[delindex])
                    del(addreses[delindex])
                    del(nicks[addres])
                    con.close()
                msg=f'<{nick}>: '+msg
                print(f"{nick}: {msg}")
                msg=msg.encode('utf-8')
                msg_length=str(len(msg)).encode("utf-8")
                msg_length+= b' '*(64-len(msg_length))
                for x in users:
                    x.send(msg_length)
                    x.send(msg)
            else:
                msg=con.recv(int(bytes_of_msg)).decode('utf-8')
                nicks[addres]=msg
                nick_seted=1               
                notification=f"<SERVER>: {msg} połączył się."
                notification=notification.encode('utf-8')
                not_length=str(len(notification)).encode("utf-8")
                not_length+= b' '*(64-len(not_length))
                print(f"{msg} polaczyl sie.")
                for x in users:
                    x.send(not_length)
                    x.send(notification)
######

def close_server():
    global server, runn, sip, sport, users, addreses, nicks
    notification="<SERVER>: Server został wyłączony."
    notification=notification.encode('utf-8')
    not_length=str(len(notification)).encode("utf-8")
    not_length+= b' '*(64-len(not_length))
    disc_msg="!@#disc#@!"
    disc_msg=disc_msg.encode('utf-8')
    disc_length=str(len(disc_msg)).encode("utf-8")
    disc_length+= b' '*(64-len(disc_length))
    for x in users:
        x.send(not_length)
        x.send(notification)
        x.send(disc_length)
        x.send(disc_msg)
    runn=False
    #server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if sip=="0.0.0.0":
        sip=socket.gethostbyname(socket.gethostname())
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect( (sip, sport))
    server.close()
    users=[]
    addreses=[]
    nicks={}