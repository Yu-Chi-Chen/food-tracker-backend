from google.oauth2 import service_account
from google.cloud import aiplatform
from flask import Flask, send_from_directory
from flask_restful import Api
from flask_cors import CORS
from api.get_record_controller import GetRecords
from api.get_record_info_controller import GetRecordInfo
from resources.firebase import Firebase
from api.get_user_upload_photo_controller import GetUserUploadPhoto
from resources.photoDetect import ImageClassificationPredictionInstance

UPLOAD_FOLDER = '../uploads'

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


credentials = service_account.Credentials.from_service_account_file(
    'ServiceAccountToken.json')

aiplatform.init(
    # your Google Cloud Project ID or number
    # environment default used is not set
    project='fine-tractor-362306',

    # the Vertex AI region you will use
    # defaults to us-central1
    location='us-central1',

    # Google Cloud Storage bucket in same region as location
    # used to stage artifacts
    staging_bucket='gs://my_staging_bucket',

    # custom google.auth.credentials.Credentials
    # environment default credentials used if not set
    credentials=credentials,

    # customer managed encryption key resource name
    # will be applied to all Vertex AI resources if set
    # encryption_spec_key_name=my_encryption_key_name,

    # the name of the experiment to use to track
    # logged metrics and parameters
    experiment='dev',

    # description of the experiment above
    experiment_description='dev dev rrrrrrrrr'
)

# create instance
prediction_instance = ImageClassificationPredictionInstance(
    project="fine-tractor-362306",
    endpoint_id="1979879593019965440",
    location="us-central1",
    api_endpoint="us-central1-aiplatform.googleapis.com"
)

firebase = Firebase()

api.add_resource(GetUserUploadPhoto, '/api/getUserUploadPhoto',
                 resource_class_args=(prediction_instance,
                                      firebase,))

api.add_resource(GetRecordInfo, '/api/record-info',
                 resource_class_args=(firebase,))

api.add_resource(GetRecords, '/api/records',
                 resource_class_args=(firebase,))


@app.route('/api/user-upload-photo/<name>')
def user_upload_photo(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


if __name__ == '__main__':
    app.run(debug=True)
