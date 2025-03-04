import pymongo

url = 'mongodb+srv://root:GcgM0Se77g5Ov2Fm@tiproject.psh9l.mongodb.net/?retryWrites=true&w=majority&appName=TiProject'
client = pymongo.MongoClient(url)
db = client.tiproject
