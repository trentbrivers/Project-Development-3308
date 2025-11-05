import { useState } from 'react';

export default function App() {
  //React is a Single Page Application framework, so everything needs to be handled by this main App component function.
  const [currentScreen, setCurrentScreen] = useState('title');
  // This is the main Array of tiles for the game board. It is a 1D array representing a 6x5 grid. 
  const [tiles, setTiles] = useState(
    Array(30).fill("$200", 0, 6)
      .fill("$400", 6, 12)
      .fill("$600", 12, 18)
      .fill("$800", 18, 24)
      .fill("$1000", 24, 30)
  );

  const handleStartGame = () => setCurrentScreen('board');
  const handleSelectQuestion = () => setCurrentScreen('question');
  const handleReturnToBoard = () => setCurrentScreen('board'); 
  const handleSubmitAnswer = () => setCurrentScreen('answer');
  //const handleGameEnd = () => setCurrentScreen('finish');

  return (
    <div className="App">
      {currentScreen === 'title' && (
        <TitleScreen onStart={handleStartGame} />
      )}
      {currentScreen === 'board' && (
        <GameBoard onSelectQuestion={handleSelectQuestion} tiles={tiles} setTiles = {setTiles}/>
      )}
      {currentScreen === 'question' && (
        <QuestionScreen onBack={handleSubmitAnswer} />
      )}
      {currentScreen === 'answer' && (
        <AnswerScreen onReturn={handleReturnToBoard} />
      )}
    </div>
  );
}

//This component presents the Title Screen consisting of 
function TitleScreen({ onStart }) {
  fetch('http://localhost:5000/initialize_game',{
    method: 'GET', 
    headers: {
      'Content-type': 'application/json'
    }
  })
  .then(response => console.log('backend response:', response.json()))
    return (
        <div className="title-screen">
            <img
                src="/notJeopardy-Logo.png"
                alt="!Jeopardy Logo"
            />
            <button onClick={onStart} className="button-design" >
                Start Game
            </button>
        </div>
    );
}

function GameBoard({ onSelectQuestion, tiles, setTiles }) {

  function handleTileClick(index) {
    // Logic to handle tile click, e.g., mark as answered
    if (tiles[index] === null) return; // Already answered
    const newTiles = tiles.slice();
    newTiles[index] = null; // Mark as answered
    console.log(`Tile ${index} clicked`);
    console.log(newTiles);
    setTiles(newTiles);
    onSelectQuestion();
  }

  return (
    <>
    <div className = "board-row"> 
    <Category value={"Category 1"}/>
    <Category value={"Category 2"}/>
    <Category value={"Category 3"}/>
    <Category value={"Category 4"}/>
    <Category value={"Category 5"}/>
    <Category value={"Category 6"}/>
    </div>

    <div className = "board-row">
    <Money value={tiles[0]} onMoneyClick={() => handleTileClick(0)}/>
    <Money value={tiles[1]} onMoneyClick={() => handleTileClick(1)}/>
    <Money value={tiles[2]} onMoneyClick={() => handleTileClick(2)}/>
    <Money value={tiles[3]} onMoneyClick={() => handleTileClick(3)}/>
    <Money value={tiles[4]} onMoneyClick={() => handleTileClick(4)}/>
    <Money value={tiles[5]} onMoneyClick={() => handleTileClick(5)}/>  
    </div>

    <div className = "board-row">
    <Money value={tiles[6]} onMoneyClick={() => handleTileClick(6)}/>
    <Money value={tiles[7]} onMoneyClick={() => handleTileClick(7)}/>
    <Money value={tiles[8]} onMoneyClick={() => handleTileClick(8)}/>
    <Money value={tiles[9]} onMoneyClick={() => handleTileClick(9)}/>
    <Money value={tiles[10]} onMoneyClick={() => handleTileClick(10)}/>
    <Money value={tiles[11]} onMoneyClick={() => handleTileClick(11)}/>  
    </div>

    <div className = "board-row">
    <Money value={tiles[12]} onMoneyClick={() => handleTileClick(12)}/>
    <Money value={tiles[13]} onMoneyClick={() => handleTileClick(13)}/>
    <Money value={tiles[14]} onMoneyClick={() => handleTileClick(14)}/>
    <Money value={tiles[15]} onMoneyClick={() => handleTileClick(15)}/>
    <Money value={tiles[16]} onMoneyClick={() => handleTileClick(16)}/>
    <Money value={tiles[17]} onMoneyClick={() => handleTileClick(17)}/>  
    </div>

    <div className = "board-row">
    <Money value={tiles[18]} onMoneyClick={() => handleTileClick(18)}/>
    <Money value={tiles[19]} onMoneyClick={() => handleTileClick(19)}/>
    <Money value={tiles[20]} onMoneyClick={() => handleTileClick(20)}/>
    <Money value={tiles[21]} onMoneyClick={() => handleTileClick(21)}/>
    <Money value={tiles[22]} onMoneyClick={() => handleTileClick(22)}/>
    <Money value={tiles[23]} onMoneyClick={() => handleTileClick(23)}/>  
    </div>

    <div className = "board-row">
    <Money value={tiles[24]} onMoneyClick={() => handleTileClick(24)}/>
    <Money value={tiles[25]} onMoneyClick={() => handleTileClick(25)}/>
    <Money value={tiles[26]} onMoneyClick={() => handleTileClick(26)}/>
    <Money value={tiles[27]} onMoneyClick={() => handleTileClick(27)}/>
    <Money value={tiles[28]} onMoneyClick={() => handleTileClick(28)}/>
    <Money value={tiles[29]} onMoneyClick={() => handleTileClick(29)}/>  
    </div>

    </>
  );
}

function QuestionScreen({ onBack }) {
  const [answer, setAnswer] = useState(''); // store the player's input

  const handleChange = (e) => {
    setAnswer(e.target.value); // update state whenever the user types
  };

  const handleSubmit = () => {
    console.log('User answer:', answer);
    onBack();
  };

  return (
    <div>
      <h3>Question: What is React?</h3>
      <input
        type="text"
        placeholder="Your answer"
        value={answer}
        onChange={handleChange}
      />
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}

function AnswerScreen({ onReturn }) {
    return (
      <div>
      <h1>My Answer</h1>

        <button onClick={onReturn} className="button-design" >
            Return to Game
        </button>
        <p>$500</p>
      </div>
    );
}

//function GameOver({})

function Category ( {value} ) {
  return <div className="cat-tile">{value}</div>;
}

function Money ( {value, onMoneyClick} ) {
  return <button className="money-tile" onClick={onMoneyClick}>{value}</button>;
}

