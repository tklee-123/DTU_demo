import requests

# Example ObjectId for the video file you want to access
qid = '66260e81a51b34b732f21167'  # Replace with the actual ObjectId

# Construct the API URL with the qid parameter
url = f'http://localhost:8000/openVideo/{qid}'

# Optional: Specify the Range header if you want to request a specific byte range
headers = {
    'Range': 'bytes=0-1023'  # Example: first 1024 bytes; adjust as needed
}

try:
    # Sending a GET request to the API
    response = requests.get(url, headers=headers, stream=True)

    # Accessing different parts of the response
    print(f'Status Code: {response.status_code}')  # HTTP status code (e.g., 200, 404)
    print(f'Response Headers: {response.headers}')  # Headers returned by the server
    print(f'Content-Type: {response.headers.get("Content-Type")}')  # Specific header

    # If you expect JSON response (for example, in case of an error):
    if response.headers.get('Content-Type') == 'application/json':
        print(f'JSON Response: {response.json()}')  # Parsed JSON response
    
    # Saving the video content to a file (if successful)
    if response.status_code in [200, 206]:
        with open('output_video.mp4', 'wb') as video_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    video_file.write(chunk)

        print('Video has been successfully downloaded.')

    elif response.status_code == 404:
        print('Video file not found.')

    else:
        print(f'Failed to retrieve video. Status code: {response.status_code}')

except requests.exceptions.RequestException as e:
    print(f'An error occurred: {e}')
