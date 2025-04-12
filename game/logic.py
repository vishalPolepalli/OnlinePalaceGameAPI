from typing import List, Optional, Any

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