from tinydb import TinyDB

def DB():
    return TinyDB('db.json')

def DB_CONFIG():
    return DB().table('CONFIG')

def DB_PRODUCT_STRUCTURE():
    return DB().table('PRODUCT_STRUCTURE') 