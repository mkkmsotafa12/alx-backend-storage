#!/usr/bin/env python3
""" Insert a document in Python """


def insert_school(mongo_collection, **kwargs):
    """ Insert a document in Python """
    doc = mongo_collection.insert_one(kwargs)
    return doc.inserted_id
