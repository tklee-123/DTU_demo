from flask import Flask, Response, jsonify, request
from kafka import KafkaConsumer
import base64
import json

app = Flask(__name__)

# Kafka Consumer setup
consumer = KafkaConsumer(
    'topic1',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='video-stream-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

@app.route('/openVideo/<qid>', methods=['GET'])
def open_video(qid):
    try:
        video_object_id = str(qid)
        start = None
        end = None
        total_length = None

        def generate_chunks():
            nonlocal start, end, total_length
            for message in consumer:
                video_data = message.value

                if video_data['video_id'] == video_object_id:
                    chunk = base64.b64decode(video_data['chunk']['data'])
                    n = video_data['chunk']['n']

                    if start is None:
                        start = n * len(chunk)

                    if total_length is None:
                        total_length = video_data.get('total_length', len(chunk))

                    end = start + len(chunk) - 1

                    yield chunk  # Yield the chunk to be streamed

                    # Update the start for the next chunk
                    start = end + 1

                    # Break the loop if this is the last chunk
                    if n + 1 >= total_length:
                        break

        # Check if start and end have valid values before creating the response
        if start is None or end is None or total_length is None:
            raise ValueError("Failed to retrieve video data properly.")

        # Create a streaming response with appropriate headers
        response = Response(generate_chunks(), status=206, content_type='video/mp4')
        response.headers['Accept-Ranges'] = 'bytes'
        response.headers['Content-Range'] = f'bytes {start}-{end}/{total_length}'
        response.headers['Content-Length'] = str(end - start + 1)

        return response

    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8081)
