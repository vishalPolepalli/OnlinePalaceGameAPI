import uuid
from typing import Dict, Optional
from fastapi import WebSocket

from api.models import JoinGameResponse
from game.logic import Game, Player
from api.models import *


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
        game = self.active_games.get(game_id)
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

# Singleton to manage all games
game_manager = GameManager()