#!/usr/bin/env python
'''
    Fernanda A. R. Silva
    Networking Systems Subject
    Computing Science Departament - UFMG
'''

import sys
import socket

MAX_CLIENTES = 10
MSG_TAMANHO_MAX = 10000


class Server():
    def __init__(self, port, ip=""):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((ip, port))
        self.s.listen(MAX_CLIENTES)

        self.lower_limit = 0
        self.global_counter = 0
        self.upper_limit = 999999

    def update_counter(self, operation, num):
        res = 0
        if(operation == 0):
            res = self.global_counter - num
            if(res < 0):
                res = self.upper_limit - num
        else:
            if(operation == 1):
                res = self.global_counter + num
                if(res < 0):
                    res = self.upper_limit + num
        if(res > self.upper_limit + 1):
            res = res - (self.upper_limit + 1)
        self.global_counter = res

    def run(self):
        while True:
            c, client = self.s.accept()
            while True:
                msg = c.recv(MSG_TAMANHO_MAX)
                if not msg:
                    break
                print("Msg recebida: {}".format(msg.decode("ascii")))
                self.update_counter(operation = 0, num = -2)

                nbytes = c.send(str(self.global_counter))
                if nbytes != len(msg):
                    break

                if msg.decode("ascii") == "tchau":
                    break

    def close(self):
        self.s.close()


if __name__ == '__main__':

    if(len(sys.argv) == 2):
        server = Server(int(sys.argv[1]))
    else:
        if(len(sys.argv) == 3):
            server = Server(str(sys.argv[1]), str(sys.argv[2]))
        else:
            print("Number of Arguments Invalid.")
    server.run()
    server.close()
