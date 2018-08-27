#!/usr/bin/env python3
# encoding: utf-8

import pymongo
from time import time
from config import Config
from lib.filetype import get_file_type


class MongoManager(object):
    def __init__(self):
        self._c = pymongo.MongoClient(host=Config.MONGO_HOST,
                                      port=Config.MONGO_PORT,
                                      connect=False)['dht']['hashset']

    def put(self, metadata, h):
        utf8_enable = False
        files = []
        # noinspection PyBroadException
        try:
            bare_name = metadata.get('name')
        except KeyError:
            bare_name = metadata.get('name.utf-8')
            utf8_enable = True
        except Exception:
            return
        if 'files' in metadata:
            for x in metadata.get('files'):
                files.append({'n': '/'.join(x.get('path.utf-8' if utf8_enable else 'path')),
                              'l': x.get('length')})
        else:
            files.append({'n': bare_name,
                          'l': metadata.get('length')})
        self._c.update(
            {'_id': h},
            {'$setOnInsert': {
                    'n': bare_name,
                    'd': int(time()),
                    '_id': h,
                    'l': sum(map(lambda y: y.get('l'), files)),
                    's': len(files),
                    'e': 1,
                    'f': files,
                    't': get_file_type(files)},
                '$set': {'m': int(time())},
                '$inc': {'c': 1}},
            upsert=True)


MONGO = MongoManager()
