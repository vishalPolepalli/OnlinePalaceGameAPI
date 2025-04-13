from typing import List, Dict, Any
from pydantic import BaseModel
from enum import Enum

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

class ActionType(str, Enum):
    PLAY_CARD = "PLAY_CARD"
    PICK_UP_PILE = "PICK_UP_PILE"

class WebSocketMessageIn(BaseModel):
    type: ActionType
    payload: Dict[str, Any]