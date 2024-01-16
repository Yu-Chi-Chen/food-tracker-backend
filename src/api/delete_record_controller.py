from flask import request
from flask_restful import Resource
import json


class DeleteRecord(Resource):
    def __init__(self, firebase):
        self.firebase = firebase

    def post(self):
        request_body = request.get_json()
        uid = request_body["uid"]
        recordId = request_body["recordId"]
        try:
            self.firebase.delete_record(uid, recordId)
            return "Success", 200
        except Exception as e:
            print(e)
            return "Error", 400
