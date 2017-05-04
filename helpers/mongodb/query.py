from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()

db = client.lhpconfessions

def arr2dict(key, value):
    fields = {}
    for i in range(len(key)):
        if (key[i] == "_id"):
            value[i] = ObjectId(value[i])
        fields[key[i]] = value[i]
    return fields

def find(collection, key = [], value = []):
    return findWithLimit(collection, key = key, value = value, limit = "infinite")

def findOne(collection, key = [], value = []):
    return findWithLimit(collection, key = key, value = value, limit = 1)

def findWithLimit(collection, limit, key = [], value = []):
    collection = db[collection]
    fields = arr2dict(key, value)
    if limit == "infinite":
        return collection.find(fields)
    else:
        return collection.find(fields).limit(limit)

def sort(collection, sort_key = [], sort_order = [], key = [], value = []):
    collection = db[collection]
    fields = arr2dict(key, value)
    # sort_fields = arr2dict(sort_key, sort_order)
    if collection.find(fields).count() > 0:
        return collection.find(fields).sort(sort_key[0], sort_order[0])
    else:
        return False

def sortWithLimit(collection, limit, sort_key = [], sort_order = [], key = [], value = []):
    collection = db[collection]
    fields = arr2dict(key, value)
    sort_fields = arr2dict(sort_key, sort_order)
    if limit == "infinite":
        return collection.find(fields).sort(sort_fields)        
    else:
        return collection.find(fields).sort(sort_fields).limit(limit)

def insert(collection, key = [], value = []):
    collection = db[collection]
    fields = arr2dict(key, value)
    _id = collection.insert_one(fields).inserted_id
    return _id

def update(collection, update_key = [], update_value = [], selector_key = [], selector_value = []):
    collection = db[collection]
    selector = arr2dict(selector_key, selector_value)
    fields = arr2dict(update_key, update_value)
    collection.update_one(selector, {"$set": fields})

def isExist(collection, key = [], value = []):
    collection = db[collection]
    fields = arr2dict(key, value)
    return collection.find(fields).count()

def get_value(collection, key = [], value = [], require = []):
    collection = db[collection]
    fields = arr2dict(key, value)
    projection = {}
    for i in range(len(require)):
        projection[require[i]] = 1
    if collection.find(fields, projection).count() > 0:
        return collection.find_one(fields, projection)
    else:
        return False

def get_arr_value(collection, key = [], value = [], require = []):
    collection = db[collection]
    fields = arr2dict(key, value)
    projection = {}
    for i in range(len(require)):
        projection[require[i]] = 1
    if collection.find(fields, projection).count() > 0:
        return collection.find(fields, projection)
    else:
        return False

def get_arr_value(collection, key = [], value = [], require = []):
    collection = db[collection]
    fields = arr2dict(key, value)
    projection = {}
    for i in range(len(require)):
        projection[require[i]] = 1
    return collection.find(fields, projection).limit(1)

def get_max(collection, max_key, key = [], value = []):
    query = sort(collection = collection, sort_key = [max_key], sort_order = [-1], \
        key = key, value = value)
    if query:
        fields = arr2dict(key, value)
        # print(query[0][max_key])
        return query[0][max_key]
    else:
        return False