import { useState } from 'react';

export default function App() {
  const [currentScreen, setCurrentScreen] = useState('title');
  const [tiles, setTiles] = useState(Array(6).fill("$200"));

  const handleStartGame = () => setCurrentScreen('board');
  const handleSelectQuestion = () => setCurrentScreen('question');
  const handleReturnToBoard = () => setCurrentScreen('board');

  return (
    <div className="App">
      {currentScreen === 'title' && (
        <TitleScreen onStart={handleStartGame} />
      )}
      {currentScreen === 'board' && (
        <GameBoard onSelectQuestion={handleSelectQuestion} tiles={tiles} setTiles = {setTiles}/>
      )}
      {currentScreen === 'question' && (
        <QuestionScreen onBack={handleReturnToBoard} />
      )}
    </div>
  );
}

// Example components

function TitleScreen({ onStart }) {
  return (
    <div>
      <h1>!Jeopardy</h1>
      <button onClick={onStart}>Start Game</button>
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
    </>
  );
}

function QuestionScreen({ onBack }) {
  return (
    <div>
      <h3>Question: What is React?</h3>
      <input type="text" placeholder="Your answer" />
      <button onClick={onBack}>Back</button>
    </div>
  );
}

function Category ( {value} ) {
  return <div className="cat-tile">{value}</div>;
}

function Money ( {value, onMoneyClick} ) {
  return <button className="money-tile" onClick={onMoneyClick}>{value}</button>;
}

/*
function Money ( {value} ) {
  function handleClick() {

  }
  return <button className="money-tile">{value}</button>;
}

function Category ( {value} ) {
  return <button className="cat-tile">{value}</button>;
}

export default function Tilescreen() {
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
    <Money value={"$200"}/>
    <Money value={"$200"}/>
    <Money value={"$200"}/>
    <Money value={"$200"}/>
    <Money value={"$200"}/>
    <Money value={"$200"}/>  
    </div>

    <div className = "board-row">
    <Money value={"$400"}/>
    <Money value={"$400"}/>
    <Money value={"$400"}/>
    <Money value={"$400"}/>
    <Money value={"$400"}/>
    <Money value={"$400"}/>  
    </div>

    <div className = "board-row">
    <Money value={"$600"}/>
    <Money value={"$600"}/>
    <Money value={"$600"}/>
    <Money value={"$600"}/>
    <Money value={"$600"}/>
    <Money value={"$600"}/>  
    </div>

    <div className = "board-row">
    <Money value={"$800"}/>
    <Money value={"$800"}/>
    <Money value={"$800"}/>
    <Money value={"$800"}/>
    <Money value={"$800"}/>
    <Money value={"$800"}/>  
    </div>

    <div className = "board-row">
    <Money value={"$1000"}/>
    <Money value={"$1000"}/>
    <Money value={"$1000"}/>
    <Money value={"$1000"}/>
    <Money value={"$1000"}/>
    <Money value={"$1000"}/>  
    </div>

    </>
  )
}
*/

/*

function Square({value, onSquareClick}) {
  return (
    <button className="square" onClick={onSquareClick}>
      {value}
    </button>
  );
}

export default function Board() {
  const [xIsNext, setXIsNext] = useState(true);
  const [squares, setSquares] = useState(Array(9).fill(null));

  function handleClick(i) {
    if (calculateWinner(squares) || squares[i]) {
      return;
    }
    const nextSquares = squares.slice();
    if (xIsNext) {
      nextSquares[i] = 'X';
    } else {
      nextSquares[i] = 'O';
    }
    setSquares(nextSquares);
    setXIsNext(!xIsNext);
  }

  const winner = calculateWinner(squares);
  let status;
  if (winner) {
    status = 'Winner: ' + winner;
  } else {
    status = 'Next player: ' + (xIsNext ? 'X' : 'O');
  }

  return (
    <>
      <div className="status">{status}</div>
      <div className="board-row">
        <Square value={squares[0]} onSquareClick={() => handleClick(0)} />
        <Square value={squares[1]} onSquareClick={() => handleClick(1)} />
        <Square value={squares[2]} onSquareClick={() => handleClick(2)} />
      </div>
      <div className="board-row">
        <Square value={squares[3]} onSquareClick={() => handleClick(3)} />
        <Square value={squares[4]} onSquareClick={() => handleClick(4)} />
        <Square value={squares[5]} onSquareClick={() => handleClick(5)} />
      </div>
      <div className="board-row">
        <Square value={squares[6]} onSquareClick={() => handleClick(6)} />
        <Square value={squares[7]} onSquareClick={() => handleClick(7)} />
        <Square value={squares[8]} onSquareClick={() => handleClick(8)} />
      </div>
    </>
  );
}

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}
*/
