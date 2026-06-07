# Tenzi — The Football Oracle 

A football-themed Akinator-style guessing game. Think of a player, team or nation and Tenzi will try to guess who you're thinking of.


## How it works
1. Choose a category — Player, Club, or Nation
2. Answer yes/no questions about who you're thinking of
3. Tenzi narrows down the candidates using a binary search algorithm
4. The Football Oracle makes its guess!

## Features
- 25 top football players from Premier League, La Liga, Bundesliga, Ligue 1 and Serie A
- 25 clubs from Europe's top 5 leagues
- 16 World Cup nations
- Smart algorithm that picks the best question each round to narrow down candidates
- If the first guess is wrong, Tenzi keeps asking until it finds the answer
- Football-themed UI with pitch design, stadium atmosphere and World Cup colors

## Tech Stack
- **Backend:** Python, Flask (REST API)
- **Database:** MySQL
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Data:** Real football data via RapidAPI

## Architecture
This project uses a modern SPA architecture:
- Flask serves only JSON responses (no HTML templates)
- JavaScript handles all UI rendering and screen transitions
- REST API endpoints for game logic

## API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/game/start` | POST | Start a new game, returns candidate IDs |
| `/api/game/question` | POST | Get the best next question |
| `/api/game/answer` | POST | Submit answer, returns filtered candidates |
| `/api/character/:id` | GET | Get character details for final guess |

## How to run locally
1. Clone the repo
2. Install dependencies:pip3 install flask flask-cors pymysql python-dotenv requests
3. Create a `.env` file:
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=tenzi_db
RAPIDAPI_KEY=your_key
4. Set up MySQL database and run `seed.py`
5. Run:
python3 app.py
6. Open `http://127.0.0.1:5000`
Commit it and tell me when done!
