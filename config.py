#!/usr/bin/env python3
# encoding: utf-8

import os


class Config(object):
    BOOTSTRAP_NODES = (
        ('router.bittorrent.com', 6881),
        ('dht.transmissionbt.com', 6881),
        ('router.utorrent.com', 6881)
    )
    REJOIN_DHT_INTERVAL = 3  # 掉线后重新加入DHT网络的时间间隔
    BIND_IP = '0.0.0.0'
    BIND_PORT = 6881
    MAX_NODE_SIZE = int(os.environ.get('MAX_NODE_SIZE', '1000'))
    DOWNLOAD_THREAD = int(os.environ.get('DOWNLOAD_THREAD', '1000'))
    MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
    MONGO_PORT = int(os.environ.get('MONGO_PORT', '27017'))
