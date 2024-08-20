
import csv
from pymongo import MongoClient

client = MongoClient("mongodb+srv://takhanhlyt66:Vly.19952003@cluster0.czn0pgn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
database = client['dtu']
question_collection = database['questions']
global questions
questions = []
def map_question_and_answers():
    dict_questions = {}
    with open("C:/Users/taly2/Downloads/Question_Choices.csv", "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            question_id = row[3]
            if question_id not in dict_questions:
                dict_questions[question_id] = {'answer': [], 'correct_answer': ''}
            dict_questions[question_id]['answer'].append(row[1])
            if row[2] == "true":
                dict_questions[question_id]['correct_answer'] = row[1]
    
    return dict_questions



def map_question_and_knowledge():
    with open("C:/Users/taly2/Downloads/Question_KC_Relationships.csv", "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            id, question_id, knowledge_id = row
            for question in questions:
                if question["_id"] == question_id:
                    question["knowledge_id"] = knowledge_id
                    break


def map_question_difficulty():
    with open('C:/Users/taly2/Downloads/Questions.csv', mode='r', encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            id, q_rich_text, q_title, explaination, hint_text, q_text, difficulty = row
            for question in questions:
                if question["_id"] == id:
                    question["title"] = q_title
                    question["content"] = q_text
                    question["difficulty"] = int(difficulty)
                    break

dict_question = map_question_and_answers()
ids = list(dict_question.keys())
questions = [{'_id': x, 'answer': dict_question[x]['answer'], 'correct_answer': dict_question[x]['correct_answer']} for x in ids]
map_question_and_knowledge()
map_question_difficulty()

question_collection.insert_many(questions)