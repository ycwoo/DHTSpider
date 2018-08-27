#!/usr/bin/env python3
# encoding: utf-8

from hashlib import sha1
from struct import unpack
from random import randint
from threading import Timer
from socket import inet_ntoa


def entropy(length):
    return ''.join(chr(randint(0, 255)) for _ in range(length))


def random_id():
    h = sha1()
    h.update(entropy(20).encode('utf-8'))
    return h.digest()


def decode_nodes(nodes):
    n = []
    length = len(nodes)
    if (length % 26) != 0:
        return n
    for i in range(0, length, 26):
        nid = nodes[i:i + 20]
        ip = inet_ntoa(nodes[i + 20:i + 24])
        port = unpack('!H', nodes[i + 24:i + 26])[0]
        n.append((nid, ip, port))
    return n


def timer(t, f):
    Timer(t, f).start()


def get_neighbor(target, nid, end=10):
    return target[:end] + nid[end:]
