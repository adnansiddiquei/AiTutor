import './App.css';
import Flashcard from './components/Flashcard.js';
import {useEffect, useState} from "react";
import flashcard from "./components/Flashcard.js";

function App() {
  const [lesson, setLesson] = useState(0)
  const [lessonSummary, setLessonSummary] = useState(null)
  const [flashcards, setFlashcards] = useState(null)
  const [answers, setAnswers] = useState([])
  
  useEffect(() => {
    const fetchAllQuestions = async (lessonId) => {
      try {
        let promises = [];
        let f = [];
        
        f.push(await (await fetch(`http://127.0.0.1:8080/question?lessonId=${lessonId}&questionNumber=0`)).json())
        f.push(await (await fetch(`http://127.0.0.1:8080/question?lessonId=${lessonId}&questionNumber=1`)).json())
        f.push(await (await fetch(`http://127.0.0.1:8080/question?lessonId=${lessonId}&questionNumber=2`)).json())
        f.push(await (await fetch(`http://127.0.0.1:8080/question?lessonId=${lessonId}&questionNumber=3`)).json())
        f.push(await (await fetch(`http://127.0.0.1:8080/question?lessonId=${lessonId}&questionNumber=4`)).json())
        f.push(await (await fetch(`http://127.0.0.1:8080/question?lessonId=${lessonId}&questionNumber=5`)).json())
        f.push(await (await fetch(`http://127.0.0.1:8080/question?lessonId=${lessonId}&questionNumber=6`)).json())
        f.push(await (await fetch(`http://127.0.0.1:8080/question?lessonId=${lessonId}&questionNumber=7`)).json())
        f.push(await (await fetch(`http://127.0.0.1:8080/question?lessonId=${lessonId}&questionNumber=8`)).json())
        f.push(await (await fetch(`http://127.0.0.1:8080/question?lessonId=${lessonId}&questionNumber=9`)).json())
        
        return f
      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };
    
    if (lesson === 0) {
      fetchAllQuestions(lesson).then(f => {setFlashcards(f)})
    }
  }, [lesson])
  
  useEffect(() => {
    console.log(answers)
  }, [answers])
  
  const whatToRender = () => {
    if (lesson === 0 && flashcards) {
      return <Flashcard lessonSummary={lessonSummary} flashcards={flashcards} setLesson={setLesson} setAnswers={setAnswers} lesson={lesson} answers={answers}></Flashcard>
    } else if (flashcards && lessonSummary) {
      return <Flashcard lessonSummary={lessonSummary} flashcards={flashcards} setLesson={setLesson} setAnswers={setAnswers} lesson={lesson} answers={answers}></Flashcard>
    } else {
      return <div></div>
    }
  }
  
  return (
    <div className="App">
      { whatToRender() }
    </div>
  );
}

export default App;
