#!/usr/bin/env python
'''
    Fernanda A. R. Silva
    Networking Systems Subject
    Computing Science Departament - UFMG
'''

import sys
import struct
import socket

MAX_CLIENTES = 10
MSG_TAMANHO_MAX = 10000


class Server():
    def __init__(self, ip, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((ip, int(port)))
        self.s.listen(MAX_CLIENTES)

        self.lower_limit = 0
        self.global_counter = 0
        self.upper_limit = 999999

    def update_counter(self, operation, num):
        if(operation is True):
            self.global_counter = self.global_counter + num
        else:
            self.global_counter = self.global_counter - num

    def receive_operation(self, client_socket, client):
        msg = client_socket.recv(MSG_TAMANHO_MAX)
        operation, number = struct.unpack("!?i", msg)
        self.update_counter(operation, number)

    def send_counter(self, client_socket, client):
        msg = struct.pack("!I", self.global_counter)
        nbytes = client_socket.send(msg)
        return True

    def run(self):
        while True:
            client_socket, client = self.s.accept()
            while True:
                if self.receive_operation(client_socket, client) is False:
                    break
                if self.send_counter(client_socket, client) is False:
                    break

    def close(self):
        self.s.close()


if __name__ == '__main__':

    if(len(sys.argv) == 2):
        server = Server("", sys.argv[1])
        server.run()
        server.close()
    else:
        if(len(sys.argv) == 3):
            server = Server(sys.argv[1], sys.argv[2])
            server.run()
            server.close()
        else:
            print("Número de Argumentos Inválidos. \n") 
            print("python3.6 servidor.py <IP> [PORTA] \n")
