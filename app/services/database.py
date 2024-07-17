import os
import logging
from uuid import uuid4
from objects import User,GameSaveData
from google.cloud import firestore

FIREBASE_DB_NAME = os.getenv('FIREBASE_DB_NAME')
USERS_COLLECTION = os.getenv('USERS_COLLECTION')
GAME_SAVES_COLLECTION = os.getenv('GAME_SAVES_COLLECTION')

class FirestoreClient():
    def __init__(self, project_id, logger: logging.Logger):
        self.client = firestore.Client(project=project_id, database=FIREBASE_DB_NAME)
        self.logger = logger

    def retrieve_user_data_ref(self, user_id):
        # This assumes that we use firebase authentication that should give unique user_id
        return self.client.collection(USERS_COLLECTION).document(user_id)
    
    def retrieve_game_data_ref(self, game_id):
        return self.client.collection(GAME_SAVES_COLLECTION).document(game_id)
    
    def add_new_user(self, user_id, username):
        user = User(user_id, username, 
                    creation_time=firestore.SERVER_TIMESTAMP, 
                    last_updated=firestore.SERVER_TIMESTAMP, 
                    game_ids=[])
        update_time, user_doc_ref = self.client.collection(USERS_COLLECTION).add(user.to_dict())
        self.logger.info(f'added new user')
        return user_doc_ref.get()

    def create_new_game(self, user_id, title):
        user_doc_ref = self.retrieve_user_data_ref(user_id)
        user_doc = user_doc_ref.get()
        game = GameSaveData(id = str(uuid4()), 
                            user_id=user_id, title=title, 
                            creation_time=firestore.SERVER_TIMESTAMP, 
                            last_updated=firestore.SERVER_TIMESTAMP)
        self.client.collection(GAME_SAVES_COLLECTION).document(game.id).set(game.to_dict())
        updated_game_ids = user_doc.get('game_ids') + [game.id]
        user_doc_ref.update({'last_updated': firestore.SERVER_TIMESTAMP, 'game_ids': updated_game_ids})

    def update_path(self, game_id, latest_city):
        game_doc_ref = self.retrieve_game_data_ref(game_id=game_id)
        game_doc = game_doc_ref.get()
        updated_journey_path = game_doc.get('journey_path') + [latest_city]
        game_doc_ref.update({'last_updated': firestore.SERVER_TIMESTAMP, 'journey_path': updated_journey_path})
