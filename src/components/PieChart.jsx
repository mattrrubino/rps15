import React from "react";
import { VictoryPie } from "victory-pie";

// Takes one prop, data, which is a dictionary of the moves and how many times they've been used
function App (props) {

  function populateData (data) {
    let Data = [];

    let sum = 0;
    for (const key in data) {
      sum += data[key]
    }

    // Populate with all 1s so it renders on fresh user
    if (sum === 0) {
      for (const key in data) {
        Data.push({ x: key, y: 1})
      }
    } else {
      for (const key in data) {
        if (data[key] != 0) {
          Data.push({ x: key, y: data[key]})
        }
      }
    }
    
    Data.sort((a,b) => a.y - b.y)
    return Data;
  }
    
  const style = {
    data: {
      fillOpacity: 0.9, stroke: "#45A29E", strokeWidth: 2
    },
    labels: {
      fontSize: 15, fill: "#66FCF1"
    }
  }

  return (
    <div>
      <VictoryPie
        data={populateData(props.data)}
        style={style}
        colorScale="qualitative"
        radius={100}
      />
    </div>
  );
};

export default App;