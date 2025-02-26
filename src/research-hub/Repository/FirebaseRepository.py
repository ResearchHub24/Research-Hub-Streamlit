from firebase.Firebase import Firebase
from model.ResearchModel import TagModel, ApplicationModel
from model.UserModel import UserModel
from utils.Secrates import json_data


class FirebaseRepository:
    def __init__(self):
        self.__firebase: Firebase = Firebase(json_data)

    def log_in(self, email, password) -> UserModel | None:
        return self.__firebase.log_in(email, password)

    def get_tags(self) -> list[TagModel]:
        return self.__firebase.get_tags()

    def add_tag(self, tag: TagModel):
        self.__firebase.add_tag(tag)

    def add_new_research(self, research):
        self.__firebase.add_new_research(research)

    def get_research(self):
        return self.__firebase.get_research()

    def delete_research(self, key):
        self.__firebase.delete_research(key)

    def update_research(self, research):
        self.__firebase.update_research(research)

    def get_application(self, path) -> list[ApplicationModel]:
        return self.__firebase.get_application(path)
