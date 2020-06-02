from flask import Flask, request
from google.cloud import storage
from PIL import Image
import os

BUCKET_NAME = os.environ.get('PROJECT_ID', '')

app = Flask(__name__)

@app.route('/process_image', methods=['POST'])
def process_image():
    img_name = request.get_data().decode()
    print ("Processing image " + img_name + "...")

    target = '/tmp/static/images/'

    print("Target: " + target)

    if not os.path.exists(target):
        print("Directory {} doesn't exist, creating it...".format(target))
        os.makedirs(target)

    storage_client = storage.Client()

    bucket = storage_client.bucket(BUCKET_NAME)

    blob = bucket.blob(img_name)

    blob.download_to_filename(target + img_name)

    for i in [45, 90, 135, 180]:
        current_img = f"{str(i)}-{img_name}"
        
        img  = Image.open(target + img_name)

        img_rotated     = img.rotate(i)
        
        destination = target + current_img

        img_rotated.save(destination)

        blob = bucket.blob(f"{img_name}/{current_img}")

        blob.upload_from_filename(destination)

        print("Object {} uploaded to bucket {}".format(current_img, BUCKET_NAME))

    
    return "Done with image" + img_name


if __name__=='__main__':
    app.run('0.0.0.0', port=8080, debug=True)

