import uuid
from typing import Dict, Optional
from fastapi import WebSocket
from game.logic import Game, Player
from api.models import *
from game.models import GamePhase

class GameManager:
    def __init__(self):
        self.active_games: Dict[str, Game] = {}
        self.player_connections: Dict[str, WebSocket] = {}

    def create_game(self, request: CreateGameRequest) -> tuple[Game, str]:
        # create the first player
        player_id = str(uuid.uuid4())
        player = Player(id=player_id, name=request.player_name)
        # create the game with the first player
        game_id = str(uuid.uuid4())[:6]
        game = Game(game_id=game_id, first_player=player)
        # add game to list of active games
        self.active_games[game_id] = game
        print(f"Game created: {game_id} by Player {player.name} ({player_id})")
        return game, player_id

    def get_game(self, game_id: str) -> Optional[Game]:
        game = self.active_games.get(game_id.lower())
        if not game:
            raise Exception(f"No game with id {game_id} found")
        return game

    def add_player_to_game(self, game_id: str, player_name: str) -> Optional[JoinGameResponse]:
        game = self.get_game(game_id)
        player_id = str(uuid.uuid4())
        player = Player(id=player_id, name=player_name)
        game.add_player(player)
        return JoinGameResponse(player_id=player_id)

    def connect_websocket(self, game_id: str, player_id: str, websocket: WebSocket):
        game = self.get_game(game_id)
        player = game.players.get(player_id)
        if not player:
            raise Exception(f"No player found")
        player.websocket = websocket
        self.player_connections[player_id] = websocket
        print(f"WebSocket connected for Player {player.name} ({player_id}) in game {game_id}")

    async def broadcast(self, game_id: str, message: Dict):
        game = self.get_game(game_id)
        websockets = [p.websocket for p in game.players.values() if p.websocket]
        for websocket in websockets:
            try:
                await websocket.send_json(message)
            except Exception as e:
                print(f"Error sending message to a websocket in game {game_id}: {e}")

    async def broadcast_game_state(self, game_id: str):
        game = self.get_game(game_id)

        message_type = "GAME_UPDATE"
        if game.phase == GamePhase.FINISHED:
            message_type = "GAME_FINISHED"

        for player in game.players.values():
            if player.websocket:
                state = game.get_game_status(perspective_player_id=player.id)
                message = WebSocketMessageOut(type=message_type, payload=state.model_dump())
                try:
                    await player.websocket.send_json(message.model_dump())
                except Exception as e:
                    print(f"Error sending state for player {player.id} in game {game_id}: {e}")

# Singleton to manage all games
game_manager = GameManager()