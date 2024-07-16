from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.utils.file import read_yaml_file
from app.services.gemini import GeminiClient

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
