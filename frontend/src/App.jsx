
import { useEffect, useState } from "react";
import "./App.css";

const positionLimits = {
  Goalkeeper: 2,
  Defender: 5,
  Midfielder: 5,
  Forward: 3,
};

const formations = {
  "3-4-3": { Goalkeeper: 1, Defender: 3, Midfielder: 4, Forward: 3 },
  "3-5-2": { Goalkeeper: 1, Defender: 3, Midfielder: 5, Forward: 2 },
  "4-3-3": { Goalkeeper: 1, Defender: 4, Midfielder: 3, Forward: 3 },
  "4-4-2": { Goalkeeper: 1, Defender: 4, Midfielder: 4, Forward: 2 },
  "4-5-1": { Goalkeeper: 1, Defender: 4, Midfielder: 5, Forward: 1 },
  "5-2-3": { Goalkeeper: 1, Defender: 5, Midfielder: 2, Forward: 3 },
  "5-3-2": { Goalkeeper: 1, Defender: 5, Midfielder: 3, Forward: 2 },
  "5-4-1": { Goalkeeper: 1, Defender: 5, Midfielder: 4, Forward: 1 },
};

const demoPlayers = [
  { id: 1, name: "Filip Gachevski", position: "Goalkeeper", price: 30000 },
  { id: 2, name: "Darko Velkovski", position: "Defender", price: 35000 },
  { id: 3, name: "Ennur Totre", position: "Midfielder", price: 30000 },
  { id: 4, name: "Ivan Nikolov", position: "Forward", price: 20000 },
  { id: 5, name: "David Denkovski", position: "Goalkeeper", price: 25000 },
  { id: 6, name: "Stefan Ashkovski", position: "Defender", price: 25000 },
  { id: 7, name: "Bojan Ilievski", position: "Midfielder", price: 25000 },
  { id: 8, name: "Petar Petkovski", position: "Forward", price: 20000 },
  { id: 9, name: "Martin Tomovski", position: "Goalkeeper", price: 20000 },
  { id: 10, name: "Aleksandar Ristovski", position: "Defender", price: 22000 },
  { id: 11, name: "Stefan Kitanovski", position: "Defender", price: 25000 },
  { id: 12, name: "Marko Gjorgjiev", position: "Midfielder", price: 28000 },
  { id: 13, name: "Filip Stojanovski", position: "Midfielder", price: 24000 },
  { id: 14, name: "Andrej Todorovski", position: "Forward", price: 26000 },
  { id: 15, name: "Nikola Karakolev", position: "Forward", price: 23000 },
  { id: 16, name: "Viktor Velkov", position: "Defender", price: 20000 },
  { id: 17, name: "Bojan Trajkovski", position: "Defender", price: 22000 },
  { id: 18, name: "Stefan Radevski", position: "Defender", price: 24000 },
  { id: 19, name: "Martin Stojanov", position: "Defender", price: 20000 },
  { id: 20, name: "David Atanasov", position: "Midfielder", price: 26000 },
  { id: 21, name: "Kristijan Naumov", position: "Midfielder", price: 23000 },
  { id: 22, name: "Daniel Petrov", position: "Midfielder", price: 25000 },
  { id: 23, name: "Luka Mitrevski", position: "Midfielder", price: 21000 },
  { id: 24, name: "Matej Angelov", position: "Forward", price: 27000 },
  { id: 25, name: "Filip Kostov", position: "Forward", price: 24000 },
  { id: 26, name: "Jovan Spasovski", position: "Forward", price: 22000 },
  { id: 27, name: "Aleksandar Iliev", position: "Goalkeeper", price: 28000 },
  { id: 28, name: "Mihail Dimitrievski", position: "Defender", price: 19000 },
];

function loadSavedSquad() {
  try {
    return JSON.parse(localStorage.getItem("fantasySquad")) || {};
  } catch {
    return {};
  }
}

function App() {
  const [savedData] = useState(() => loadSavedSquad());

  const [selectedPlayers, setSelectedPlayers] = useState(
    () => savedData.selectedPlayers || [],
  );

  const [startingPlayers, setStartingPlayers] = useState(
    () => savedData.startingPlayers || [],
  );

  const [captainId, setCaptainId] = useState(
    () => savedData.captainId ?? null,
  );

  const [formation, setFormation] = useState(() => {
    const saved = savedData.formation;
    return formations[saved] ? saved : "4-3-3";
  });

  const [activePosition, setActivePosition] = useState(null);
  const [activePlayerId, setActivePlayerId] = useState(null);
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  const [activeTab, setActiveTab] = useState("dashboard");

  const [marketSearch, setMarketSearch] = useState("");
  const [positionFilter, setPositionFilter] = useState("All");
  const [sortOrder, setSortOrder] = useState("name");

  const formationSlots = formations[formation];

  useEffect(() => {
    const handleBeforeUnload = (event) => {
      if (!hasUnsavedChanges) return;
      event.preventDefault();
      event.returnValue = "";
    };

    window.addEventListener("beforeunload", handleBeforeUnload);

    return () => {
      window.removeEventListener("beforeunload", handleBeforeUnload);
    };
  }, [hasUnsavedChanges]);

  const squadValue = selectedPlayers.reduce(
    (total, player) => total + player.price,
    0,
  );

  const remainingBudget = 700000 - squadValue;

  const closeSelection = () => {
    setActivePosition(null);
    setActivePlayerId(null);
  };

  const changeTab = (tab) => {
    closeSelection();
    setActiveTab(tab);
  };

  const changeFormation = (newFormation) => {
    if (!formations[newFormation]) return;

    const slots = formations[newFormation];
    const keptStarters = [];

    Object.keys(slots).forEach((position) => {
      const playersInPosition = startingPlayers.filter(
        (player) => player.position === position,
      );

      const captain = playersInPosition.find(
        (player) => player.id === captainId,
      );

      const otherPlayers = playersInPosition.filter(
        (player) => player.id !== captainId,
      );

      if (captain && slots[position] > 0) {
        keptStarters.push(
          captain,
          ...otherPlayers.slice(0, slots[position] - 1),
        );
      } else {
        keptStarters.push(...otherPlayers.slice(0, slots[position]));
      }
    });

    setStartingPlayers(keptStarters);
    setFormation(newFormation);
    setHasUnsavedChanges(true);
    closeSelection();
  };

  const selectStarter = (player) => {
    const alreadyStarting = startingPlayers.some(
      (starter) => starter.id === player.id,
    );

    if (alreadyStarting && player.id !== activePlayerId) return;

    if (!activePlayerId) {
      const currentCount = startingPlayers.filter(
        (starter) => starter.position === player.position,
      ).length;

      if (currentCount >= formationSlots[player.position]) return;
    }

    const updatedStarters = activePlayerId
      ? startingPlayers.map((starter) =>
          starter.id === activePlayerId ? player : starter,
        )
      : [...startingPlayers, player];

    setStartingPlayers(updatedStarters);
    setHasUnsavedChanges(true);
    closeSelection();
  };

  const removeStarter = (player) => {
    setStartingPlayers(
      startingPlayers.filter((starter) => starter.id !== player.id),
    );

    if (captainId === player.id) {
      setCaptainId(null);
    }

    setHasUnsavedChanges(true);
    closeSelection();
  };

  const addPlayer = (player) => {
    const isSelected = selectedPlayers.some(
      (selected) => selected.id === player.id,
    );

    if (isSelected || selectedPlayers.length >= 15) return;

    const playersInPosition = selectedPlayers.filter(
      (selected) => selected.position === player.position,
    ).length;

    if (playersInPosition >= positionLimits[player.position]) return;
    if (player.price > remainingBudget) return;

    setSelectedPlayers([...selectedPlayers, player]);
    setHasUnsavedChanges(true);
  };

  const removePlayer = (player) => {
    setSelectedPlayers(
      selectedPlayers.filter((selected) => selected.id !== player.id),
    );

    setStartingPlayers(
      startingPlayers.filter((starter) => starter.id !== player.id),
    );

    if (captainId === player.id) {
      setCaptainId(null);
    }

    setHasUnsavedChanges(true);
    closeSelection();
  };

  const saveSquad = () => {
    localStorage.setItem(
      "fantasySquad",
      JSON.stringify({
        selectedPlayers,
        startingPlayers,
        captainId,
        formation,
      }),
    );

    setHasUnsavedChanges(false);
    alert("Squad saved successfully!");
  };

  const renderPitchRow = (position, interactive = true) => {
    const starters = startingPlayers.filter(
      (player) => player.position === position,
    );

    const emptySlots = Math.max(
      0,
      formationSlots[position] - starters.length,
    );

    return (
      <div className="pitch-row" key={position}>
        {starters.map((player) => (
          <button
            key={player.id}
            onClick={
              interactive
                ? () => {
                    setActivePosition(position);
                    setActivePlayerId(player.id);
                  }
                : undefined
            }
            disabled={!interactive}
            title={interactive ? "Click to replace player" : player.name}
          >
            {player.name}
            {captainId === player.id && " ⭐"}
          </button>
        ))}

        {interactive &&
          Array.from({ length: emptySlots }).map((_, index) => (
            <button
              key={`empty-${position}-${index}`}
              onClick={() => {
                setActivePosition(position);
                setActivePlayerId(null);
              }}
            >
              + {position}
            </button>
          ))}

        {!interactive &&
          Array.from({ length: emptySlots }).map((_, index) => (
            <span key={`empty-${position}-${index}`}>
              Empty {position}
            </span>
          ))}
      </div>
    );
  };

  
  const renderPlayerSelection = () => {
    if (!activePosition) return null;

    const activePlayer = startingPlayers.find(
      (player) => player.id === activePlayerId,
    );

    return (
      <div className="player-selection">
        <h3>
          {activePlayerId ? "Manage Player" : `Choose a ${activePosition}`}
        </h3>

        {activePlayer && (
          <div className="player-item">
            <span>{activePlayer.name}</span>

            <button
              onClick={() => {
                setCaptainId(activePlayer.id);
                setHasUnsavedChanges(true);
                closeSelection();
              }}
              disabled={captainId === activePlayer.id}
            >
              {captainId === activePlayer.id ? "⭐ Captain" : "Make Captain"}
            </button>
          </div>
        )}

        {selectedPlayers
          .filter(
            (player) =>
              player.position === activePosition &&
              (!startingPlayers.some(
                (starter) => starter.id === player.id,
              ) ||
                player.id === activePlayerId),
          )
          .map((player) => (
            <div key={player.id} className="player-item">
              <span>
                {player.name} — {player.price.toLocaleString()} MKD
              </span>
              <button onClick={() => selectStarter(player)}>
                Replace
              </button>
            </div>
          ))}

        {activePlayerId && (
          <button onClick={() => removeStarter(activePlayer)}>
            Remove from Starting XI
          </button>
        )}

        <button onClick={closeSelection}>Cancel</button>
      </div>
    );
  };


  const filteredPlayers = demoPlayers
    .filter((player) => {
      const matchesPosition =
        positionFilter === "All" || player.position === positionFilter;

      const matchesSearch = player.name
        .toLowerCase()
        .includes(marketSearch.toLowerCase());

      return matchesPosition && matchesSearch;
    })
    .sort((a, b) => {
      if (sortOrder === "price-low") return a.price - b.price;
      if (sortOrder === "price-high") return b.price - a.price;
      return a.name.localeCompare(b.name);
    });

  return (
    <div>
      <header className="navbar">
        <h2>
          FANTASY <span>MACEDONIA</span>
        </h2>

        <nav className="main-tabs">
          <button
            className={activeTab === "dashboard" ? "active" : ""}
            onClick={() => changeTab("dashboard")}
          >
            Dashboard
          </button>

          <button
            className={activeTab === "market" ? "active" : ""}
            onClick={() => changeTab("market")}
          >
            Player Market
          </button>

          <button
            className={activeTab === "squad" ? "active" : ""}
            onClick={() => changeTab("squad")}
          >
            My Squad
          </button>
        </nav>
      </header>

      {/* SIMPLE DASHBOARD */}
      {activeTab === "dashboard" && (
        <main className="dashboard">
          <div className="dashboard-heading">
            <div>
              <p className="dashboard-eyebrow">FANTASY MACEDONIA</p>
              <h1>My Team</h1>
              <p>Manage your squad and prepare your starting XI.</p>
            </div>

            <button onClick={() => changeTab("squad")}>
              Manage Squad →
            </button>
          </div>

          <div className="stats">
            <div className="stat-card">
              <p>Players selected</p>
              <h2>{selectedPlayers.length} / 15</h2>
            </div>

            <div className="stat-card">
              <p>Starting XI</p>
              <h2>{startingPlayers.length} / 11</h2>
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

          <section className="dashboard-panel">
            <div className="panel-heading">
              <div>
                <h2>Starting XI</h2>
                <p>{formation} formation</p>
              </div>

              <button onClick={() => changeTab("squad")}>
                Edit Team →
              </button>
            </div>

            <div className="football-pitch preview-pitch">
              {renderPitchRow("Forward", false)}
              {renderPitchRow("Midfielder", false)}
              {renderPitchRow("Defender", false)}
              {renderPitchRow("Goalkeeper", false)}
            </div>

            {startingPlayers.length === 0 && (
              <p className="empty-message">
                Your team is empty. Visit the Player Market to get started.
              </p>
            )}
          </section>
        </main>
      )}

      {/* PLAYER MARKET */}
      {activeTab === "market" && (
        <main className="player-market">
          <div className="section-heading">
            <div>
              <p className="dashboard-eyebrow">BUILD YOUR TEAM</p>
              <h1>Player Market</h1>
              <p>Find players and build your 15-player squad.</p>
            </div>

            <div className="market-budget">
              <span>Remaining budget</span>
              <strong>{remainingBudget.toLocaleString()} MKD</strong>
            </div>
          </div>

          <div className="market-controls">
            <input
              type="search"
              placeholder="Search players..."
              value={marketSearch}
              onChange={(event) => setMarketSearch(event.target.value)}
            />

            <select
              value={positionFilter}
              onChange={(event) => setPositionFilter(event.target.value)}
            >
              <option value="All">All positions</option>
              <option value="Goalkeeper">Goalkeepers</option>
              <option value="Defender">Defenders</option>
              <option value="Midfielder">Midfielders</option>
              <option value="Forward">Forwards</option>
            </select>

            <select
              value={sortOrder}
              onChange={(event) => setSortOrder(event.target.value)}
            >
              <option value="name">Sort by name</option>
              <option value="price-low">Price: low to high</option>
              <option value="price-high">Price: high to low</option>
            </select>
          </div>

          <p>
            {selectedPlayers.length} / 15 players selected
          </p>

          {filteredPlayers.map((player) => {
            const isSelected = selectedPlayers.some(
              (selected) => selected.id === player.id,
            );

            const playerInPosition = selectedPlayers.filter(
              (selected) => selected.position === player.position,
            ).length;

            const canAdd =
              !isSelected &&
              selectedPlayers.length < 15 &&
              playerInPosition < positionLimits[player.position] &&
              player.price <= remainingBudget;

            return (
              <div key={player.id} className="player-item">
                <span>
                  {player.name} — {player.position} —{" "}
                  {player.price.toLocaleString()} MKD
                </span>

                <button
                  onClick={() => addPlayer(player)}
                  disabled={!canAdd}
                >
                  {isSelected ? "Added" : "Add"}
                </button>
              </div>
            );
          })}

          {filteredPlayers.length === 0 && (
            <p>No players found.</p>
          )}
        </main>
      )}

      {/* MY SQUAD */}
      {activeTab === "squad" && (
        <main className="squad-page">
          <div className="section-heading">
            <div>
              <p className="dashboard-eyebrow">YOUR TEAM MANAGEMENT</p>
              <h1>My Squad</h1>
              <p>Choose your formation, starting XI and captain.</p>
            </div>

            <button className="save-squad-button" onClick={saveSquad}>
              Save Squad
            </button>
          </div>

          <div className="stats">
            <div className="stat-card">
              <p>Players selected</p>
              <h2>{selectedPlayers.length} / 15</h2>
            </div>

            <div className="stat-card">
              <p>Starting XI</p>
              <h2>{startingPlayers.length} / 11</h2>
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

          <section className="football-pitch">
            <div className="pitch-heading">
              <div>
                <h2>Starting XI</h2>
                <p>Click a player or empty position to make changes.</p>
              </div>

              <div className="formation-selector">
                <label htmlFor="formation">Formation:</label>

                <select
                  id="formation"
                  value={formation}
                  onChange={(event) => changeFormation(event.target.value)}
                >
                  {Object.keys(formations).map((name) => (
                    <option key={name} value={name}>
                      {name}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="pitch-players">
              {renderPitchRow("Forward")}
              {renderPitchRow("Midfielder")}
              {renderPitchRow("Defender")}
              {renderPitchRow("Goalkeeper")}
            </div>

            {renderPlayerSelection()}
          </section>

          <section className="selected-players">
            <h2>Full Squad</h2>
            <p>Manage your starters, substitutes and captain.</p>

            {selectedPlayers.length === 0 ? (
              <p>
                No players selected yet. Visit the Player Market to add players.
              </p>
            ) : (
              selectedPlayers.map((player) => {
                const isStarter = startingPlayers.some(
                  (starter) => starter.id === player.id,
                );

                const positionFull =
                  startingPlayers.filter(
                    (starter) => starter.position === player.position,
                  ).length >= formationSlots[player.position];

                return (
                  <div key={player.id} className="player-item">
                    <span>
                      {player.name} — {player.position} —{" "}
                      {player.price.toLocaleString()} MKD
                      {isStarter && " ⭐"}
                      {captainId === player.id && " (Captain)"}
                    </span>

                    <button
                      onClick={() => {
                        setActivePosition(player.position);
                        setActivePlayerId(null);
                      }}
                      disabled={isStarter || positionFull}
                    >
                      {isStarter ? "In Starting XI" : "Select on Pitch"}
                    </button>

                    <button onClick={() => removePlayer(player)}>
                      Remove
                    </button>

                    <button
                      onClick={() => {
                        if (isStarter) {
                          setCaptainId(player.id);
                          setHasUnsavedChanges(true);
                        }
                      }}
                      disabled={!isStarter}
                    >
                      {captainId === player.id ? "⭐ Captain" : "Set Captain"}
                    </button>
                  </div>
                );
              })
            )}
          </section>
        </main>
      )}
    </div>
  );
}

export default App;
