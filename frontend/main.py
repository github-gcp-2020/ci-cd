from flask import Flask, request, render_template
import os

from google.cloud import storage
from send_request import send_request

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

BUCKET_NAME = os.environ.get('PROJECT_ID', '')

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload-image', methods=['POST'])
def upload_image():

    target = os.path.join('/tmp/', 'static/images/')
    print("Target: " + target)

    if not os.path.exists(target):
        print("Directory {} doesn't exist, creating it...".format(target))
        os.makedirs(target)

    upload = request.files.getlist("file")[0]

    filename = upload.filename

    destination = "/".join([target, filename])

    upload.save(destination)

    upload_to_gcs(destination, filename)

    result = send_request(BUCKET_NAME, filename)

    return render_template(
                "uploaded.html", result={
                    "uploaded": "File {} uploaded to bucket {}".format(filename, BUCKET_NAME),
                    "task":      result
                })

def upload_to_gcs(source, filename):
    storage_client = storage.Client()

    bucket = storage_client.bucket(BUCKET_NAME)

    blob = bucket.blob(filename)

    blob.upload_from_filename(source)

    print("Object {} uploaded to bucket {}".format(source, BUCKET_NAME))


if __name__=='__main__':
    app.run('0.0.0.0', port=8080, debug=True)
