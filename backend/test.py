from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import gridfs
import base64
from kafka import KafkaProducer
import json

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['dtu']
fs = gridfs.GridFS(db)

# Kafka setup
topic = 'topic1'
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.route('/sendVideoChunks/<qid>', methods=['GET'])
def send_video_chunks(qid):
    try:
        video_object_id = ObjectId(qid)

        chunks = db.fs.chunks.find({'files_id': video_object_id}).sort('n', 1)

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
            producer.send(topic, message)
            print(f"Chunk {chunk['n']} sent to topic {topic}")
            producer.flush()

        return jsonify({'status': 'Chunks sent successfully'}), 200

    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)

# from pymongo import MongoClient
# from bson import ObjectId
# import gridfs
# import base64
# from kafka import KafkaProducer
# import json

# # Connect to MongoDB
# client = MongoClient('mongodb://localhost:27017/')
# db = client['dtu']

# # Initialize Kafka producer
# producer = KafkaProducer(
#     bootstrap_servers='localhost:9092',
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

# # Initialize GridFS
# fs = gridfs.GridFS(db)

# # Example files_id (replace with actual ID, make sure it's correctly formatted)
# files_id = ObjectId('66c54735b7a6a3486e6d6c6b')

# # Retrieve chunks by files_id
# chunks = db.fs.chunks.find({'files_id': files_id}).sort('n', 1)

# # Send each chunk to the Kafka topic
# for chunk in chunks:
#     print("Processing chunk", chunk['n'])
#     try:
#         # Encode binary data to Base64
#         data = base64.b64encode(chunk['data']).decode('utf-8')

#         # Prepare the message
#         message = {
#             'video_id': str(files_id),
#             'chunk': {
#                 '_id': str(chunk['_id']),
#                 'files_id': str(chunk['files_id']),
#                 'n': chunk['n'],
#                 'data': data
#             }
#         }

#         # Send the message to the Kafka topic
#         future = producer.send('topic-name', message)
#         future.get(timeout=10)
#         print(f"Chunk {chunk['n']} sent successfully!")
#     except Exception as e:
#         print(f"Failed to send chunk {chunk['n']}: {e}")

# # Flush any remaining messages
# producer.flush()

# print("Chunks sent to Kafka successfully!")
