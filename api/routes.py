from fastapi import APIRouter
from api.models import *
from game.manager import game_manager
router = APIRouter()

@router.post("/games", response_model=CreateGameResponse, status_code=201)
async def create_game(request: CreateGameRequest):
    game, player_id = game_manager.create_game(request)
    return CreateGameResponse(game_id= game.game_id, player_id=player_id)


@router.get("/games", response_model=GetGamesResponse, status_code=200)
async def get_games():
    return GetGamesResponse(games= game_manager.active_games.keys())