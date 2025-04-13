from typing import List
from pydantic import BaseModel

from game.logic import Player


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