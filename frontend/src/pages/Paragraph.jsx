import Navbar from "../components/Navbar"
import Footer from "../components/Footer.jsx"
import { useState, useEffect, useRef } from 'react'
import style from "./Paragraph.module.css"
import api from "../api/axios.js"

export default function Paragraph() {

  const [paragraphs, setParagraphs] = useState([]);
  const [currPara, setCurrPara] = useState([]);
  const [hoveredWord, setHoveredWord] = useState(null)
  const [details, setDetails] = useState(" Hover Over a Word To See Its Details")
  const hoverTimeout = useRef(null)

  useEffect(() => {
    api.get('/paragraph/').then((res) => {
      setParagraphs(res.data);
      console.log(res.data);
    })
  }, [])
  
  const handleOnMouseEnter = (w, i) => {
    hoverTimeout.current = setTimeout(() => {
        setHoveredWord(i);
        const word = w.replace(/[^a-zA-Z]/g, '').toLowerCase()
        api.get(`/words/${word}`).then((res) => {
          setDetails(res.data.definition);
        })
      }, 500)
  }
  
  const handleOnMouseLeave = () => {
    clearTimeout(hoverTimeout.current);
    setHoveredWord(null);
  }

  return <> <Navbar />
    <div className={style.page}>
      <div className={style.sidebar}>
        {paragraphs.map((p) => (
          <div className={style.sidebarButton} key={p.id} onClick={() => {setCurrPara(p.word_list)}}>{p.title}</div>
        ))}
      </div>
      <div className={style.contentWrapper}>
        <div className={style.details}>
          {details}
        </div>
        <div className={style.content}>
        {currPara.map((w, i) => (
          <span
            className={hoveredWord === i ? style.hovered : ''}
            onMouseEnter={() => {handleOnMouseEnter(w, i)}}
            onMouseLeave={handleOnMouseLeave}
          >{`${w} `}
            </span>
          ))}
        </div>
      </div>
    </div>
    <Footer /></>
}
