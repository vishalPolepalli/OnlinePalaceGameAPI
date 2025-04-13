from fastapi import APIRouter, HTTPException
from api.models import *
from game.manager import game_manager

router = APIRouter()

@router.post("/games", response_model=CreateGameResponse, status_code=201)
async def create_game(request: CreateGameRequest):
    game, player_id = game_manager.create_game(request)
    return CreateGameResponse(game_id= game.game_id, player_id=player_id)

@router.get("/games", response_model=GetGamesResponse)
async def get_games():
    return GetGamesResponse(games= game_manager.active_games.keys())

@router.post("/games/{game_id}/join", response_model=JoinGameResponse)
async def join_game(game_id: str, request: JoinGameRequest):
    try:
        response = game_manager.add_player_to_game(game_id=game_id, player_name=request.player_name)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to join game: {e}")

@router.get("/games/{game_id}/players", response_model=GetPlayersResponse)
async def get_game(game_id: str):
    try:
        game = game_manager.get_game(game_id)
        return GetPlayersResponse(players= game.players.keys())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get players for game: {e}")