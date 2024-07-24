import os
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from app.utils.file import read_yaml_file
from app.services.gemini import GeminiClient
from app.services.database import FirestoreClient
from loguru import logger

db_client = FirestoreClient(os.environ['FIRESTORE_PROJECT_ID'], logger=logger)

router = APIRouter(
    prefix="/game",
    tags=["game"]
)

@router.post('/start-game')
async def start_game():
    '''
    Start the game with this endpoint
    Returns:
      text/plain stream text
    '''
    try:
        prompts = read_yaml_file('./static/prompts.yaml')
        start_prompt = prompts.get('start', None)
        
        if not start_prompt:
            raise "No starting prompt"

        gemini = GeminiClient()
        response = gemini.use_gemini().generate_content(start_prompt)
        def generate():
            for chunk in response:
                yield chunk.text
        return StreamingResponse(generate(), media_type="text/plain")
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

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
