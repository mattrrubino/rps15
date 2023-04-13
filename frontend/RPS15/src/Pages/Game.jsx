import React from 'react'
import './Game.css'
import { useState } from 'react'
import Select from 'react-select';
import PieChart from '../components/PieChart'

const Game = () => {
  const [round, setRound] = useState(1);
  const [player, setPlayer] = useState("Player");
  const [opponent, setOpponent] = useState("Opponent");
  const [playerScore, setPlayerScore] = useState(0);
  const [opponentScore, setOpponentScore] = useState(0);


  const [selectedOption, setSelectedOption] = useState("Select your sign");

  let message = "Game Message";

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
          {message}
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
              <PieChart test="foo"/>
            </div>
          </div>
        </div>
        <div className='chat-container page-item'>
          Chat
        </div>
      </div>
    </div>
  )
}

export default Game