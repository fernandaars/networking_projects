#!/usr/bin/env python
'''
    Fernanda A. R. Silva
    Networking Systems Subject
    Computing Science Departament - UFMG
'''

import sys
import socket

MSG_TAMANHO_MAX = 10000


class Client():
    def __init__(self, ip, port):
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.c.connect((ip, port))

    def run(self):
        while True:
            msg = input("Msg: ").encode("ascii")
            nbytes = self.c.send(msg)
            if nbytes != len(msg):
                print("Falhou ao enviar a mensagem")
                break

            msg = self.c.recv(MSG_TAMANHO_MAX)
            if not msg:
                print("Falhou para receber uma mensagem")
                break
            print("Msg recebida:")
            # " {}".format(msg.decode("ascii")))
            if msg.decode("ascii") == "tchau":
                break

    def close(self):
        self.c.close()


if __name__ == '__main__':
    if len(sys.argv) == 3:
        client = Client(sys.argv[1], int(sys.argv[2]))
    else:
        print("Number of Arguments Invalid.")
    client.run()
    client.close()
