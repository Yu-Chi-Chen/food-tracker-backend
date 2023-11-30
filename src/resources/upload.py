from flask import request
from flask_restful import Resource
from werkzeug.utils import secure_filename
from resources.photoDetect import ImageClassificationPredictionInstance

import uuid
import os


class FileUpload(Resource):
    def __init__(self, predictor):
        self.predictor = predictor

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
            file_path = os.path.join('..\\uploads', filename)
            file.save(file_path)
            print('File successfully uploaded')
            # file.save(os.path.join('D:\\git\\food-tracker\\food-tracker-backend\\uploads', filename))
            # print('File successfully uploaded')
            # 调用图像识别方法

            try:
                result = self.predictor.predict_image_classification_sample(
                    filename=file_path)

                print("辨識結果: ", result[0]['displayNames'][0])
            # ...
                return 'File successfully uploaded and processed', 200
            except Exception as e:
                print(f"Error during image classification: {e}")
                return 'Error during image classification', 500
