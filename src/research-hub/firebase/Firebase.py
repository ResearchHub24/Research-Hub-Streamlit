import json
from typing import List

import firebase_admin
import streamlit as st
from firebase_admin import credentials, firestore, db
from google.cloud.firestore_v1 import Client, FieldFilter

from model.ResearchModel import TagModel, ResearchModel
from model.UserModel import UserModel
from utils.Exceptions import LoginException, TagException
from utils.Secrates import json_data
from utils.Utils import States


class Firebase:
    def __init__(self, path):
        self.__credit = credentials.Certificate(path)
        try:
            self.app = firebase_admin.get_app()
        except ValueError:
            # If not, initialize a new app
            self.app = firebase_admin.initialize_app(self.__credit, {
                'databaseURL': 'https://researchhub-21392-default-rtdb.firebaseio.com/'
            })
        self.db: Client = firestore.client()
        self.ref = db.reference('tags')

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

    def get_tags(self):
        # if st.session_state[States.User.name] is None:
        #     raise LoginException('Please login to continue')
        tags = str(self.ref.get())
        if not tags or tags == 'None':
            return []
        return self.tagsToList(tags.replace('\'', '\"'))

    def add_tag(self, tag: TagModel):
        if st.session_state[States.User.name] is None:
            raise LoginException('Please login to continue')
        uid = st.session_state[States.User.name].uid
        tag.created_by = uid
        if self.ref.child(tag.name.upper()).get():
            raise TagException('Tag already exists')
        self.ref.child(tag.name.upper()).set(tag.__dict__)

    @staticmethod
    def tagsToList(tags_json) -> List[TagModel]:
        data = json.loads(tags_json)
        return [TagModel(**tag_data) for tag_data in data.values()]

    def add_new_research(self, research: ResearchModel):
        doc_ref = self.db.collection('research').document()
        research.key = doc_ref.id
        doc_ref.set(research.__dict__)

    def get_research(self):
        research = (self.db.collection('research').where(
            filter=FieldFilter('created_by_UID', '==', st.session_state[States.User.name].uid),
        ).stream())
        return [ResearchModel(**doc.to_dict()) for doc in research]


def test():
    firebase = Firebase(json_data)
    for reg in firebase.get_research():
        print(reg)
# test()
