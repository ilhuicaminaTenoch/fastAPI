from pymongo import MongoClient

# user: zerocoolmoreno
# pass: 8eZEUdeJVzyzg8Zs
# mongodb+srv://zerocoolmoreno:8eZEUdeJVzyzg8Zs@cluster0.ewkgi5y.mongodb.net/
# mongodb+srv://zerocoolmoreno:8eZEUdeJVzyzg8Zs@cluster0.ewkgi5y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
db_client = MongoClient('mongodb+srv://zerocoolmoreno:8eZEUdeJVzyzg8Zs@cluster0.ewkgi5y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0').sample_mflix
