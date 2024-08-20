import csv
from pymongo import MongoClient
import random
from faker import Faker
import numpy as np

client = MongoClient("mongodb+srv://takhanhlyt66:Vly.19952003@cluster0.czn0pgn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
database = client['dtu']
student_collection = database['students']
fake = Faker('vi_VN')
global student
student = {}


def map_student():
    with open('C:/Users/taly2/Downloads/Student_Specialization.csv', mode='r', encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            id, specialization, student_id = row
            student[student_id] = student.get("student_id", '')
            if specialization not in student[student_id]:
                student[student_id] = specialization

map_student()
list_id = set(student.keys())
list_student = [{
    "_id": id, 
    "specialization": student[id],
    "birth_year": 2024 - int(np.clip(np.random.normal(19, 4), 7, 40)),  
    "full_name": fake.name(),
    "email": fake.email()} for id in list_id]
def map_specialization():
    with open('C:/Users/taly2/Downloads/Specialization.csv', mode='r', encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)

        for row in csv_reader:
            id, title = row
            for student in list_student:
                if student['specialization'] == id:
                    student['specialization_name'] = title
map_specialization()
student_collection.insert_many(list_student)

