import csv
from pymongo import MongoClient

client = MongoClient("mongodb+srv://takhanhlyt66:Vly.19952003@cluster0.czn0pgn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
database = client['dtu']
bundle_collection = database['bundle']

global bundle
bundle = {}


def map_bundle():
    with open('C:/Users/taly2/Downloads/Questions.csv', mode='r', encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            id, q_rich_text, q_title, explaination, hint_text, q_text, difficulty = row
            b = str(q_title).strip().split("-")[0]  
            bundle[b] = bundle.get(b, [])
            bundle[b].append(id)

map_bundle()

for b, questions in bundle.items():
    bundle_collection.insert_one({
        "_id": b,
        "questions": questions
    })
