import React, { useEffect } from 'react';
import PieChart from '../components/PieChartForProfile';
import './Profile.css';
import { useState } from 'react';

export default function Profile() {
  const [playerData, setPlayerData] = useState([]);
  const [eloMessage, setEloMessage] = useState("You're just ok, you still need to get better");


  useEffect(() => {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/api/user");

    console.log(xhr.status)

    if (xhr.status === 200) {
      xhr.responseType = 'json';
      setPlayerData(xhr.response);
    } 
    // else {
    //     alert("Failed to load your data")
    // }
    if (playerData["Elo"] < 500) {
      setEloMessage("You really suck at this game, stop playing");
    }

    xhr.send();

  })

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
  };

  return (
    <div>
      <div className='container'>
        <div className='title'><span>You really suck at this game, stop playing</span></div>
        {/* <div className='title'><span>{eloMessage}</span></div> */}
        <div className='user'>
          <h1>Username: Test</h1>
          {/* <h1>Username: Test{playerData['Username']}</h1> */}
        </div>
      
        <div className='chart'>
          <h1>Your Stats:</h1>
          <span>Wins: 0</span>
          <span> Losses: 457</span>
          <span> Elo: 13</span>
          {/* <span>{playerData['Wins']}</span><span>{playerData['Losses']}</span><span>{playerData['Elo']}</span> */}
          <PieChart data={testdata}/>
          {/* <PieChart data={playerData['MoveCounts']}/> */}
        </div>

      </div>
    </div>
  )
}
