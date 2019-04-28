#!/usr/bin/env python
'''
    Fernanda A. R. Silva
    Networking Systems Subject
    Computing Science Departament - UFMG
'''

import sys
import struct
import socket

SOF_16_Base = 0xcc
EOF_16_Base = 0xcd
MSG_TAMANHO_MAX = 10000

class Data_Encoding():
    def encode16(Array_bytes):
        base16 = ""
        for binary in Array_bytes:
            hexa = hex(int(binary, 2))
            temp = hexa.lstrip('0x')
            #print(temp)
            if len(temp) < 2:
                zero = "0"
                temp = zero + temp
                #print("Precisou completar: ",temp)
            base16 = base16 + temp
        return base16

    def decode16(string):
        return bytes.fromhex(string).decode('ascii')


class Data_Framing():
    def insert_DLE(string, index):
        return string[:index] + '1b' + string[index:]

    def findDLE(dado):
        start = 0
        ind = 0
        while ind!=-1:
            if start < len(dado):
                ind = dado.find("1b", start)
                print(ind)
                if ind != -1:
                    dado = insert_DLE(dado, ind)
                    print(dado)
                    start = ind + 4
            else:
                ind = -1
        return dado

    def findEOF(dado):
        start = 0
        ind = 0
        while ind!=-1:
            if start < len(dado):
                ind = dado.find("cd", start)
                print(ind)
                if ind != -1:
                    dado = insert_DLE(dado, ind)
                    print(dado)
                    start = ind + 4
            else:
                ind = -1
        return dado

    def framing(ID, flags, checksum, dados):
        frame = "cc"
        frame = frame + ID + flags + checksum + dados + "dc"
        return frame

#class Error_Detection():
#class Data_Sequencing():
#class Data_Transmission():

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