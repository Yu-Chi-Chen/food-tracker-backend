from flask import request
from flask_restful import Resource
import json

from resources.image_handler import ImageHandler
from resources.image_predictor import ImagePredictor


class GetUserUploadPhoto(Resource):

    items_to_check = ['反式脂肪', '糖', '飽和脂肪',
                      '蛋白質', '膽固醇', '磷', '鈉', '鈣', '鉀', '鐵']

    def __init__(self, predictor, firebase):
        self.image_handler = ImageHandler()
        self.image_predictor = ImagePredictor(predictor)
        self.firebase = firebase
        # self.data_service = DataService(firebase)
        # self.health_advisor = HealthAdvisor(self.data_service)
        # self.dietary_advisor = DietaryAdvisor(self.data_service)

    def post(self):
        if 'photo' not in request.files:
            return 'No photo part', 400

        file = request.files['photo']
        if file.filename == '':
            return 'No selected file', 400

        file_name, file_path = self.image_handler.save_image(file)

        # predict
        try:
            prediction_result = self.image_predictor.predict(file_path)
        except Exception as e:
            return f"Error during image classification: {str(e)}", 500

        # get food data
        try:
            food_id = prediction_result
            # food_id = "familymart_rice_ball_kimchi_tuna"
            food_data = self.firebase.get_food_data(food_id)
        except Exception as e:
            return f"Error during get food data: {str(e)}", 500

        # get user data
        uid = request.form.get('uid')
        if uid is None:
            return 'No uid provided', 400

        try:
            user_data = self.firebase.get_user_data(uid)
            food_to_avoid = self.firebase.get_disease_info(
                user_data['disease'])
            print("food_to_avoid: ", food_to_avoid)
        except Exception as e:
            print(f"Error during get user data: {e}")
            return 'Error during get user data', 500

        overflow_items = set()
        for item in self.items_to_check:
            print("item: ", item)
            print("  food_data.keys(): ", item in food_data.keys())
            print("  food_to_avoid: ", item in food_to_avoid.keys())
            if (item in food_data.keys()) and (item in food_to_avoid.keys()):
                print('  check if both are not None')
                if food_data[item] is not None and food_to_avoid[item] is not None:
                    print("  food_data[item]: ", food_data[item])
                    print("  food_to_avoid[item]: ", food_to_avoid[item])
                    if food_data[item] > food_to_avoid[item]:
                        print("overflow")
                        overflow_items.add(item)

        try:
            record_id = self.firebase.add_record(
                uid, file_name, food_data['name'], food_id, food_data['熱量'], overflow_items)
            print("record_id: ", record_id)
        except Exception as e:
            return f"Error during add record: {str(e)}", 500

        response_data = {
            "id": record_id,
        }

        print("response_data: ", response_data)

        return json.dumps(response_data, ensure_ascii=False), 200
