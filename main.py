"""
TravelBucks Rewards & Play Platform - Simplified API
FastAPI backend with core endpoints
"""
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="TravelBucks Rewards & Play Platform",
    description="Gamified travel rewards platform with membership tiers, entertainment games, and sweepstakes",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "service": "TravelBucks Rewards & Play Platform",
        "status": "online",
        "version": "1.0.0",
        "message": "Welcome to TravelBucks! Your gamified travel rewards platform."
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "travelbucks-api"}

@app.get("/api/v1/membership/tiers")
async def get_membership_tiers():
    """Get all membership tiers"""
    return {
        "tiers": [
            {
                "id": 1,
                "name": "TravelBucks Go",
                "description": "Entry tier - Start your travel rewards journey",
                "price_monthly": 0.00,
                "price_annual": 0.00,
                "features": ["Basic rewards", "Game access", "Sweepstakes entry"]
            },
            {
                "id": 2,
                "name": "TravelBucks Plus",
                "description": "Enhanced tier - More rewards and benefits",
                "price_monthly": 9.99,
                "price_annual": 99.99,
                "features": ["2x rewards", "Premium games", "Priority support", "Monthly bonus TravelBucks"]
            },
            {
                "id": 3,
                "name": "TravelBucks Premium",
                "description": "Ultimate tier - Maximum rewards and exclusive perks",
                "price_monthly": 19.99,
                "price_annual": 199.99,
                "features": ["3x rewards", "All games", "VIP support", "Exclusive sweepstakes", "Travel concierge"]
            }
        ]
    }

@app.get("/api/v1/games")
async def get_games():
    """Get available entertainment games"""
    return {
        "games": [
            {"id": 1, "name": "Destination Dash", "type": "arcade", "cost_travelbucks": 10},
            {"id": 2, "name": "Travel Trivia Challenge", "type": "trivia", "cost_travelbucks": 5},
            {"id": 3, "name": "World Explorer Quest", "type": "adventure", "cost_travelbucks": 15},
            {"id": 4, "name": "Bucket List Bingo", "type": "bingo", "cost_travelbucks": 8},
            {"id": 5, "name": "Globe Spinner", "type": "wheel", "cost_travelbucks": 20}
        ]
    }

@app.get("/api/v1/sweepstakes/active")
async def get_active_sweepstakes():
    """Get currently active sweepstakes"""
    return {
        "sweepstakes": [
            {
                "id": 1,
                "title": "Dream Vacation to Hawaii",
                "description": "Win a 7-day all-inclusive trip to Maui",
                "entry_cost_travelbucks": 100,
                "amoe_available": True,
                "entries": 15234,
                "end_date": "2026-03-01T00:00:00Z"
            },
            {
                "id": 2,
                "title": "European Adventure Package",
                "description": "10-day tour of Italy, France, and Spain",
                "entry_cost_travelbucks": 150,
                "amoe_available": True,
                "entries": 8912,
                "end_date": "2026-04-15T00:00:00Z"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    # Read port from environment variable, default to 8080
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
