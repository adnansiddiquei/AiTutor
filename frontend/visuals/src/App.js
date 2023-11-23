import './App.css';
import ScatterPlot from "./components/ScatterPlot.js";
import {useEffect, useState} from "react";
import Dropdown from  './components/Dropdown.js'

function App() {
  // const data = [
  //   { x: 1, y: 2, category: 'A', zScore: 1 },
  //   { x: 3, y: 4, category: 'B', zScore: 0.4 },
  //   { x: 2, y: 3.7, category: 'B', zScore: 0.1 },
  //   { x: 2, y: 3.6, category: 'C', zScore: 0.6 },
  //   // ... more data points
  // ];
  
  const [data, setData] = useState(null)
  const [lesssonId, setLessonId] = useState(0)
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8080/visualise?lessonId=${lesssonId}`);
        if (!response.ok) {
          throw new Error(`Error: ${response.status}`);
        }
        const result = await response.json();
        setData(result)
      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };
    
    fetchData()
  }, [])
  
  return (
    <div className="App">
      <div>
        {data && <ScatterPlot data={data} />}
        <Dropdown lessonId={lesssonId} setLessonId={setLessonId}></Dropdown>
      </div>
    </div>
  );
}

export default App;
