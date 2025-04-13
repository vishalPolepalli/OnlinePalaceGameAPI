from typing import List, Dict, Any
from pydantic import BaseModel

# --- API Request/Response Models ---
class CreateGameRequest(BaseModel):
    player_name: str

class CreateGameResponse(BaseModel):
    game_id: str
    player_id: str

class GetGamesResponse(BaseModel):
    games: List[str]

class JoinGameRequest(BaseModel):
    player_name: str

class JoinGameResponse(BaseModel):
    player_id: str

class GetPlayersResponse(BaseModel):
    players: List[str]

class WebSocketMessageOut(BaseModel):
    type: str # e.g., "GAME_UPDATE", "ERROR", "YOUR_TURN", "PLAYER_JOINED"
    payload: Dict[str, Any]