import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import Client, FieldFilter

from model.UserModel import UserModel
from utils.Exceptions import LoginException


class Firebase:
    def __init__(self, path):
        self.__credit = credentials.Certificate(path)
        try:
            self.app = firebase_admin.get_app()
        except ValueError:
            # If not, initialize a new app
            self.app = firebase_admin.initialize_app(self.__credit)
        self.db: Client = firestore.client()

    def log_in(self, email, password):
        user = self.db.collection('user_database').where(
            filter=FieldFilter('email', '==', email),
        ).stream()
        for doc in user:
            user = UserModel(**doc.to_dict())
        if not isinstance(user, UserModel):
            raise LoginException('Invalid Email')
        if user.password == password:
            return user
        else:
            raise LoginException('Invalid Password')
