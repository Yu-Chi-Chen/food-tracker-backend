from flask import request
from flask_restful import Resource
from werkzeug.utils import secure_filename
import uuid
import os

class FileUpload(Resource):
    def post(self):
        if 'photo' not in request.files:
            print('No photo part')
            return 'No photo part', 400

        file = request.files['photo']
        if file.filename == '':
            print('No selected file')
            return 'No selected file', 400

        if file:
            filename = str(uuid.uuid4()) + ".jpg"
            file.save(os.path.join('D:\\git\\food-tracker\\food-tracker-backend\\uploads', filename))
            print('File successfully uploaded')
            return 'File successfully uploaded', 200
