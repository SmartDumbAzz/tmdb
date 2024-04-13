import requests
import gzip
import json
from datetime import datetime, timedelta
from flask import Flask, jsonify
from io import BytesIO

app = Flask(__name__)

@app.route('/movies', methods=['GET'])
def get_movies():
    # Get the current date and time
    current_datetime = datetime.utcnow()

    # Check if the current time is before 9:00 AM UTC
    if current_datetime.hour < 9:
        # If it is, subtract one day from the current date
        current_datetime -= timedelta(days=1)

    # Format the date as MM_DD_YYYY
    date_str = current_datetime.strftime('%m_%d_%Y')

    # Create the URL
    url = f'http://files.tmdb.org/p/exports/movie_ids_{date_str}.json.gz'

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # If it was, save the content to a BytesIO object
        compressed_file = BytesIO(response.content)

        # Open the BytesIO object and extract the data
        decompressed_file = gzip.GzipFile(fileobj=compressed_file)

        # Load the JSON data
        data = json.loads(decompressed_file.read().decode())

        # Return the data as a JSON response
        return jsonify(data)

    else:
        # If the request was not successful, return an error message
        return jsonify({'error': 'Could not download data'})

if __name__ == '__main__':
    app.run(debug=True)
