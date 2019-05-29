#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
##############################################################
##**********************************************************##
##***         FEDERAL UNIVERSITY OF MINAS GERAIS         ***##
##***             COMPUTER SCIENCE DEPARTMENT            ***##
##***                                                    ***##
##***           Author: Fernanda Aparecida R. Silva      ***##
##***                                                    ***##
##**********************************************************##
##############################################################
'''

# Imports
import sys
import json
# import numpy
# import struct
import socket
# import logging
# --

# Variables Defined By The Especification
__port__ = 5151
__network__ = "127.0.1.0"
__interface__ = "lo"
__json_labels__ = ("type", "source", "destination")
__network_mask__ = 24
__MAX_CLIENTES__ = 10
__message_types__ = ("data", "update", "trace", "table")
__MSG_TAMANHO_MAX__ = 100
__acepted_commands__ = ("add", "del", "table", "trace", "quit")
__command_to_add_interfaces__ = "ip addr add <ip>/<prefixlen> dev <interface>"
# --


class Message:
    message = ""

    def __init__(self, type, log, args):
        data = {}
        if type in __message_types__:
            data['type'] = type
            for index in args:
                data[index] = args[index]
            json_data = json.dumps(data)
            self.message = json_data
        else:
            print(log)


class RoutingTable:
    routing_table = {"127.0.1.2": {"127.0.1.4": 10}}

    def __init__(self, input_file):
        if input_file is None:
            return
        try:
            file_pointer = open(input_file, "r")
        except IOError:
            print("log")
        lines = file_pointer.readlines()
        for line in lines:
            print("ei")
            args = line.split(" ")
            if(args[0] == "add"):
                self.add_route(args[1], args[2], None)
            if(args[1] == "del"):
                self.del_route(args)

    def add_route(self, ip, weigth, router):
        if(router is None):
            router = ip
        if (ip in self.routing_table) is False:
            self.routing_table[ip] = {router: weigth}
        else:
            routes = self.routing_table[ip]
            routes[router] = weigth
            self.routing_table[ip] = routes

    def del_route(self, ip):
        del self.routing_table[ip]
        for route in self.routing_table:
            routers = self.routing_table[route]
            for router in routers:
                if(routers[router] == ip):
                    del routers[router]
            self.routing_table[route]


class Router:
    def __init__(self, ip):
        self.address = (ip, __port__)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(self.address)

    def send_message(self, address, message):
        response = self.s.sendto(message.encode("ascii"), (address, __port__))
        if response != len(message):
            print("log")
            return False
        return True

    def receive_message(self):
        message, address = self.s.recvfrom(__MSG_TAMANHO_MAX__)
        if message is None:
            print("log")
            return False
        message = message.decode("ascii")
        print(message)
        return True

    def close(self):
        self.s.close()


if __name__ == "__main__":
    address = sys.argv[1]
    period = float(sys.argv[2])
    input_file = None
    if len(sys.argv) == 4:
        input_file = sys.argv[3]

    r = RoutingTable(input_file)

    '''
    r.add_route("1.1.1.1", 9999, None)
    print(json.dumps(r.routing_table))
    r2 = Router(address)
    m = Message("data", "log", {"dede": "2"})
    r2.send_message(address, m.message)
    r2.receive_message()
    '''

