from flask import request
from flask_restful import Resource
import json


class GetRecordInfo(Resource):

    def __init__(self, firebase):
        # self.image_handler = ImageHandler()
        # self.image_predictor = ImagePredictor(predictor)
        self.firebase = firebase
        # self.data_service = DataService(firebase)
        # self.health_advisor = HealthAdvisor(self.data_service)
        # self.dietary_advisor = DietaryAdvisor(self.data_service)

    def get(self):
        recordId = request.args.get('recordId')
        print("recordId: ", recordId)
        uid = request.args.get('uid')
        print("uid: ", uid)
        try:
            record = self.firebase.get_record_info(uid, recordId)
            food_data = self.firebase.get_food_data(record['food_id'])
            response = {
                "picture_path": record['picture_path'],
                "name": record['name'],
                "food_id": record['food_id'],
                "calories": record['calories'],
                "overflow_items": record['overflow_items'],
                "sugar":  0 if food_data['糖'] is None else food_data['糖'],
                "protein": 0 if food_data['蛋白質'] in food_data else food_data['蛋白質'],
                "sodium": 0 if food_data['鈉'] is None else food_data['鈉'],
                "fat": 0 if food_data['脂肪'] is None else food_data['脂肪'],
                "carbohydrate": 0 if food_data['碳水化合物'] is None else food_data['碳水化合物'],
                "time": record['time'].strftime("%Y-%m-%d %H:%M")
            }
            print("response: ", response)
            return response, 200
        except Exception as e:
            print(e)
            return "Error", 400
