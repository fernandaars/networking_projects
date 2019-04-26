#!/usr/bin/env python
'''
    Fernanda A. R. Silva
    Networking Systems Subject
    Computing Science Departament - UFMG
'''

import sys
import socket
import struct

MSG_TAMANHO_MAX = 10000


class Client():

    def __init__(self, ip, port):
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.c.connect((str(ip), int(port)))

    def send_operation(self, operation, number):
        if(operation == "+"):
            client_msg = struct.pack("!?i", True, int(number))
        else:
            if(operation == "-"):
                client_msg = struct.pack("!?i", False, int(number))
            else:
                print("[+/-] [INTEIRO] \n")
        nbytes = self.c.send(client_msg)
        if nbytes != len(client_msg):
            print("Falha No Envio da Mensagem. \n")

    def receive_counter(self):
        self.c.settimeout(15.0)
        try:
            server_msg = self.c.recv(MSG_TAMANHO_MAX)
        except socket.timeout:
            return False
        if not server_msg:
            return False
        print(server_msg.decode("ascii"))
        return True

    def run(self):
        while True:
            try:
                client_msg = input("")
            except EOFError:
                break
            operation, number = client_msg.split(" ")
            self.send_operation(operation, number)
            if self.receive_counter() is False:
                break

    def close(self):
        self.c.close()


if __name__ == '__main__':
    if len(sys.argv) == 3:
        client = Client(sys.argv[1], sys.argv[2])
        client.run()
        client.close()
    else:
        print("Número de Argumentos Inválidos. \n")
        print("python3.5 cliente.py [IP] [PORTA] \n")
