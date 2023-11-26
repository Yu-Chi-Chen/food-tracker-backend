from flask import Flask
from flask_restful import Api
from flask_cors import CORS 
from resources.upload import FileUpload

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(FileUpload, '/api/getUserUploadPhoto')

if __name__ == '__main__':
    app.run(debug=True)