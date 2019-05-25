from pymongo import MongoClient
from conf.conf import get_conf

mongo_client = MongoClient(get_conf("mongo_db"), username=get_conf("mongo_username"), password=get_conf("mongo_password"))
mongoc = mongo_client.site6vdata