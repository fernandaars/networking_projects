#!/usr/bin/env python
'''
    Fernanda A. R. Silva
    Ketlyn C. Sena de Castro
    Networking Systems Subject
    Computing Science Departament - UFMG
'''

import sys
# import struct
import socket
# import threading

DLE_16_Base = "1b"
SOF_16_Base = "cc"
EOF_16_Base = "cd"
MAX_CLIENTES = 100
MSG_TAMANHO_MAX = 10000
CONFIRMATION_FRAME = "aaaaaaaaaaaaaaa"
FRAME_EXAMPLE = "cc007fae2d01020304cd"


class DataEncoding():
    def encode_16(self, bytes_array):
        base16 = ""
        for binary in bytes_array:
            hexa = hex(int(binary, 2))
            temp = hexa.lstrip('0x')
            if len(temp) < 2:
                zero = "0"
                temp = zero + temp
            base16 = base16 + temp
        return base16

    def pre_encode(self, lista):
        size = len(lista)
        bytes_array = []
        for i in range(0, size):
            num = bin(lista[i])
            num = num.replace("0b", "")
            bytes_array.append(num)
        return bytes_array

    def decode_16(self, string):
        size = len(string)
        lista = []
        i = 0
        while i < size:
            s = string[i:i + 2]
            i = i + 2
            lista.append(int(s, 16))
        return lista

    def saidaDado(self, lista):
        size = len(lista)
        dado = lista[5:size - 1]

        size = len(dado)
        frase = ""
        for i in range(0, size):
            frase = frase + chr(dado[i])
        return frase

class DataFraming():
    def calculate_checksum(self, frame):
        size = len(frame)
        x = 0
        soma = 0
        while size > 1:
            b1 = frame[x]
            b2 = frame[x + 1]
            soma = soma + (b1 << 8) + b2
            size = size - 2
            x = x + 2

        if size > 0:
            soma = soma + frame[x]

        while (soma >> 16):
            soma = (soma & 0xffff) + (soma >> 16)

        soma = 0xffff - soma
        b1 = soma >> 8
        b2 = soma & 0xff

        return b1, b2

    def convertInt(self, lista):
        size = len(lista)
        inteiros = []
        for x in range(0, size):
            num = int(lista[x], 2)
            inteiros.append(num)
        return inteiros  

    def byte_stuffing(self, lista):
        size = len(lista)
        i = 0
        while i < size:
            if lista[i] == 27 or lista[i] == 205:
                lista.insert(i, 27)
                i = i + 2
                size = size + 1
            else:
                i = i + 1
        return lista

    def undo_byte_stuffing(self, lista):
        size = len(lista)
        i = 0
        while i < size:
            if lista[i] == 27:
                lista.pop(i)
                size = size - 1
            i = i + 1
        return lista

    def framing(self, lista, ID, FLAG, checksum1, checksum2):
        lista.append(205)
        lista.insert(0, checksum2)
        lista.insert(0, checksum1)
        lista.insert(0, FLAG)
        lista.insert(0, ID)
        lista.insert(0, 204)
        return lista

    def set_checksum(self, lista, byte1, byte2):
        lista[3] = byte1
        lista[4] = byte2
        return lista

    def set_id(self):
        return 1

    def set_flag(self):
        return 7


class SocketExtended():
    def __init__(self, type, ip, port):
        if(type == "client"):
            self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.c.connect((ip, int(port)))
        if(type == "server"):
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind((ip, int(port)))
            self.s.listen(MAX_CLIENTES)
            self.c, self.client = self.s.accept()

    def send_frame(self, frame):
        self.c.send(frame.encode("ascii"))

    def receive_frame(self):
        frame = self.c.recv(MSG_TAMANHO_MAX)
        print(str(frame.decode("ascii")))

    def send_confirmation(self):
        self.c.send(CONFIRMATION_FRAME.encode("ascii"))

    def receive_confirmation(self):
        frame = self.c.recv(MSG_TAMANHO_MAX)
        print(str(frame.decode("ascii")))

    def close(self):
        self.c.close()
        self.s.close()


class Data_Transmission():
    count_ativo = 0
    count_passivo = 0

    def __init__(self, type, ip, port, input_file, output_file):
        try:
            self.input_pointer = open(input_file, "r")
            self.output_pointer = open(output_file, "w")
        except OSError as e:
            print("Error in The File Openning" + str(e))

        self.socket_object = SocketExtended(type, ip, port)

    def active_transmission(self):
        print("Active Count: " + str(self.count_ativo))
        self.count_ativo += 1
        self.socket_object.send_frame(FRAME_EXAMPLE)
        # line = self.input_pointer.readline()
        # while (line):
        #     response = self.socket_object.send_frame()
        #     if(response is True):
        #         break
        #     self.socket_object.receive_confirmation()
        #     line = self.input_pointer.readline()

    def passive_transmission(self):
        print("Passive Count: " + str(self.count_passivo))
        self.count_passivo += 1
        self.socket_object.receive_frame()
        # client_socket, client = self.socket_object.accept()
        # while True:
        #     line = self.socket_object.receive_frame(client_socket, client)
        #     if(line is None):
        #         break
        #     if self.socket_object.send_confirmation(client_socket,
        #                                             client) is False:
        #         break
        #     self.output_pointer.write(line)

    def close_transmission(self):
        self.input_pointer.close()
        self.output_pointer.close()
        self.socket_object.close()


if __name__ == '__main__':
    executable_name = str(sys.argv[0])
    param = str(sys.argv[1])
    input_file = str(sys.argv[3])
    output_file = str(sys.argv[4])

    if(param == "-c"):
        ip, port = str(sys.argv[2]).split(":")
        t = Data_Transmission("client", ip, port, input_file, output_file)
        t.active_transmission()

    if(param == "-s"):
        ip = ""
        port = sys.argv[2]
        t = Data_Transmission("server", ip, port, input_file, output_file)
        t.passive_transmission()
