from pymongo import MongoClient
mongo_client = MongoClient('mongodb://192.168.1.6:27017/')
collection=mongo_client.spider
result = collection.contract_three_item.find()
for index,data in enumerate(result):
    print index
    print data