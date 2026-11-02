# Fantasy Macedonia — Frontend

The frontend is the React web application for Fantasy Macedonia, a fantasy football project based on the Macedonian First League.

It is built with React 19 and Vite 8.

## Current Features

### Dashboard
- Dark-themed fantasy football interface
- Squad overview and statistics
- Starting XI preview

### Player Market
- Browse available demo players
- Search players by name
- Filter players by position
- Sort players by name or price
- Add players to the squad
- Automatic budget and position-limit validation

### Squad Management
- Select up to 15 players
- Position limits:
  - 2 goalkeepers
  - 5 defenders
  - 5 midfielders
  - 3 forwards
- 700,000 MKD starting budget
- Remaining budget and squad value calculations
- Interactive football pitch
- Formation selection:
  - 3-4-3
  - 3-5-2
  - 4-3-3
  - 4-4-2
  - 4-5-1
  - 5-2-3
  - 5-3-2
  - 5-4-1
- Starting XI selection and replacement
- Captain selection
- Remove players from the squad
- Save squad locally using browser localStorage
- Unsaved changes warning

## Current Limitations

- The frontend currently uses demo player data.
- It is not yet connected to the Django REST API.
- Authentication is not implemented.
- Squad data is stored locally in the browser rather than on the server.
- Bench-to-starting XI substitution is still planned.
- Player statistics and fantasy points are not yet connected to real match data.

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

- Implement bench-to-starting XI substitutions
- Connect the frontend to the Django REST API
- Add user authentication
- Implement server-side squad persistence
- Add live match statistics and fantasy points
- Improve responsive layouts and styling
