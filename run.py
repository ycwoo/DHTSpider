#!/usr/bin/env python3
# encoding: utf-8

from dht import DHTServer
from model.init import database_initialize


if __name__ == "__main__":
    database_initialize()
    dht = DHTServer()
    dht.start()
    dht.auto_send_find_node()
