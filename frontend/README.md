# Fantasy Macedonia — Frontend

The frontend is the React web application for Fantasy Macedonia, a fantasy football project based on the Macedonian First League.

It is built with React 19 and Vite 8.

## Current Features

- Dark-themed fantasy football dashboard
- Squad selection using React state
- Maximum squad size of 15 players
- Position limits:
  - 2 goalkeepers
  - 5 defenders
  - 5 midfielders
  - 3 forwards
- Remaining budget calculation
- Total squad value calculation
- Selected-player list and removal

The current implementation uses demo player data. It is not yet connected to the Django backend.

## Requirements

- Node.js
- npm

## Installation

From the repository root:

```bash
cd frontend
npm install
```

## Development

Start the Vite development server:

```bash
npm run dev
```

Open the local URL printed in the terminal, usually:

`http://localhost:5173/`

Keep the terminal running while developing.

## Available Scripts

| Command | Description |
|---|---|
| `npm run dev` | Start the development server |
| `npm run build` | Create a production build |
| `npm run preview` | Preview the production build |
| `npm run lint` | Run ESLint |

## Project Structure

```text
frontend/
├── public/
├── src/
│   ├── assets/
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   └── main.jsx
├── index.html
├── package.json
├── package-lock.json
└── vite.config.js
```

## Planned Work

- Build an interactive player market
- Allow users to select individual players
- Implement starting XI and captain selection
- Connect to the Django REST API
- Add authentication and persistent squads
- Improve responsive layouts and styling