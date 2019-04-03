#!/usr/bin/env python
'''
    Fernanda A. R. Silva
    Networking Systems Subject
    Computing Science Departament - UFMG
'''

import sys
import socket
import struct

MAX_CLIENTES = 10
MSG_TAMANHO_MAX = 10000


class Server():
    def __init__(self, ip, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((str(ip), int(port)))
        self.s.listen(MAX_CLIENTES)

        self.lower_limit = 0
        self.global_counter = 0
        self.upper_limit = 1000000

    def update_counter(self, operation, num):
        res = 0
        if(operation == 0):
            res = self.global_counter - num
        else:
            if(operation == 1):
                res = self.global_counter + num

        if(res < self.lower_limit):
            res += self.upper_limit
        if(res >= self.upper_limit):
            res = res - self.upper_limit
        self.global_counter = res

    def receive_operation(self, client_socket, client):
        client_socket.settimeout(15.0)
        client_msg = client_socket.recv(MSG_TAMANHO_MAX)
        if not client_msg:
            return False
        else:
            operation, number = struct.unpack("!?i", client_msg)
            self.update_counter(operation, number)
        return True

    def send_counter(self, client_socket):
        server_msg = struct.pack("!I", self.global_counter)
        nbytes = client_socket.send(server_msg)
        if nbytes != len(server_msg):
            print("Falha No Envio da Mensagem. \n")
            return False
        return True

    def run(self):
        while True:
            client_socket, client = self.s.accept()
            while True:
                if(self.receive_operation(client_socket, client) is False):
                    break
                if(self.send_counter(client_socket) is False):
                    break

    def close(self):
        self.s.close()


if __name__ == '__main__':

    if(len(sys.argv) == 2):
        try:
            server = Server("", sys.argv[1])
            server.run()
            server.close()
        except KeyboardInterrupt:
            exit(1)
    else:
        if(len(sys.argv) == 3):
            try:
                server = Server(sys.argv[1], sys.argv[2])
                server.run()
                server.close()
            except KeyboardInterrupt:
                exit(2)
        else:
            print("Número de Argumentos Inválidos. \n")
            print("python3.5 servidor.py <IP> [PORTA] \n")
