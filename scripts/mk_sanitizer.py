import codecs
import os
import pymongo

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
        raise Exception('You need to configure the host and port '
                        'of the MongoDB document server')


def get_mongo_collection(collection='goals', database='nbsap',
                         host=None, port=None):

    conn = get_mongo_connection(host, port)
    db = conn[database]

    return db[collection]


def sanitizer(field='description', one_level=True,
              has_son=None, mycollection=None):

    try:
        collection = get_mongo_collection(mycollection)
    except TypeError:
        print 'Must provide a valid collection'

    for db_object in collection.find():
        if one_level is True:
            for lang in ['en', 'fr', 'nl']:
                fw = codecs.open("fw.txt", "w", "utf-8")
                fw.write(db_object[field][lang])
                fw.close()
                os.system("python html2text.py fw.txt > fr.txt")
                fr = codecs.open("fr.txt", "r", "utf-8")
                content = fr.read()
                db_object[field][lang] = content
                collection.save(db_object)

        if has_son is not None:
            for subfield in db_object[has_son]:
                for lang in ['en', 'fr', 'nl']:
                    fw = codecs.open("fw.txt", "w", "utf-8")
                    fw.write(subfield[field][lang])
                    fw.close()
                    os.system("python html2text.py fw.txt > fr.txt")
                    fr = codecs.open("fr.txt", "r", "utf-8")
                    content = fr.read()
                    subfield[field][lang] = content
                    collection.save(db_object)

if __name__ == "__main__":
    sanitizer(mycollection='goals')

    sanitizer(mycollection='targets')

    sanitizer(field='body', one_level=False,
              has_son='actions', mycollection='actions')

    sanitizer(field='body', has_son='subobjs',
              mycollection='objectives')
