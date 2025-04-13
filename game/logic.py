import random
from typing import List, Optional, Any, Dict
from game.models import *

PALACE_VALUES = {
    Rank.TWO: 2, Rank.THREE: 3, Rank.FOUR: 4, Rank.FIVE: 5, Rank.SIX: 6,
    Rank.SEVEN: 7, Rank.EIGHT: 8, Rank.NINE: 9, Rank.TEN: 10, Rank.JACK: 11,
    Rank.QUEEN: 12, Rank.KING: 13, Rank.ACE: 14
}
RESET_CARD_RANK = Rank.TWO
CLEAR_PILE_RANK = Rank.TEN

class Player:
    def __init__(self, id: str, name: str):
        self.id: str = id
        self.name: str = name
        self.hand: List[Card] = []
        self.face_up: List[Card] = []
        self.face_down: List[Card] = []
        self.websocket: Optional[Any] = None

    def sort_hand(self):
        self.hand.sort()

    def get_state(self) -> PlayerState:
        """Returns a Pydantic model representation of the player's public state."""
        return PlayerState(
            id=self.id,
            name=self.name,
            hand=self.hand,
            face_up=self.face_up,
            face_down_count=len(self.face_down)
        )

    def get_hidden_state(self) -> PlayerState:
         """Returns state as seen by other players."""
         return PlayerState(
            id=self.id,
            name=self.name,
            hand=[Card(rank=Rank.TWO, suit=Suit.HEARTS)] * len(self.hand),
            face_up=self.face_up,
            face_down_count=len(self.face_down)
         )

class Game:
    def __init__(self, game_id: str, first_player: Player):
        self.game_id: str = game_id
        self.players: Dict[str, Player] = {first_player.id: first_player}
        self.player_order: List[str] = [first_player.id]
        self.deck: List[Card] = self.create_deck()
        self.pile: List[Card] = []
        self.current_player_index: Optional[int] = None
        self.phase: GamePhase = GamePhase.WAITING_FOR_PLAYERS
        self.winner_id: Optional[str] = None
        self.last_action: Optional[str] = "Game created"

    def create_deck(self) -> List[Card]:
        deck = [Card(rank=r, suit=s) for r in Rank for s in Suit]
        random.shuffle(deck)
        return deck

    def add_player(self, player: Player):
        if self.phase != GamePhase.WAITING_FOR_PLAYERS:
            raise Exception("Cannot add a player to a game that has started")
        if len(self.players) >= 5:
             raise Exception("Cannot add a player if there as game is at it's max of 5 players ")
        self.players[player.id] = player
        self.player_order.append(player.id)
        self.last_action = f"{player.name} joined the game."

    def deal_cards(self):
        number_players = len(self.players)
        if number_players < 2 or number_players > 5:
            return # invalid amount of players
        # Deal Face Down Cards
        for _ in range(3):
            for player in self.player_order:
                if self.deck:
                    self.players[player].face_down.append(self.deck.pop())
        # Deal Face Up Cards
        for _ in range(3):
            for player in self.player_order:
                if self.deck:
                    self.players[player].face_up.append(self.deck.pop())
        # Deal Hand Cards
        for _ in range(3):
            for player in self.player_order:
                if self.deck:
                    self.players[player].hand.append(self.deck.pop())
        for player in self.players.values():
            player.sort_hand()

        # TODO: Implement logic for determining starting player based on face up cards
        self.current_player_index = 0
        self.phase = GamePhase.PLAYING
        self.last_action = "Dealing complete. Game starts."
