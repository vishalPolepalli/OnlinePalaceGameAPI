from random import random
from typing import List, Optional, Any, Dict
from .models import Card, PlayerState, GameState, Suit, Rank, GamePhase

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
        self.deck: List[Card] = self._create_deck()
        self.pile: List[Card] = []
        self.current_player_index: Optional[int] = None
        self.phase: GamePhase = GamePhase.WAITING_FOR_PLAYERS
        self.winner_id: Optional[str] = None
        self.last_action: Optional[str] = "Game created"

    def _create_deck(self) -> List[Card]:
        deck = [Card(rank=r, suit=s) for r in Rank for s in Suit]
        random.shuffle(deck)
        return deck

    def add_player(self, player: Player):
        if self.phase != GamePhase.WAITING_FOR_PLAYERS:
            return
        if len(self.players) >= 4:
             return
        self.players[player.id] = player
        self.player_order.append(player.id)
        self.last_action = f"{player.name} joined the game."