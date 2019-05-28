# Routing Protocol Based on Distance Vector
An implementation of a virtual topology of routers, where the routers use a routing protocol based on a distance vector.

# How to Run

To run this program, you should call it like this:

```bash
$ ./router.py <ADDR> <PERIOD> [STARTUP]
```
**<ADDR>** is the IP address to be binded.
**<PERIOD>** is the period of time between the update messages.
**[STARTUP]** is a file with the start configuration of the topology.

You can also call the Python program directly from the src directory. For that, use this command:

```bash
$ python src/router.py <ADDR> <PERIOD> [STARTUP]
```

# Commands

* **add**: add a route with the given weight to the given ip.
```bash
$ add <ip> <weight>
```

* **del**: del the route with the given ip.
```bash
$ del <ip>
```
* **table**: show the routing table.
```bash
$ table
```
* **trace**: count the number os hops between two routers.
```bash
$ trace <ip>
``` 

* **quit**: quit the program.
```bash
$ quit
```
