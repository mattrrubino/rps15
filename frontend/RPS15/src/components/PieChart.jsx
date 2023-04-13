import React from "react";
import { VictoryPie } from "victory-pie";

const myData = [
  { x: "Group A", y: 900 },
  { x: "Group B", y: 400 },
  { x: "Group C", y: 300 },
];

const style = {
    data: {
      fillOpacity: 0.9, stroke: "#45A29E", strokeWidth: 2
    },
    labels: {
      fontSize: 15, fill: "#66FCF1"
    }
  }

const App = () => {
  return (
    <div>
      <VictoryPie
        data={myData}
        style={style}
        colorScale="qualitative"
        radius={100}
      />
    </div>
  );
};

export default App;