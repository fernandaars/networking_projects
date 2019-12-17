#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
##############################################################
##**********************************************************##
##***         FEDERAL UNIVERSITY OF MINAS GERAIS         ***##
##***             COMPUTER SCIENCE DEPARTMENT            ***##
##***                                                    ***##
##***         Author: Fernanda Aparecida R. Silva        ***##
##***                                                    ***##
##**********************************************************##
##############################################################
'''

# Imports
import sys
import json
import timer
# import numpy
# import struct
import socket
import logging
import threading
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
    def create_message(type, source, destination, args):
        data = {}
        if type in __message_types__:
            data["type"] = type
            data["source"] = source
            data["destination"] = destination
            for index in args:
                data[index] = args[index]
            data = json.dumps(data)
            json_obj = json.loads(data)
            return json_obj
        else:
            logging.warning("Empty Message Created.")
            return None

    def get_value_from_massage(key, message):
        content = json.dumps(message)
        return content[key]


class RoutingTable:
    routing_table = {"127.0.1.2": {"127.0.1.4": 10,
                                   "127.0.1.6": 12},
                     "135.929.929": {"111.111.111.11": 2}}

    def __init__(self, input_file):
        if input_file is None:
            return
        try:
            file_pointer = open(input_file, "r")
        except IOError:
            logging.warning("Statup File Doesn't Exist.")
            return
        lines = file_pointer.readlines()
        for line in lines:
            line = line.replace('\n', "")
            args = line.split(" ")
            if(args[0] == "add"):
                self.add_route(args[1], args[2], None)
            if(args[1] == "del"):
                self.del_route(args)
        file_pointer.close()

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
                if(router == ip):
                    del routers[router]
            self.routing_table[route]

    def format(self):
        routing_table_message = []
        for route in self.routing_table:
            routers = self.routing_table[route]
            for router in routers:
                routing_table_message.append((str(route), str(router),
                                              routers[router]))
        return str(routing_table_message)


class Router:
    def __init__(self, ip):
        self.ip = ip
        self.address = (ip, __port__)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(self.address)

    def send_message(self, address, message):
        response = self.s.sendto(message.encode("ascii"), (address, __port__))
        if response != len(message):
            logging.warning("Error in The Sending of a Message.")
            return False
        print(Message.get_value_from_massage("payload", message))
        return True

    def receive_message(self):
        message, address = self.s.recvfrom(__MSG_TAMANHO_MAX__)
        if message is None:
            logging.warning("Error in The Receiving of a Message.")
            return False
        message = message.decode("ascii")
        print(message)
        return True

    def send_table(self, ip, routing_table):
        message_content = {"payload": routing_table.format()}
        message = Message.create_message("data", self.ip, ip, message_content)
        print(message)
        next_router = self.find_next_router(ip, routing_table)
        self.send_message(next_router, message)

    def send_trace(self, ip, routing_table):
        message_content = {"hops": [str(self.ip)]}
        message = Message.create_message("trace", self.ip, ip, message_content)
        next_router = self.find_next_router(ip, routing_table)
        self.send_message(next_router, message)

    def upload_trace(self, ip, routing_table, trace_message):
        hops = trace_message["hops"]
        hops.append(self.ip)
        trace_message["hops"] = hops
        if trace_message["destination"] == self.ip:
            next_router = (hops[-2], __port__)
        else:
            next_router = self.find_next_router(ip, routing_table)
        self.send_message(next_router, trace_message)

    def find_next_router(self, ip, routing_table):
        route = routing_table.routing_table[ip]
        if len(route) > 1:
            route = min(route.items(), key=lambda x: x[1])
        return (route[0], __port__)

    def request_message(self, ip, routing_table, type, args):
        message_content = None
        if type == "data":
            message_content = {"distances": {"127.0.1.4": 10, "127.0.1.5": 0,
                                             "127.0.1.2": 10, "127.0.1.3": 10}}
        message = Message.create_message(type, self.ip, ip, message_content)
        self.send_message(ip, message)

    def close(self):
        self.s.close()


known_routers = []
distance_vector = []

if __name__ == "__main__":
    logging.basicConfig(filename='router_fernanda.log', filemode='w',
                        format='%(asctime)s - %(levelname)s - %(message)s')
    address = sys.argv[1]
    period = float(sys.argv[2])
    input_file = None
    if len(sys.argv) == 4:
        input_file = sys.argv[3]

    r_table = RoutingTable(input_file)
    router = Router(address)
    # threading.Thread(.start()

    while True:
        try:
            command = input()
        except (KeyboardInterrupt, EOFError) as e:
            logging.debug("Good Bye!")
            router.close()
            exit()
        command_args = command.split(" ")
        if command_args[0] in __acepted_commands__:
            if(command_args[0] == "add"):
                r_table.add_route(command_args[1], command_args[2], None)
            if(command_args[0] == "del"):
                r_table.del_route(command_args[1])
            if(command_args[0] == "table"):
                router.send_table(command_args[1], r_table)
            if(command_args[0] == "trace"):
                router.send_trace(command_args[1], r_table)
            if(command_args[0] == "quit"):
                logging.debug("Good Bye!")
                exit()
        else:
            logging.warning("Command Invalid!")
