"""
TravelBucks Rewards Platform - Simplified Demo API
Demonstrates core features: Membership Tiers, Games, Sweepstakes, Travel Booking
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum
import random
import os

app = FastAPI(
    title="TravelBucks Rewards API",
    description="iOS Travel Rewards Platform with Games, Sweepstakes & Travel Booking",
    version="1.0.0"
)

# CORS for iOS app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== MODELS =====
class MembershipTier(str, Enum):
    FREE = "free"
    PREMIUM = "premium"
    ELITE = "elite"

class User(BaseModel):
    user_id: str
    email: str
    membership_tier: MembershipTier
    travelbucks_balance: int
    xp_points: int

class GameResult(BaseModel):
    game_id: str
    score: int
    xp_earned: int
    travelbucks_earned: int

class SweepstakesEntry(BaseModel):
    sweepstakes_id: str
    entry_method: str  # "purchase" or "amoe"
    
class TravelBooking(BaseModel):
    provider: str
    destination: str
    price: float
    travelbucks_applied: int

# ===== IN-MEMORY DATA (Demo) =====
users_db: Dict[str, User] = {}
sweepstakes_db = {
    "hawaii-trip-2026": {
        "id": "hawaii-trip-2026",
        "title": "Win a Trip to Hawaii!",
        "description": "5-day vacation package for 2",
        "prize_value": 5000,
        "entry_cost_travelbucks": 100,
        "end_date": "2026-03-01",
        "total_entries": 1523,
        "amoe_enabled": True
    },
    "europe-tour": {
        "id": "europe-tour",
        "title": "European Adventure Sweepstakes",
        "description": "10-day tour across 5 countries",
        "prize_value": 8000,
        "entry_cost_travelbucks": 150,
        "end_date": "2026-04-15",
        "total_entries": 891,
        "amoe_enabled": True
    }
}

games_db = {
    "word-search": {"name": "Travel Word Search", "xp_reward": 50},
    "trivia": {"name": "Travel Trivia", "xp_reward": 75},
    "match-3": {"name": "Destination Match", "xp_reward": 60},
    "memory": {"name": "Landmark Memory", "xp_reward": 55},
    "crossword": {"name": "Travel Crossword", "xp_reward": 80}
}

# ===== API ENDPOINTS =====
@app.get("/")
def root():
    return {
        "app": "TravelBucks Rewards Platform",
        "version": "1.0.0",
        "status": "active",
        "features": [
            "3 Membership Tiers (Free/Premium/Elite)",
            "5 Entertainment Games with XP rewards",
            "Sweepstakes with AMOE compliance",
            "Travel Booking Integration (5 providers)",
            "TravelBucks & XP Ledger System"
        ],
        "endpoints": {
            "health": "/health",
            "user": "/api/user/{user_id}",
            "games": "/api/games",
            "sweepstakes": "/api/sweepstakes",
            "booking": "/api/booking/providers"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected",
        "services": {
            "games": "operational",
            "sweepstakes": "operational",
            "booking": "operational"
        }
    }

@app.post("/api/user/register")
def register_user(email: str, tier: MembershipTier = MembershipTier.FREE):
    user_id = f"user_{len(users_db) + 1}"
    user = User(
        user_id=user_id,
        email=email,
        membership_tier=tier,
        travelbucks_balance=1000 if tier == MembershipTier.FREE else 5000,
        xp_points=0
    )
    users_db[user_id] = user
    return {
        "success": True,
        "user": user,
        "welcome_bonus": user.travelbucks_balance
    }

@app.get("/api/user/{user_id}")
def get_user(user_id: str):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.get("/api/games")
def list_games():
    return {
        "games": [
            {"id": k, **v} for k, v in games_db.items()
        ],
        "total_games": len(games_db)
    }

@app.post("/api/games/play")
def play_game(user_id: str, game_id: str, score: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Game not found")
    
    user = users_db[user_id]
    game = games_db[game_id]
    
    # Calculate rewards based on score
    xp_earned = game["xp_reward"]
    travelbucks_earned = max(10, score // 10)
    
    # Apply membership tier multipliers
    multipliers = {
        MembershipTier.FREE: 1.0,
        MembershipTier.PREMIUM: 1.5,
        MembershipTier.ELITE: 2.0
    }
    multiplier = multipliers[user.membership_tier]
    xp_earned = int(xp_earned * multiplier)
    travelbucks_earned = int(travelbucks_earned * multiplier)
    
    # Update user
    user.xp_points += xp_earned
    user.travelbucks_balance += travelbucks_earned
    
    return GameResult(
        game_id=game_id,
        score=score,
        xp_earned=xp_earned,
        travelbucks_earned=travelbucks_earned
    )

@app.get("/api/sweepstakes")
def list_sweepstakes():
    return {
        "active_sweepstakes": list(sweepstakes_db.values()),
        "total": len(sweepstakes_db)
    }

@app.post("/api/sweepstakes/enter")
def enter_sweepstakes(user_id: str, sweepstakes_id: str, entry_method: str = "purchase"):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    if sweepstakes_id not in sweepstakes_db:
        raise HTTPException(status_code=404, detail="Sweepstakes not found")
    
    user = users_db[user_id]
    sweepstakes = sweepstakes_db[sweepstakes_id]
    
    if entry_method == "purchase":
        cost = sweepstakes["entry_cost_travelbucks"]
        if user.travelbucks_balance < cost:
            raise HTTPException(status_code=400, detail="Insufficient TravelBucks")
        user.travelbucks_balance -= cost
    
    sweepstakes["total_entries"] += 1
    
    return {
        "success": True,
        "entry_method": entry_method,
        "sweepstakes": sweepstakes["title"],
        "entry_number": sweepstakes["total_entries"],
        "remaining_balance": user.travelbucks_balance
    }

@app.get("/api/sweepstakes/amoe/{sweepstakes_id}")
def get_amoe_info(sweepstakes_id: str):
    """Alternative Method of Entry - Free postal mail entry"""
    if sweepstakes_id not in sweepstakes_db:
        raise HTTPException(status_code=404, detail="Sweepstakes not found")
    
    return {
        "sweepstakes_id": sweepstakes_id,
        "amoe_enabled": True,
        "instructions": "Mail a 3x5 card with your name, email, and sweepstakes ID to: TravelBucks AMOE, PO Box 12345, San Francisco, CA 94101",
        "rules": "No purchase necessary. Void where prohibited. Must be 18+. One entry per envelope.",
        "deadline": sweepstakes_db[sweepstakes_id]["end_date"]
    }

@app.get("/api/booking/providers")
def list_providers():
    return {
        "providers": [
            {"id": "travel-leaders", "name": "Travel Leaders Network", "type": "agency"},
            {"id": "expedia-taap", "name": "Expedia TAAP", "type": "taap"},
            {"id": "vax", "name": "VAX VacationAccess", "type": "taap"},
            {"id": "carnival", "name": "Carnival Cruise Line", "type": "direct"},
            {"id": "hotelbeds", "name": "Hotelbeds", "type": "aggregator"}
        ]
    }

@app.post("/api/booking/search")
def search_travel(provider: str, destination: str, checkin: str, checkout: str):
    # Simulated search results
    base_price = random.randint(500, 3000)
    return {
        "provider": provider,
        "results": [
            {
                "id": f"result_{i}",
                "name": f"Amazing {destination} Hotel {i+1}",
                "price": base_price + (i * 100),
                "rating": round(4.0 + random.random(), 1),
                "travelbucks_eligible": True
            }
            for i in range(3)
        ]
    }

@app.post("/api/booking/book")
def book_travel(user_id: str, provider: str, destination: str, price: float, travelbucks_to_apply: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[user_id]
    
    if travelbucks_to_apply > user.travelbucks_balance:
        raise HTTPException(status_code=400, detail="Insufficient TravelBucks")
    
    # 1 TravelBuck = $0.01 USD
    discount = travelbucks_to_apply * 0.01
    final_price = max(0, price - discount)
    
    user.travelbucks_balance -= travelbucks_to_apply
    
    return {
        "booking_id": f"booking_{random.randint(10000, 99999)}",
        "provider": provider,
        "destination": destination,
        "original_price": price,
        "travelbucks_applied": travelbucks_to_apply,
        "discount": discount,
        "final_price": final_price,
        "confirmation": "CONFIRMED",
        "remaining_travelbucks": user.travelbucks_balance
    }

@app.get("/api/leaderboard")
def get_leaderboard():
    sorted_users = sorted(users_db.values(), key=lambda u: u.xp_points, reverse=True)
    return {
        "leaderboard": [
            {
                "rank": i + 1,
                "user_id": user.user_id,
                "xp_points": user.xp_points,
                "membership_tier": user.membership_tier
            }
            for i, user in enumerate(sorted_users[:10])
        ]
    }

@app.get("/api/membership/tiers")
def get_membership_tiers():
    return {
        "tiers": [
            {
                "id": "free",
                "name": "Free",
                "cost": 0,
                "benefits": ["Access to all 5 games", "1x XP & TravelBucks", "Enter sweepstakes"],
                "multiplier": 1.0
            },
            {
                "id": "premium",
                "name": "Premium",
                "cost": 9.99,
                "benefits": ["All Free benefits", "1.5x XP & TravelBucks", "Exclusive sweepstakes", "Priority support"],
                "multiplier": 1.5
            },
            {
                "id": "elite",
                "name": "Elite",
                "cost": 29.99,
                "benefits": ["All Premium benefits", "2x XP & TravelBucks", "VIP sweepstakes", "Concierge service", "Early access"],
                "multiplier": 2.0
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
