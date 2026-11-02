import { useState } from 'react'
import './App.css'

const positionLimits = {
  Goalkeeper: 2,
  Defender: 5,
  Midfielder: 5,
  Forward: 3,
}

const demoPlayers = [
  { id: 1, name: 'Filip Gachevski', position: 'Goalkeeper', price: 30000 },
  { id: 2, name: 'Darko Velkovski', position: 'Defender', price: 35000 },
  { id: 3, name: 'Ennur Totre', position: 'Midfielder', price: 30000 },
  { id: 4, name: 'Ivan Nikolov', position: 'Forward', price: 20000 },
  { id: 5, name: 'David Denkovski', position: 'Goalkeeper', price: 25000 },
  { id: 6, name: 'Stefan Ashkovski', position: 'Defender', price: 25000 },
  { id: 7, name: 'Bojan Ilievski', position: 'Midfielder', price: 25000 },
  { id: 8, name: 'Petar Petkovski', position: 'Forward', price: 20000 },
  { id: 9, name: 'Demo Goalkeeper 3', position: 'Goalkeeper', price: 20000 },
  { id: 10, name: 'Demo Defender 3', position: 'Defender', price: 22000 },
  { id: 11, name: 'Demo Defender 4', position: 'Defender', price: 25000 },
  { id: 12, name: 'Demo Midfielder 3', position: 'Midfielder', price: 28000 },
  { id: 13, name: 'Demo Midfielder 4', position: 'Midfielder', price: 24000 },
  { id: 14, name: 'Demo Forward 3', position: 'Forward', price: 26000 },
  { id: 15, name: 'Demo Forward 4', position: 'Forward', price: 23000 },
  { id: 16, name: 'Demo Defender 5', position: 'Defender', price: 20000 },
  { id: 17, name: 'Demo Defender 6', position: 'Defender', price: 22000 },
  { id: 18, name: 'Demo Defender 7', position: 'Defender', price: 24000 },
  { id: 19, name: 'Demo Defender 8', position: 'Defender', price: 20000 },
  { id: 20, name: 'Demo Midfielder 5', position: 'Midfielder', price: 26000 },
  { id: 21, name: 'Demo Midfielder 6', position: 'Midfielder', price: 23000 },
  { id: 22, name: 'Demo Midfielder 7', position: 'Midfielder', price: 25000 },
  { id: 23, name: 'Demo Midfielder 8', position: 'Midfielder', price: 21000 },
  { id: 24, name: 'Demo Forward 5', position: 'Forward', price: 27000 },
  { id: 25, name: 'Demo Forward 6', position: 'Forward', price: 24000 },
  { id: 26, name: 'Demo Forward 7', position: 'Forward', price: 22000 },
  { id: 27, name: 'Demo Goalkeeper 4', position: 'Goalkeeper', price: 28000 },
  { id: 28, name: 'Demo Defender 9', position: 'Defender', price: 19000 },
]

function App() {
  const [selectedPlayers, setSelectedPlayers] = useState([])
  const squadValue = selectedPlayers.reduce(
  (total, player) => total + player.price,
  0
)

const remainingBudget = 700000 - squadValue
  return (
    <div>
      <header className="navbar">
        <h2>FANTASY <span>MACEDONIA</span></h2>

        <nav>
          <a href="#">Dashboard</a>
          <a href="#">My Squad</a>
          <a href="#">Player Market</a>
          <a href="#">Leagues</a>
        </nav>
      </header>

      <button
          onClick={() => {
            if (selectedPlayers.length < 15) {
              const nextPlayer = demoPlayers.find(player => {
                const alreadySelected = selectedPlayers.some(
                  selected => selected.id === player.id
                )

                const playersInPosition = selectedPlayers.filter(
                  selected => selected.position === player.position
                ).length

                return (
                  !alreadySelected &&
                  playersInPosition < positionLimits[player.position]
                )
              })
              if (nextPlayer){
                setSelectedPlayers([...selectedPlayers, nextPlayer])
              }
            }
          }}
          disabled={selectedPlayers.length >= 15
        }>
          Add Player
        </button>

      <div className="stats">
        <div className="stat-card">
          <p>Players selected</p>
          <h2>{selectedPlayers.length} / 15</h2>
        </div>
        <div className="stat-card">
          <p>Starting XI</p>
          <h2>0 / 11</h2>
        </div>
        <div className="stat-card">
          <p>Remaining budget</p>
          <h2>{remainingBudget.toLocaleString()} MKD</h2>
        </div>
        <div className="stat-card">
          <p>Squad value</p>
          <h2>{squadValue.toLocaleString()} MKD</h2>
        </div>
      </div>

      <div className="selected-players">
        <h2>My Squad</h2>
        {selectedPlayers.length === 0 ? (
          <p>No players selected yet.</p>
        ) : (
            selectedPlayers.map(player => (
              <div key={player.id} className="player-item">
                <span>{player.name} — {player.position}</span>

                <button
                  onClick={() => {
                    setSelectedPlayers(
                      selectedPlayers.filter(
                        selected => selected.id !== player.id
                      )
                    )
                  }}
                >
                  Remove
                </button>
              </div>
            ))
          )
        }
      </div>


      <h1>FANTASY MACEDONIA</h1>
      <p>Your fantasy football experience starts here.</p>
    </div>
  )
}

export default App