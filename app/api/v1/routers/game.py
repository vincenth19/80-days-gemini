import os
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from app.utils.file import read_yaml_file
from app.services.gemini import GeminiClient
from app.services.database import FirestoreClient
from app.services.options import JourneyPath
from loguru import logger

db_client = FirestoreClient(os.environ['FIRESTORE_PROJECT_ID'], logger=logger)

router = APIRouter(
    prefix="/game",
    tags=["game"]
)

@router.post("/{user_id}")
async def new_game(user_id: str, title: str = Query("Unnamed Game", min_length=1)):
    return db_client.create_new_game(user_id=user_id, title=title)

@router.get("/{user_id}")
def list_saves(user_id):
    return db_client.retrieve_user_data_ref(user_id).get().get('game_ids')

@router.get("/{user_id}/{game_id}")
def retrieve_save(user_id, game_id):
    return db_client.retrieve_game_data_ref(game_id).get().to_dict()

@router.delete("/{user_id}/{game_id}")
def delete_save(user_id, game_id):
    return db_client.delete_game_save(user_id, game_id)

@router.post("/options/path")
def generate_path_option(location):
    gemini_client = GeminiClient()
    model = gemini_client.use_gemini()
    path_options = JourneyPath(model, './static/prompts.yaml', logger, location)
    return path_options.options