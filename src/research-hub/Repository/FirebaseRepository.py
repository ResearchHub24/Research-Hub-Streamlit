from firebase.Firebase import Firebase
from model.UserModel import UserModel
from utils.Secrates import json_data


class FirebaseRepository:
    def __init__(self):
        self.__firebase: Firebase = Firebase(json_data)

    def log_in(self, email, password) -> UserModel | None:
        return self.__firebase.log_in(email, password)
