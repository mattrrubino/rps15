import React from "react";
import { VictoryPie } from "victory-pie";


function App (props) {
// const App = (props) => {
    const myData = [
        { x: props.test, y: 900 },
        { x: "Group B", y: 400 },
        { x: "Group C", y: 300 },
    ];

    let Data = [];

    function populateData (data) {
        for (const key in data){
            Data.concat(
                { x: key, y: data[key]}
            )
        }
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
        data={myData}
        style={style}
        colorScale="qualitative"
        radius={100}
      />
    </div>
  );
};

export default App;