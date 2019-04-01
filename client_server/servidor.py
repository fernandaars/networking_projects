#!/usr/bin/env python
'''
    Fernanda A. R. Silva
    Networking Systems Subject
    Computing Science Departament - UFMG
'''

import sys
import socket

MAX_CLIENTES = 10
MSG_TAMANHO_MAX = 100


class Server():
    def __init__(self, port, ip=""):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(address=(ip, port))
        self.s.listen(MAX_CLIENTES)
        self.counter = 0

    def run(self):
        while True:
            c, client = self.s.accept()
            print("Conectado a {}".format(client))

            while True:
                msg = c.recv(MSG_TAMANHO_MAX)
                if not msg:
                    break
                print("Msg recebida: {}".format(msg.decode("ascii")))

                nbytes = c.send(msg)
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
