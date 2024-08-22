from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import pickle
from bson import ObjectId
from pymongo import MongoClient
import implicit
from data_preprocessing import Dataset
from gridfs import GridFS
from kafka import KafkaProducer, KafkaConsumer
import json
import base64
app = Flask(__name__)
CORS(app)

# Load dataset
# with open('dataset.pkl', 'rb') as file:
#     dataset = pickle.load(file)

# Load pretrained model
# model = implicit.cpu.als.AlternatingLeastSquares.load('model.npz')

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))
consumer = KafkaConsumer('topic-send',
                         bootstrap_servers='localhost:9092',
                         auto_offset_reset='earliest',
                         group_id='video-stream-group',
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# Connect to MongoDB
# client = MongoClient(
#     'mongodb+srv://admin:admin123@cluster0.jmil5cr.mongodb.net/dtu?retryWrites=true&w=majority&appName=Cluster0')
client = MongoClient("mongodb://localhost:27017")
db = client['dtu']
grid_fs = GridFS(db)

@app.route('/get_infor/<player_id>', methods=['GET'])
def get_infor(player_id):
    try:
        player = db.players.find_one({'_id': ObjectId(player_id)})
        player['_id'] = str(player['_id'])
        if not player:
            return jsonify({'error': 'Player not found'}), 404
        return jsonify(player), 200
    except Exception as error:
        # print('Error:', error)
        return jsonify({'error': 'Internal server error.'}), 500


@app.route('/get_question', methods=['POST'])
def get_question():
    try:
        data = request.json
        question_id = data.get('question_id')
        question_id = [ObjectId(id) for id in question_id]
        pipeline = [
            {"$match": {"_id": {"$in": question_id}}},
            {"$project": {"_id": 0,
                        "id": {"$toString": "$_id"},
                        "question": "$content",
                        "options": "$answers",
                        "answer": "$correct_answer",
                        "outcome": "$questions.outcome",
                        "difficulty": "$difficulty",
                        "category": "$category",
                        "multimedia": {"$toString": "$multimedia"}, }}
        ]
        question = list(db.questions.aggregate(pipeline))
        # print(question)
        if not question:
            return jsonify({'error': 'Question not found'}), 404
        return jsonify(question), 200
    except Exception as error:
        # print('Error:', error)
        return jsonify({'error': 'Internal server error.'}), 500



@app.route('/openVideo/<qid>', methods=['GET'])
def open_video(qid):
    try:
        video_object_id = ObjectId(qid)
        range_header = request.headers.get('Range', None)

        chunks = db.fs.chunks.find({'files_id': video_object_id}).sort('n', 1)

        # Send each chunk to the Kafka topic
        for chunk in chunks:
            # Encode binary data to Base64
            data = base64.b64encode(chunk['data']).decode('utf-8')

            # Prepare the message
            message = {
                'video_id': str(video_object_id),
                'chunk': {
                    '_id': str(chunk['_id']),
                    'files_id': str(chunk['files_id']),
                    'n': chunk['n'],
                    'data': data
                }
            }

            # Send the message to the Kafka topic
            producer.send('topic-send', message)
            producer.flush()

        def generate_chunks():
            start = end = total_length = None

            for message in consumer:
                video_data = message.value

                if video_data['video_id'] == str(video_object_id):
                    chunk = base64.b64decode(video_data['chunk']['data'])
                    start = start or 0
                    end = len(chunk) - 1
                    total_length = video_data.get('total_length', end + 1)

                    # Yield the chunk to be streamed
                    yield chunk

                    # Break the loop if this is the last chunk
                    if end + 1 >= total_length:
                        break

        # Create a response object for streaming
        response = Response(generate_chunks(), status=206, content_type='video/mp4')
        response.headers['Accept-Ranges'] = 'bytes'
        if start is not None and end is not None and total_length is not None:
            response.headers['Content-Range'] = f'bytes {start}-{end}/{total_length}'
            response.headers['Content-Length'] = str(end - start + 1)
        
        return response

    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500



    

# @app.route('/openVideo/<qid>', methods=['GET'])
# def open_video(qid):
#     try:
#         video_object_id = ObjectId(qid)
#         file = grid_fs.find_one({'_id': video_object_id})
#         if not file:
#             return jsonify({'error': 'Video file not found.'}), 404

#         range_header = request.headers.get('Range', None)
#         if not range_header:
#             # If no Range header, stream the whole file
#             video_stream = grid_fs.get(video_object_id)
#             response = Response(video_stream, content_type='video/mp4')
#             response.headers['Content-Length'] = file.length
#             return response
#         else:
#             # Handle Range header for partial content streaming
#             start, end = range_header.replace('bytes=', '').split('-')
#             start = int(start)
#             end = int(end) if end else file.length - 1

#             video_stream = grid_fs.get(video_object_id)
#             video_stream.seek(start)

#             chunk_size = end - start + 1
#             data = video_stream.read(chunk_size)
            
#             response = Response(data, status=206, content_type='video/mp4')
#             response.headers['Content-Range'] = f'bytes {start}-{end}/{file.length}'
#             response.headers['Accept-Ranges'] = 'bytes'
#             response.headers['Content-Length'] = str(chunk_size)
#             return response
#     except Exception as e:
#         return jsonify({'error': 'Internal Server Error'}), 500


# @app.route('/recommend_with_data', methods=['POST'])
# def recommend_new_data():
#     data = request.json
#     print(len(data))
#     player_ixs, question_ixs = dataset.add_new_data(data)
#     sparse_player_ques = dataset.build_sparse_player_ques()
#     model.partial_fit_users(player_ixs, sparse_player_ques[player_ixs, :])
#     model.partial_fit_items(
#         question_ixs, sparse_player_ques[:, question_ixs].transpose().tocsr())
#     ixs, _ = model.recommend(
#         player_ixs, sparse_player_ques[player_ixs], N=10, filter_already_liked_items=True)
#     result_dict = {}
#     for i, player_ix in enumerate(player_ixs):
#         result_dict[str(dataset.get_player_id(player_ix))] = [
#             str(dataset.get_question_id(ix)) for ix in ixs[i]]
#     # print(result_dict)
#     return jsonify(result_dict)


# @app.route('/recommend', methods=['POST'])
# def recommend():
#     user = request.json
#     player_ids = user['player_id']
#     if isinstance(player_ids, str):
#         player_ixs = dataset.get_player_ix(ObjectId(player_ids))
#     elif isinstance(player_ids, list):
#         player_ixs = [dataset.get_player_ix(
#             ObjectId(player_id)) for player_id in player_ids]
#     else:
#         raise ValueError(
#             'player_ids must be an str or a list of str')
#     sparse_player_ques = dataset.build_sparse_player_ques()
#     ids, _ = model.recommend(
#         player_ixs, sparse_player_ques[player_ixs], N=10, filter_already_liked_items=True)
#     if ids.ndim == 1:
#         return jsonify([str(dataset.get_question_id(ix)) for ix in ids])
#     result_dict = {}
#     for i, player_id in enumerate(player_ids):
#         result_dict[str(player_id)] = [str(dataset.get_question_id(ix))
#                                        for ix in ids[i]]
#     # print(result_dict)
#     return jsonify(result_dict)


if __name__ == '__main__':
    app.run(port=8080, debug=True)
