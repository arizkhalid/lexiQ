import { useState, useEffect, useRef } from 'react'
import style from "./Paragraph.module.css"
import { api } from "../api/axios.js"
import { useNavigate } from 'react-router-dom'

export default function Paragraph() {
  const [showToast, setShowToast] = useState(false)
  const navigate = useNavigate();

  const [paragraphs, setParagraphs] = useState([]);

  useEffect(() => {
    setShowToast(true)
    const t = setTimeout(() => setShowToast(false), 6000)
    return () => clearTimeout(t)
  }, [])

  useEffect(() => {
    api.get('/paragraph/').then((res) => {
      setParagraphs(res.data);
      console.log(res.data);
    })
  }, [])

  return <>
    <div className={`${style.page} font-sans`}>
      {showToast && (
        <div className="fixed bottom-4 right-4 bg-gray-800 text-white px-4 py-2 rounded shadow" role="status">
          Sorry — our servers are a bit slow right now. We're working on it.
        </div>
      )}
      <h1>Select a Paragraph!</h1>
      <div className={style.cardContainer}>
        {paragraphs.map((p) => (
          <div className={style.paraCard} key={p.id} onClick={() => { navigate(`read/?para_id=${p.id}`) }}>
            <div className="text-xl border-b-2">{p.title}</div>
            <div className="text-sm pt-4">
              <div><strong>Difficulty:</strong><br />{p.difficulty}<br />•</div>
              <div><strong>Source:</strong><br />{p.source}<br />•</div>
              <div><strong>Words:</strong><br />{p.word_length}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  </>
}
