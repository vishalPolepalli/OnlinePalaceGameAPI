from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

# MARK: Card
class Suit(str, Enum):
    HEARTS = "H"
    CLUBS = "C"
    DIAMONDS = "D"
    SPADES = "S"

class Rank(str, Enum):
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"

class Card(BaseModel):
    rank: Rank
    suit: Suit

    def __hash__(self):
        return hash((self.rank, self.suit))

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank == other.rank and self.suit == other.suit

# MARK: Player
class PlayerState(BaseModel):
    id: str
    name: str
    hand: List[Card] = Field(default_factory=list)
    face_up: List[Card] = Field(default_factory=list)
    face_down_count: int = 0

# MARK: Game
class GamePhase(str, Enum):
    WAITING_FOR_PLAYERS = "WAITING_FOR_PLAYERS"
    PLAYING = "PLAYING"
    FINISHED = "FINISHED"

class GameState(BaseModel):
    game_id: str
    players: List[PlayerState] = Field(default_factory=list)
    pile: List[Card] = Field(default_factory=list)
    deck_size: int = 0
    current_player_id: Optional[str] = None
    phase: GamePhase = GamePhase.WAITING_FOR_PLAYERS
    winner_id: Optional[str] = None
    last_action: Optional[str] = None