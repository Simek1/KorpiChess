import socket
import threading


def connect_to_server(serverport, serverip, nick):
    global client
    client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect((serverip, int(serverport)))
    send(nick)
    
def send(msg):
    msg=msg.encode('utf-8')
    msg_length=str(len(msg)).encode("utf-8")
    msg_length+= b' '*(64-len(msg_length))
    client.send(msg_length)
    client.send(msg)

    
def download_msg(newmsg):
    while True:
        bytes_of_msg=client.recv(64).decode('utf-8')
        new_msg=client.recv(int(bytes_of_msg))
        new_msg=new_msg.decode('utf-8')
        newmsg.append(new_msg)
        if new_msg=="!@#disc#@!":
            client.close()
            try:
                print("POŁĄCZENIE Z SERWEREM ZOSTAŁO ZAMKNIĘTE\n")
            except:
                pass
            break
        else:
            print(new_msg)