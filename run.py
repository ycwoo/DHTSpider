#!/usr/bin/env python3
# encoding: utf-8

from dht import DHTServer


if __name__ == "__main__":
    dht = DHTServer()
    dht.start()
    dht.auto_send_find_node()
