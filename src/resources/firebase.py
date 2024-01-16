import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
from google.cloud.firestore import FieldFilter
import os

from resources.datetime_tool import DatetimeTool


class Firebase:
    # Use a service account.
    # cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
    cred = credentials.Certificate(
        "healthrecord-ae765-firebase-adminsdk-mplg2-5746f48506.json")

    app = firebase_admin.initialize_app(cred)
    db = firestore.client()

    def get_food_data(self, food_name):
        doc_ref = self.db.collection("food").document(food_name)

        doc = doc_ref.get()
        if doc.exists:
            print(f"get_food_data: {doc.to_dict()}")
            return doc.to_dict()
        else:
            print("No such document!")
            return None

    def get_user_data(self, uid):
        doc_ref = self.db.collection("user_information").document(uid)

        doc = doc_ref.get()
        if doc.exists:
            print(f"get_user_data: {doc.to_dict()}")
            return doc.to_dict()
        else:
            print("No such document!")
            return None

    def get_disease_info(self, diseases):
        food_to_avoid = set()
        for disease in diseases:
            doc_ref = self.db.collection(
                "diretary_attention").document(disease)
            doc = doc_ref.get()
            if doc.exists:
                print(f"disease: {doc.to_dict()}")
                food_to_avoid.update(doc.to_dict()['FoodsToAvoid'].items())
            else:
                print("No such document " + disease + " !")

        print("get_disease_info(): ", food_to_avoid)
        return dict(food_to_avoid)

    def add_record(self, uid, picture_path, food_name, food_id, food_calories, overflow_items) -> str:
        update_time, record_ref = self.db.collection("user_information").document(uid).collection("record").add({
            "picture_path": picture_path,
            "name": food_name,
            "food_id": food_id,
            "calories": food_calories,
            "overflow_items": overflow_items,
            "time": firestore.SERVER_TIMESTAMP
        })
        print("add_reacrd(): ", record_ref.id)
        return record_ref.id

    def get_record_info(self, uid, record_id):
        doc_ref = self.db.collection("user_information").document(
            uid).collection("record").document(record_id)

        doc = doc_ref.get()
        if doc.exists:
            print(f"get_record: {doc.to_dict()}")
            return doc.to_dict()
        else:
            print("No such document!")
            return None

    def get_record(self, uid, time_start, time_end, limit=10, last_pop_time=None):
        doc_ref = self.db.collection("user_information").document(
            uid).collection("record")

        timestamp_start = DatetimeTool.convert_to_utc(time_start)
        timestamp_end = DatetimeTool.convert_to_utc(time_end)

        query = doc_ref.order_by("time").where(filter=FieldFilter("time", ">=", timestamp_start)).where(
            filter=FieldFilter("time", "<", timestamp_end))

        if last_pop_time is not None:
            query = query.start_after({"time": last_pop_time}).limit(limit)

        results = [
            {
                "id": doc.id,
                **doc.to_dict()
            }for doc in query.stream()
        ]

        print(f"get_record({uid}, {time_start}, {time_end}): {results}")

        last_pop_time = results[-1]['time']

        return results, last_pop_time

    def delete_record(self, uid, record_id):
        doc_ref = self.db.collection("user_information").document(
            uid).collection("record").document(record_id)
        doc_ref.delete()
        return True
