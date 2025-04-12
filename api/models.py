from typing import List
from pydantic import BaseModel

# --- API Request/Response Models ---
class CreateGameRequest(BaseModel):
    player_name: str

class CreateGameResponse(BaseModel):
    game_id: str
    player_id: str

class GetGamesResponse(BaseModel):
    games: List[str]