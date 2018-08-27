#!/usr/bin/env python3
# encoding: utf-8

import socket
import math
from struct import pack
from time import sleep, time
from lib.utils import random_id
from lib.bencode import bencode, bdecode


def send_packet(the_socket, msg):
    the_socket.send(msg)


def send_message(the_socket, msg):
    msg_len = pack('>I', len(msg))
    return the_socket.send(msg_len + msg)


def send_handshake(the_socket, h):
    bt_header = chr(len('BitTorrent protocol')) + 'BitTorrent protocol'
    ext_bytes = '\x00\x00\x00\x00\x00\x10\x00\x00'
    peer_id = random_id()
    the_socket.send(bt_header.encode('utf-8') + ext_bytes.encode('utf-8') + h + peer_id)


def check_handshake(packet, s):
    try:
        bt_header_len, packet = ord(packet[:1]), packet[1:]
        if bt_header_len != len('BitTorrent protocol'):
            return False
    except TypeError:
        return False

    bt_header, packet = packet[:bt_header_len], packet[bt_header_len:]
    if bt_header.decode('utf-8') != 'BitTorrent protocol':
        return False

    packet = packet[8:]
    h = packet[:20]
    return h == s


def send_ext_handshake(the_socket):
    msg = chr(20).encode('utf-8') + chr(0).encode('utf-8') + bencode({'m': {'ut_metadata': 1}})
    send_message(the_socket, msg)


def request_metadata(the_socket, ut_metadata, piece):
    msg = chr(20).encode('utf-8') + chr(ut_metadata).encode('utf-8') + bencode({'msg_type': 0, 'piece': piece})
    send_message(the_socket, msg)


def get_ut_metadata(data):
    ut_metadata = '_metadata'
    index = data.index(ut_metadata.encode('utf-8')) + len(ut_metadata) + 1
    return int(chr(int(data[index])))


def get_metadata_size(data):
    metadata_size = 'metadata_size'
    start = data.index(metadata_size.encode('utf-8')) + len(metadata_size) + 1
    data = data[start:]
    return int(data[:data.index('e'.encode('utf-8'))])


def get_whole_metadata(the_socket, timeout=5):
    the_socket.setblocking(0)
    total_data = []
    begin = time()
    while True:
        sleep(0.05)
        if total_data and time() - begin > timeout:
            break
        elif time() - begin > timeout * 2:
            break
        # noinspection PyBroadException
        try:
            data = the_socket.recv(1024)
            if data:
                total_data.append(data)
                begin = time()
        except Exception:
            pass
    return b''.join(total_data)


def download_metadata(address, infohash, timeout=5):
    the_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # noinspection PyBroadException
    try:
        the_socket.settimeout(5)
        the_socket.connect(address)
        send_handshake(the_socket, infohash)
        packet = the_socket.recv(4096)
        if not check_handshake(packet, infohash):
            return
        send_ext_handshake(the_socket)
        packet = the_socket.recv(4096)
        ut_metadata, metadata_size = get_ut_metadata(packet), get_metadata_size(packet)
        metadata = []
        for piece in range(int(math.ceil(metadata_size / (16.0 * 1024)))):
            request_metadata(the_socket, ut_metadata, piece)
            packet = get_whole_metadata(the_socket, timeout)
            metadata.append(packet[packet.index('ee'.encode('utf-8')) + 2:])
        metadata = bdecode(b''.join(metadata))
        if isinstance(metadata.get('name'), str):
            # MONGO.put(metadata, ''.join(['%02x' % x for x in infohash]).strip())
            print(metadata.get('name'))
    except Exception:
        return
    finally:
        the_socket.close()
