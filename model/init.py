#!/usr/bin/env python3
# coding=utf-8

from mongoengine import register_connection


def database_initialize():
    """
    初始化数据库
    :return:
    """
    register_connection('dht', 'dht')
