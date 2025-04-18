from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from api.models import *
from game.manager import game_manager
from game.models import GamePhase

router = APIRouter()

@router.post("/games", response_model=CreateGameResponse, status_code=201)
async def create_game(request: CreateGameRequest):
    game, player_id = game_manager.create_game(request)
    return CreateGameResponse(game_id= game.game_id.upper(), player_id=player_id)

@router.get("/games", response_model=GetGamesResponse)
async def get_games():
    return GetGamesResponse(games= game_manager.active_games.keys())

@router.post("/games/{game_id}/join", response_model=JoinGameResponse)
async def join_game(game_id: str, request: JoinGameRequest):
    try:
        response = game_manager.add_player_to_game(game_id=game_id, player_name=request.player_name)
        player = game_manager.get_game(game_id).players[response.player_id].get_hidden_state()
        message = WebSocketMessageOut(type="PLAYER_JOINED", payload= {"new_player": player.model_dump()})
        await game_manager.broadcast(game_id=game_id, message=message.model_dump())
        # await game_manager.broadcast_game_state(game_id=game_id) not sure if this is needed yet

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to join game: {e}")

@router.get("/games/{game_id}/players", response_model=GetPlayersResponse)
async def get_game_players(game_id: str):
    try:
        game = game_manager.get_game(game_id)
        return GetPlayersResponse(players= game.players.keys())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get players for game: {e}")

@router.post("/games/{game_id}/start")
async def start_game(game_id: str):
    try:
        game = game_manager.get_game(game_id)
        game.deal_cards()
        game.phase = GamePhase.STARTED

        # send message to all players that game has started
        await game_manager.broadcast_game_state(game_id=game_id)

        # send message to current player it's their turn
        current_player = game.get_current_player()
        if current_player and current_player.websocket:
            message = WebSocketMessageOut(type="YOUR_TURN", payload= {})
            await current_player.websocket.send_json(message.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start game {game_id}: {e}")


@router.websocket("/ws/game/{game_id}/{player_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str, player_id: str):
    try:
        game = game_manager.get_game(game_id)
        player = game.players.get(player_id)
        if not player:
            await websocket.close(code=1008, reason="Player not found in game: {game_id}")
            return

        await websocket.accept()
        game_manager.connect_websocket(game_id=game_id, player_id=player_id, websocket=websocket)

        initial_state=game.get_game_status(perspective_player_id=player_id)
        message = WebSocketMessageOut(type="CONNECTION_ESTABLISHED", payload=initial_state.model_dump())
        await websocket.send_json(message.model_dump())

        try:
            while True:
                data = await websocket.receive_json()
                message = WebSocketMessageIn(**data)

                if message.action_type == ActionType.PICK_UP_PILE:
                    game.pick_up_pile(player_id=player_id)

        except WebSocketDisconnect:
            print(f"WebSocket disconnected for Player {player_id} in game {game_id}")
            await game_manager.disconnect_websocket(game_id=game_id, player_id=player_id)

    except Exception as e:
        print(f"Error during WebSocket connection setup for {player_id} in {game_id}: {e}")
        try:
             await websocket.close(code=1011)
        except:
             pass
