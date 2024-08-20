import csv
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

client = MongoClient("mongodb+srv://takhanhlyt66:Vly.19952003@cluster0.czn0pgn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
database = client['dtu']
interaction_collection = database['interactions']
interaction = []

def map_interaction():
    with open("C:/Users/taly2/Downloads/Transaction.csv", "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            id, selection_change, start_time, end_time, difficulty_feedback, trust_feedback, answer_status, answer_text, student_id, hint_used, question_id, answer_choice_id, is_hidden = row
            
            start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f %z')
            end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f %z')
            time_span = end_time - start_time
            
            interaction.append({
                "_id": ObjectId(),  
                "selection_change": int(selection_change),
                "start_time": start_time,
                "end_time": end_time,
                "hint_used": hint_used,
                "time_span": time_span.total_seconds(),  
                "difficulty_feedback": float(difficulty_feedback),
                "trust_feedback": float(trust_feedback),
                "answer_status": answer_status,
                "student_id": student_id,
                "question_id": question_id
            })

map_interaction()
interaction_collection.insert_many(interaction)
