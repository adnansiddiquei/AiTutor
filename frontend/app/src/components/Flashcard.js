import React, { useState } from 'react';
import './Flashcard.css'; // Make sure to create a corresponding CSS file

function Flashcard({ lessonSummary, flashcards, lesson, setLesson, setAnswers, answers }) {
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null)
  const [lessonFinished, setLessonFinished] = useState(false)
  const [showingLessonSummary, setShowingLessonSummary] = useState(lessonSummary?.lessonId > 0)
  const currentCard = flashcards[currentCardIndex];
  
  const handleNextCard = () => {
    if (selectedAnswer !== null) {
      setAnswers(prevAnswers => prevAnswers.concat([{
        id: currentCard.id,
        answer: currentCard.answers.indexOf(selectedAnswer),
        responseTime: 5,
        lessonId: lesson
      }]))
      
      if (!currentCard.lessonFinished) {
        setCurrentCardIndex((prevIndex) => prevIndex + 1);
        setSelectedAnswer(null)
      } else { // i.e., they've just answered the last question
        setLessonFinished(true)
  
        fetch('http://127.0.0.1:8080/question', {
          method: 'POST', // Specify the method
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(answers),
        })
          .then(response => response.json()) // Parse the response as JSON
          .then(data => {
            console.log('Success:', data); // Handle the response data
          })
          .catch((error) => {
            console.error('Error:', error); // Handle the error
          });
      }
    } else {
      alert('Please select an answer before submitting.');
    }
  };
  
  const handleAnswerClick = (answer) => {
    setSelectedAnswer((prevAnswer) => prevAnswer === answer ? null : answer)
  }
  
  const handleExplain = () => {
    // Logic to explain the answer
  };
  
  const handleNextLesson = () => {
    setLesson(prevLesson => prevLesson + 1)
  };
  
  const handleStart = () => setShowingLessonSummary(false)
  
  
  const lessonSummaryDiv =
    <div className="flashcard-container">
      <div className="flashcard">
        <div className="question">Lesson Summary</div>
        <div>{lessonSummary?.summary}</div>
        <div className="buttons">
          <button onClick={handleStart}>Let's get started</button>
        </div>
      </div>
    </div>
  
  const flashcardsDiv =
    <div className="flashcard-container">
      <div className="flashcard">
        <div>{
          !lessonFinished ?
            <div>
              <div className="question">{currentCard.question}</div>
              <ul className="answers">
                {currentCard.answers.map((answer, index) => (
                  <li
                    key={index}
                    className={answer === selectedAnswer ? 'selected' : ''}
                    onClick={() => handleAnswerClick(answer)}
                  >
                    {answer}
                  </li>
                ))}
              </ul>
              <div className="buttons">
                <button onClick={handleExplain}>Explain</button>
                <button onClick={handleNextCard}>Submit</button>
              </div>
            </div> :
            <div>
              <div className="question" style={{marginTop: 100, fontSize: 40}}>Lesson Finished!</div>
              <button onClick={handleNextLesson} style={{marginTop: 50}}>Next Lesson</button>
            </div>
        
        }</div>
      </div>
    </div>
  
  return (
    showingLessonSummary ? lessonSummaryDiv : flashcardsDiv
  );
}

export default Flashcard;