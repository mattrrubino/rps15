import React, { useEffect } from 'react';
import PieChart from '../components/PieChart';
import './Profile.css';
import { useState } from 'react';

export default function Profile() {
  const [loading, setLoading] = useState(true);
  const [playerData, setPlayerData] = useState(null);
  const [eloMessage, setEloMessage] = useState("");

  useEffect(() => {
    var xhr = new XMLHttpRequest();
    xhr.responseType = 'json';
    xhr.open("GET", "/api/user");

    xhr.onreadystatechange = (e) => {
      if (xhr.readyState != XMLHttpRequest.DONE) {
          return;
      }

      setLoading(false);
      if (xhr.status !== 200) {
        return;
      }

      setPlayerData(xhr.response);
      if (xhr.response["Elo"] >= 500) {
        setEloMessage("You're just ok, you still need to get better");
      } else {
        setEloMessage("You really suck at this game, stop playing");
      }
    }

    xhr.send();
  }, [])

  return (
    <div>
      <div className='container'>
        {loading ? (
          <div className='title'><span>Loading...</span></div>
        ) : (
          playerData ? (
            <div>
              <div className='title'><span>{eloMessage}</span></div>
              <div className='user'>
                <h1>Username: {playerData['Username']}</h1>
              </div>
            
              <div className='chart'>
                <h1>Your Stats:</h1>
                <p>Wins: {playerData['Wins']}</p>
                <p>Losses: {playerData['Losses']}</p>
                <p>Elo: {playerData['Elo']}</p>
                <PieChart data={playerData['MoveCounts']}/>
              </div>
            </div>
          ) : (
            <div className='title'><span>No profile found.</span></div>
          )
        )
        }
      </div>
    </div>
  )
}
