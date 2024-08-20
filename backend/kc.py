
import csv
from pymongo import MongoClient

client = MongoClient("mongodb+srv://takhanhlyt66:Vly.19952003@cluster0.czn0pgn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
database = client['dtu']
knowledge_collection = database['knowledges']
global knowledge
knowledge = []

def map_knowledge():
    with open("C:/Users/taly2/Downloads/KCs.csv", "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            id, name, description  = row
            knowledge.append({
                "_id": id,
                "name": name,
                "description": description
            })


# def map_knowledge_relationship():
#     with open('C:/Users/taly2/Downloads/KC_Relationships.csv', mode='r', encoding="utf-8") as file:
#         csv_reader = csv.reader(file)
#         next(csv_reader)
#         for row in csv_reader:
#             id, q_rich_text, q_title, explaination, hint_text, q_text, difficulty = row
#             for question in questions:
#                 if question["_id"] == id:
#                     question["title"] = q_title
#                     question["content"] = q_text
#                     question["difficulty"] = int(difficulty)
#                     break

map_knowledge()

knowledge_collection.insert_many(knowledge)