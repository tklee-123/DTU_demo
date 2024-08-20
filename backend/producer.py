from gridfs import GridFS
from kafka import KafkaProducer
from bson import ObjectId

class Producer:
    
    def __init__(self, database):
        self.database = database
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')

    def stream_video_to_kafka(self, qid):
        grid_fs = GridFS(self.database)
        video_file = grid_fs.get(ObjectId(qid))
    
        for chunk in video_file:
            self.producer.send('video-stream', chunk)
        
        self.producer.flush()
