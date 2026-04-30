import style from "./Quiz.module.css"
import { useEffect, useState, useRef } from "react"
import { api } from "../api/axios.js"

export default function Quiz() {
  const [question, setQuestion] = useState(null) 
  const questionRef = useRef()
  const [selected, setSelected] = useState("")
  const [ended, setEnded] = useState(null)
  const [correct, setCorrect] = useState(null)
  const [correctOption, setCorrectOption] = useState('')
  const [loading, setLoading] = useState(false);

  const handleGenrate = () => {
    setEnded(null);
    setLoading(true);
    api.post('/quiz/generate/').then((res) => {
      localStorage.setItem('quiz_id', res.data.quiz_id);
      setQuestion(res.data.question)
      setLoading(false);
    })
  }
  const handleSolveSubmit = () => {
    if (correct !== null) {
      setQuestion(questionRef.current);
      setCorrect(null);
      return
    }
    setLoading(true);
    api.post('/quiz/mcq_solved/', {
      quiz_id: localStorage.getItem("quiz_id"),
      mcq_id: question.id,
      selected: selected
    }).then(res => {
      setLoading(false);
      if (res.data?.ended) {
          setCorrect(res.data.correct)
          setCorrectOption(res.data.correct_option)
          setTimeout(() => {
            setCorrect(null)
            setQuestion(null)
            setSelected('')
            setEnded(true)
          }, 1000)
          return
      }
      console.log(res.data);
      setCorrect(res.data.correct)
      setCorrectOption(res.data.correct_option)
      questionRef.current = res.data.next;
    });
    
    useEffect(() => {
      document.documentElement.classList.toggle("loading", loading);
      return () => document.documentElement.classList.remove("loading");
    }, [loading]);
  }
  return <>
    <div className={style.page}>
      {correct !== null && <div className={`${style.feedback} ${correct ? style.correct : style.incorrect}`}>{correct ? "Correct" : "Incorrect"}</div>}
      {ended && <div>
        <div className={style.feedback}>Quiz Ended</div>
      </div>}
      {!ended && question ? 
        <>
          <h3 className={style.question}>{question.text}</h3>
          <div className={style.options}>
            {question.options.map((op) => (
              <div 
                key={op}
                className={`${style.option} ${selected === op ? style.selected : ''} ${correctOption === op ? style.correct : ''}`}
                onClick={() => setSelected(op)}
              >
                {op}
              </div>
            ))}
          </div>
          <button className={style.button} onClick={handleSolveSubmit} disabled={!selected}>{correct !== null ? "Next" : "Submit"}</button>
        </> :
        <button className={style.button} onClick={handleGenrate}>Generate Quiz</button> 
      }
    </div>
  </>
}
