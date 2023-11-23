import './App.css';
import ScatterPlot from "./components/ScatterPlot.js";
import {useState} from "react";

function App() {
  // const data = [
  //   { x: 1, y: 2, category: 'A', zScore: 1 },
  //   { x: 3, y: 4, category: 'B', zScore: 0.4 },
  //   { x: 2, y: 3.7, category: 'B', zScore: 0.1 },
  //   { x: 2, y: 3.6, category: 'C', zScore: 0.6 },
  //   // ... more data points
  // ];
  
  const [data, setData] = useState(null)
  
  const fetchData = async () => {
    try {
      const response = await fetch('https://localhost:8080/visualise');
      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      const result = await response.json();
      setData(result);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    }
  };
  
  return (
    <div className="App">
      <ScatterPlot data={data} />
    </div>
  );
}

export default App;
