# Fantasy Macedonia (FFM)

Fantasy Macedonia is a fantasy football project based on the Macedonian First League (Prva Makedonska Fudbalska Liga).

The project consists of a Django REST API, a Python data pipeline and a React frontend.

## Project Status

### Data Pipeline
- [x] Collect team and player data from Transfermarkt
- [x] Prepare player and team datasets
- [x] Calculate estimated fantasy player prices in MKD
- [x] Export datasets for the backend

### Backend
- [x] Django and Django REST Framework API
- [x] Team and player models
- [x] User registration and token authentication
- [x] Fantasy squad validation
- [x] Fantasy scoring logic
- [x] Automated tests

### Frontend
- [x] React application created with Vite
- [x] Dark-themed fantasy football dashboard
- [x] Player market with search and position filters
- [x] Player selection and removal
- [x] Squad size and position limits
- [x] Budget and squad value calculations
- [x] Starting XI selection and player replacement
- [x] Formation selection
- [x] Captain selection
- [x] Interactive football pitch
- [x] Local squad saving using browser localStorage
- [ ] Bench-to-starting XI substitution workflow
- [ ] Connect the frontend to the Django API
- [ ] Authentication and server-side squad persistence

### Future Work
- [ ] Complete transfers and round management
- [ ] Automatic match statistics
- [ ] Live fantasy points and rankings
- [ ] Deployment
- [ ] Mobile application

## Game Rules

The initial squad rules are:

- **Squad size:** 15 players
- **Positions:** 2 goalkeepers, 5 defenders, 5 midfielders and 3 forwards
- **Club limit:** Maximum 3 players from one club
- **Budget:** 700,000 MKD
- **Starting lineup:** 11 players, with 4 substitutes
- **Captain:** Must be in the starting lineup and receives double points

The backend contains squad validation and scoring logic. The frontend currently uses illustrative demo player data and stores the squad locally in the browser.

## Project Structure

```text
fantasy-macedonia/
├── backend/       Django REST API
├── scraping/      Player data collection and price calculation
├── frontend/      React + Vite application
├── README.md
└── .gitignore
```

Additional documentation:

- [Backend README](backend/README.md)
- [Scraping README](scraping/README.md)
- [Frontend README](frontend/README.md)

## Tech Stack

| Component | Technologies |
|---|---|
| Frontend | React 19, Vite 8, JavaScript, CSS |
| Backend | Python 3.13, Django 6, Django REST Framework |
| Data pipeline | Python, transfermarkt-api |
| Development database | SQLite |

## Getting Started

### 1. Backend

Requires Python 3.13.

```bash
cd backend
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py import_players
python manage.py import_prices
python manage.py createsuperuser
python manage.py runserver
```

The backend runs at `http://127.0.0.1:8000/`.

See [backend/README.md](backend/README.md) for API details and tests.

### 2. Frontend

Requires Node.js and npm.

```bash
cd frontend
npm install
npm run dev
```

Vite prints the local development URL in the terminal, usually `http://localhost:5173/`.

Useful commands:

```bash
npm run dev       # Start development server
npm run build     # Build for production
npm run preview   # Preview production build
npm run lint      # Run ESLint
```

See [frontend/README.md](frontend/README.md) for more details.

### 3. Scraping

The scraping scripts have their own Python environment.

```bash
cd scraping
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

See [scraping/README.md](scraping/README.md) before running the scripts.

## Data Source

Player and team data is collected from Transfermarkt using an unofficial API package. Automated requests are rate-limited, and generated datasets are stored locally.

This project is under development. Check Transfermarkt's terms and the relevant data licensing requirements before any public release.

## Author

Sashko
