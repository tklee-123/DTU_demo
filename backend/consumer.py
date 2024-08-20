from kafka import KafkaConsumer, KafkaProducer
from gridfs import GridFS
from pymongo import MongoClient
import json
from bson import ObjectId

# MongoDB and GridFS setup
client = MongoClient('mongodb+srv://admin:admin123@cluster0.jmil5cr.mongodb.net/dtu?retryWrites=true&w=majority&appName=Cluster0')
db = client['dtu']
grid_fs = GridFS(db)

# Kafka setup
consumer = KafkaConsumer('topic-send',
                         bootstrap_servers='localhost:9092',
                         auto_offset_reset='earliest',
                         group_id='video-stream-group',
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

for message in consumer:
    data = message.value
    video_id = data['video_id']
    range_header = data.get('range', None)

    video_object_id = ObjectId(video_id)
    file = grid_fs.find_one({'_id': video_object_id})

    if not file:
        continue  
    if not range_header:
        start = 0
        end = file.length - 1
    else:
        start, end = range_header.replace('bytes=', '').split('-')
        start = int(start)
        end = int(end) if end else file.length - 1

    video_stream = grid_fs.get(video_object_id)
    video_stream.seek(start)

    chunk_size = end - start + 1
    chunk = video_stream.read(chunk_size)

    # Send the chunk data back to the topic_reply
    producer.send('topic-reply', {
        'video_id': video_id,
        'chunk': chunk.decode('utf-8', errors='ignore'),
        'start': start,
        'end': end,
        'total_length': file.length
    })
    producer.flush()
