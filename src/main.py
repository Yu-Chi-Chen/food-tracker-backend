from google.oauth2 import service_account
from google.cloud import aiplatform
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from resources.upload import FileUpload
from resources.photoDetect import ImageClassificationPredictionInstance


app = Flask(__name__)
CORS(app)
api = Api(app)


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

api.add_resource(FileUpload, '/api/getUserUploadPhoto',
                 resource_class_args=(prediction_instance,))

if __name__ == '__main__':
    app.run(debug=True)
