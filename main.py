from fastapi import FastAPI
from api.routes import router as game_router # Import the router
app = FastAPI(
    title="Palace Card Game Backend",
    description="API and WebSocket server for a multiplayer Palace game.",
    version="0.1.0",
)

app.include_router(game_router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Palace Game Backend!"}
