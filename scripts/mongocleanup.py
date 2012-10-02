import re
import os

import pymongo
import codecs
from mongokit import Connection

MONGODB = "localhost:27017"


def get_mongo_connection(host=None, port=None):
    """ Open a connection to the MongoDB server """
    if not host and not port:
        try:
            host, port = MONGODB.split(':')
        except (AttributeError, ValueError):
            host, port = None, None

    if host and port:
        conn = Connection(host, int(port))
        return conn
    else:
        raise Exception("You need to configure the host and port "
                        "of the MongoDB document server")


def get_mongo_collection(collection='goals', database='nbsap',
                         host=None, port=None):
    conn = get_mongo_connection(host, port)
    db = conn[database]

    return db[collection]


def sanitizer(mycollection=None):
    try:
        collection = get_mongo_collection(mycollection)
    except TypeError:
        print 'Must provide a valid collection'

    try:
        collection.remove(safe=True)
    except pymongo.errors.OperationFailure:
        print 'Operational error when removing collection %s' % (mycollection)

if __name__ == "__main__":
    sanitizer(mycollection='actions')
    sanitizer(mycollection='objectives')
    sanitizer(mycollection='mapping')
