from flask import request
from flask_restful import Resource
import json


class GetRecords(Resource):

    def __init__(self, firebase):
        # self.image_handler = ImageHandler()
        # self.image_predictor = ImagePredictor(predictor)
        self.firebase = firebase
        # self.data_service = DataService(firebase)
        # self.health_advisor = HealthAdvisor(self.data_service)
        # self.dietary_advisor = DietaryAdvisor(self.data_service)

    def post(self):
        request_body = request.get_json()
        start_time = request_body["start_time"]
        end_time = request_body["end_time"]
        uid = request_body["uid"]
        print("uid: ", uid)
        try:
            records, last_pop_time = self.firebase.get_record(
                uid, start_time, end_time)

            response = {
                "last_pop_time": last_pop_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
                "data": [
                    {
                        "id": record['id'],
                        "picture_path": record['picture_path'],
                        "name": record['name'],
                        "food_id": record['food_id'],
                        "calories": record['calories'],
                        "overflow_items": record['overflow_items'],
                        "time": record['time'].strftime("%Y-%m-%d %H:%M")
                    } for record in records
                ]
            }
            print("response: ", response)
            return response, 200
        except Exception as e:
            print(e)
            return "Error", 500
