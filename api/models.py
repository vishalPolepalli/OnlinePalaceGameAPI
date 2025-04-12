from pydantic import BaseModel


# --- API Request/Response Models ---
class CreateGameRequest(BaseModel):
    player_name: str
