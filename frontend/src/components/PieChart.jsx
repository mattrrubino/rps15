import React from "react";
import { VictoryPie } from "victory-pie";

// Takes one prop, data, which is a dictionary of the moves and how many times they've been used
function App (props) {

  function populateData (data) {
    let Data = [];

    for (const key in data){
      Data.push({ x: key, y: data[key]})
    }
    
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