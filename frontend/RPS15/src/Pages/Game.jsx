import React from 'react'
import './Game.css'
import { useState } from 'react'
import Select from 'react-select';
import PieChart from '../components/PieChart'

const Game = () => {
  const [round, setRound] = useState(1);
  const [player, setPlayer] = useState("Player");
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState("So Empty");
  const [playerScore, setPlayerScore] = useState(0);
  const [opponent, setOpponent] = useState("Opponent");
  const [opponentScore, setOpponentScore] = useState(0);
  const [gameMessage, setGameMessage] = useState("Game Message");
  const [selectedOption, setSelectedOption] = useState("Select your sign"); // for dropdown selection

  // Create websocket connection
  function componentDidMount() {
    const ws = new WebSocket('ws://localhost:8000/ws')
    // Callback when a message is received
    ws.onmessage = this.onMessage
    
    this.setState({
      ws: ws,
      // Create an interval to send echo messages to the server
      interval: setInterval(() => ws.send('echo'), 1000)
    })
  }

  // For submitting chats
  const onSubmit = (e) => {
    e.preventDefault();
  
    console.log("Message Sent: " + message);
    setMessage('');
  }

  // test data for the pie chart
  let testdata = {
    "rock": 3,
    "scissors": 5,
    "gun": 2,
    "banana": 8,
    "paper": 1,
    "1": 4,
    "2": 15,
    "3": 3,
    "zac": 60,
    "5": 9,
    "6": 3,
    "7": 2,
    "8": 1,
    "9": 11,
    "0": 20,
  }

  const options = [
    {value: "Rock", label: "Rock"},
    {value: "Fire", label: "Fire"},
    {value: "Scissors", label: "Scissors"},
    {value: "Snake", label: "Snake"},
    {value: "Human", label: "Human"},
    {value: "Tree", label: "Tree"},
    {value: "Wolf", label: "Wolf"},
    {value: "Sponge", label: "Sponge"},
    {value: "Paper", label: "Paper"},
    {value: "Air", label: "Air"},
    {value: "Water", label: "Water"},
    {value: "Dragon", label: "Dragon"},
    {value: "Devil", label: "Devil"},
    {value: "Lightning", label: "Lightning"},
    {value: "Gun", label: "Gun"}
  ];

  const selectStyles = {
    control: (base, state) => ({
      ...base,
      background: "#1e1e1e",
      width: "125px",
      borderRadius: state.isFocused ? "3px 3px 0 0" : 3,
      boxShadow: state.isFocused ? null : null,
      "&:hover": {
      }
    }),
    singleValue: (provided, state) => ({
      ...provided,
      color: 'inherit',
      background: "#1e1e1e",
    }),
    menu: (provided, state) => ({
      ...provided,
      'z-index': 9,
      background: "#1e1e1e",
    }),
    multiValue: (provided, state) => ({
      ...provided,
      color: state.isDisabled ? "#000" : "#fff",
      background: "#1e1e1e",
    }),
  };

  return (
    <div className='game-page'>
      <div className='page-container'>
        <div className='round-tracker page-item'>
          Round {round}
        </div>
        <div className='game-message page-item'>
          {gameMessage}
        </div>
        <div className='game-container page-item'>
          <div className='player-side game-item'>
          <div className='opponent-score'>
              {player}: {playerScore}
            </div>
            <Select 
              styles={selectStyles}
              className='select-sign'
              value={selectedOption}
              onChange={setSelectedOption}
              options={options}  
            />
          </div>
          <div className='opponent-side game-item'>
            <div className='opponent-score'>
              {opponent}: {opponentScore}
            </div>
            <div className='chart'>
              <PieChart data={testdata}/>
            </div>
          </div>
        </div>
        <div className='chat-container page-item'>
          <div className='chat-display'>
            {messages}
          </div>
          <form className='chat-input' onSubmit={onSubmit}>
            <label htmlFor='message'></label>
            <input 
              type="text"
              id='message'
              name='message'
              className='message-input'
              value={message}
              placeholder='Message: (Enter to submit)'
              onChange={(e) => setMessage(e.target.value)}
            />
          </form>
        </div>
      </div>
    </div>
  )
}

export default Game