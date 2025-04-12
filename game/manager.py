import uuid
from typing import Dict
from fastapi import WebSocket
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
        game_id = str(uuid.uuid4())[:8]
        game = Game(game_id=game_id, first_player=player)
        # add game to list of active games
        self.active_games[game_id] = game
        print(f"Game created: {game_id} by Player {player.name} ({player_id})")
        return game, player_id
    