import os
import logging
from uuid import uuid4
from app.services.objects import User,GameSaveData
# from objects import User, GameSaveData
from google.cloud import firestore
from loguru import logger

FIREBASE_DB_NAME = os.environ['FIREBASE_DB_NAME']
USERS_COLLECTION = os.environ['USERS_COLLECTION']
GAME_SAVES_COLLECTION = os.environ['GAME_SAVES_COLLECTION']

class FirestoreClient():
    def __init__(self, project_id, logger: logging.Logger):
        self.client = firestore.Client(project=project_id, database=FIREBASE_DB_NAME)
        self.logger = logger

    def retrieve_user_data_ref(self, user_id):
        # This assumes that we use firebase authentication that should give unique user_id
        return self.client.collection(USERS_COLLECTION).document(user_id)
    
    def add_new_user(self, user_id, username):
        self.logger.info(f'adding new user')
        user = User(user_id, username, 
                    creation_time=firestore.SERVER_TIMESTAMP, 
                    last_updated=firestore.SERVER_TIMESTAMP, 
                    game_ids=[])
        self.logger.info(f'adding new user to user collection')
        user_doc_ref = self.client.collection(USERS_COLLECTION).document(user.id)
        user_doc_ref.set(user.to_dict())
        return user_doc_ref.get().to_dict()
    
    def retrieve_game_data_ref(self, game_id):
        return self.client.collection(GAME_SAVES_COLLECTION).document(game_id)

    def create_new_game(self, user_id, title):
        game = GameSaveData(id = str(uuid4()), 
                            user_id=user_id, title=title, 
                            creation_time=firestore.SERVER_TIMESTAMP, 
                            last_updated=firestore.SERVER_TIMESTAMP)
        user_doc_ref = self.retrieve_user_data_ref(user_id)
        user_doc = user_doc_ref.get()
        updated_game_ids = user_doc.get('game_ids') + [game.id]

        self.logger.info(f"adding new game id {game.id} to game save collection")
        game_doc_ref = self.client.collection(GAME_SAVES_COLLECTION).document(game.id)
        game_doc_ref.set(game.to_dict())
        self.logger.info(f"adding new game id {game.id} to user data")
        user_doc_ref.update({'last_updated': firestore.SERVER_TIMESTAMP, 'game_ids': updated_game_ids})
        return game_doc_ref.get().to_dict()
    
    def delete_game_save(self, user_id, game_id):
        self.client.collection(GAME_SAVES_COLLECTION).document(game_id).delete()
        user_doc_ref = self.retrieve_user_data_ref(user_id)
        user_doc = user_doc_ref.get()
        updated_game_ids = user_doc.get('game_ids')
        self.logger.info(f'removing {game_id} from user data and game save collection')
        updated_game_ids.remove(game_id)
        user_doc_ref.update({'last_updated': firestore.SERVER_TIMESTAMP, 'game_ids': updated_game_ids})
        return {"game_id": game_id}

    def update_path(self, game_id, latest_city):
        game_doc_ref = self.retrieve_game_data_ref(game_id=game_id)
        game_doc = game_doc_ref.get()
        self.logger.info(f'updating path in game {game_id}')
        updated_journey_path = game_doc.get('journey_path') + [latest_city]
        game_doc_ref.update({'last_updated': firestore.SERVER_TIMESTAMP, 'journey_path': updated_journey_path})

# if __name__=="__main__":
#     db_client = FirestoreClient('days-gemini', logger=logger)
#     # test = db_client.add_new_user('test1', 'test1')
#     # test = db_client.create_new_game('test1', 'test1')
#     # test = db_client.delete_game_save('test1', 'a1c22f3c-b651-439f-9427-244d044dc970')
#     print(test)