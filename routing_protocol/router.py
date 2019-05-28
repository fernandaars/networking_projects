# Imports
import sys
import json
import numpy
import struct
import socket
import logging
# --

# Variables Defined By The Especification
__network__ = "127.0.1.0"
__interface__ = "lo"
__json_labels__ = ("type", "source", "destination")
__network_mask__ = 24
__message_types__ = ("data", "update", "trace", "table")
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
    table_labels = ("destination", "router", "network_mask", "weigth", "ref",
                    "use", "iface")
    table = numpy.zeros((16, len(table_labels)))

    def __init__(self):
        print(self.table)


if __name__ == "__main__":
    args = {"iphone": 2007,
            "iphone 3G": 2008,
            "iphone 3GS": 2009,
            "iphone 4": 2010,
            "iphone 4S": 2011,
            "iphone 5": 2012,
            "source": 2,
            "destination": 3}
    m = Message("data", "log", args)
    r = RoutingTable()
    print(m.table)
