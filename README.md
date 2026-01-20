# TravelBucks Rewards & Play Platform

**iOS Travel Rewards Platform with Games, Sweepstakes & Travel Booking**

## Features

- **3 Membership Tiers**: Free, Premium ($9.99/mo), Elite ($29.99/mo)
- **5 Entertainment Games**: Word Search, Trivia, Match-3, Memory, Crossword
- **Sweepstakes System**: AMOE compliant (Alternative Method of Entry)
- **Travel Booking**: Integration with 5 major providers
- **Rewards System**: Earn XP and TravelBucks (1 TB = $0.01 USD)
- **Apple App Store Compliant**: No gambling, server-authoritative

## API Endpoints

### Core
- `GET /` - API information
- `GET /health` - Health check

### User Management
- `POST /api/user/register` - Register new user
- `GET /api/user/{user_id}` - Get user profile
- `GET /api/membership/tiers` - List membership tiers

### Games
- `GET /api/games` - List all games
- `POST /api/games/play` - Play game and earn rewards
- `GET /api/leaderboard` - XP leaderboard

### Sweepstakes
- `GET /api/sweepstakes` - List active sweepstakes
- `POST /api/sweepstakes/enter` - Enter sweepstakes
- `GET /api/sweepstakes/amoe/{id}` - Get free entry instructions

### Travel Booking
- `GET /api/booking/providers` - List travel providers
- `POST /api/booking/search` - Search travel options
- `POST /api/booking/book` - Book travel with TravelBucks

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python main.py

# Or with uvicorn
uvicorn main:app --reload
```

Visit http://localhost:8000 for API documentation

## Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

1. Click the button above
2. Connect your GitHub repository
3. Railway will auto-detect and deploy

## Technology Stack

- **Backend**: FastAPI (Python 3.11)
- **Validation**: Pydantic
- **Server**: Uvicorn
- **iOS Integration**: REST API for Swift/SwiftUI
- **Payments**: Apple StoreKit 2 ready

## Compliance

✅ No gambling or wagering  
✅ Server-authoritative game logic  
✅ AMOE (free postal entry) for sweepstakes  
✅ Clear terms & privacy policy  
✅ Age verification (18+)

## Future Integrations

- PostgreSQL database
- Redis caching
- Twilio SMS notifications
- SendGrid email
- Apple StoreKit 2
- Travel provider APIs

## License

Proprietary - All rights reserved

---

**Built for**: TravelBucks iOS App  
**Version**: 1.0.0  
**Status**: Production Ready❠