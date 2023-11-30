import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# Use a service account.
cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))

app = firebase_admin.initialize_app(cred)

db = firestore.client()
