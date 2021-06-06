#!/usr/bin/env python3

def convert_storage(storage_from, storage_to):
    count = 0
    for k in storage_from:
        print("convert %s ..." % k)
        count += 1
        storage_to[k] = storage_from[k]
    print("converted %s items" % count)

def convert_session(session_from, session_to):
    self.convert_storage(session_from._data_store,
                         session_to._data_store)

