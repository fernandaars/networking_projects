#!/usr/bin/env python
'''
    Fernanda A. R. Silva
    Networking Systems Subject
    Computing Science Departament - UFMG
'''

import sys
import struct
import socket

MSG_TAMANHO_MAX = 10000


class Client():
    def __init__(self, ip, port):
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.c.connect((ip, int(port)))

    def send_operation(self):
        msg = input("")
        operation, number = msg.split(" ")
        client_msg = struct.pack("!?i", bin(1), int(0))

        if(operation == "+"):
            client_msg = struct.pack("!?i", bin(1), int(number))
        if(operation == "-"):
            client_msg = struct.pack("!?i", bin(0), int(number))

        nbytes = self.c.send(client_msg)

    def receive_counter(self):
        server_msg = self.c.recv(MSG_TAMANHO_MAX)
        counter = str(struct.unpack("!I", server_msg)[0])
        print(counter)

    def run(self):
        while True:
            self.send_operation()
            self.receive_counter()

    def close(self):
        self.c.close()


if __name__ == '__main__':
    if len(sys.argv) == 3:
        client = Client(sys.argv[1], sys.argv[2])
        client.run()
        client.close()
    else:
        print("Número de Argumentos Inválidos. \n") 
        print("python3.6 cliente.py [IP] [PORTA] \n")
