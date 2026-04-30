import Navbar from "../components/Navbar"
import arrowIcon from "../assets/arrow.svg"
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
      {/* {currPara.length !== 0 && <div className={style.contentWrapper}> */}
      {/*   <div className={style.content}> */}
      {/*     {currPara.map((w, i) => ( */}
      {/*       <span */}
      {/*         className={hoveredWord === i ? style.hovered : ''} */}
      {/*         onMouseEnter={() => { handleOnMouseEnter(w, i) }} */}
      {/*         onMouseLeave={handleOnMouseLeave} */}
      {/*       >{`${w} `} */}
      {/*       </span> */}
      {/*     ))} */}
      {/*   </div> */}
      {/* </div>} */}
      {/* {currPara.length !== 0 ? <div className={style.contentWrapper}> */}
      {/*   <div className={style.details}> */}
      {/*     <h3 className="font-bold text-2xl p-1">{details.text}</h3> */}
      {/*     <div> */}
      {/*       {FIELDS.map(({ label, key }) => { */}
      {/*         const val = get(details, key); */}
      {/*         return ( */}
      {/*           <> */}
      {/*             <span key={`${key}-label`} className={style.label}>{label}:</span> */}
      {/*             <span key={`${key}-value`} className={style.value}>{val || "-"}</span> */}
      {/*           </> */}
      {/*         ); */}
      {/*       })} */}
      {/*     </div> */}
      {/*   </div> */}
      {/* </div> : <div className="h-[90%] w-full"> */}
      {/*   <div className="text-3xl items-center justify-center flex text-left font-sans h-full"> */}
      {/*     <ul className={`${style.instructions} gap-5 flex flex-col`}> */}
      {/*       <li className={style.instruction}>Select a Paragraph</li> */}
      {/*       <li className="flex justify-center rotate-180"><img src={arrowIcon} alt="icon" className="h-10 w-10" /></li> */}
      {/*       <li className={style.instruction}>Read</li> */}
      {/*       <li className="flex justify-center rotate-180"><img src={arrowIcon} alt="icon" className="h-10 w-10" /></li> */}
      {/*       <li className={style.instruction}>Hover to learn about unfamiliar words</li> */}
      {/*       <li className="flex justify-center rotate-180"><img src={arrowIcon} alt="icon" className="h-10 w-10" /></li> */}
      {/*       <li className={style.instruction}>Click to add to weak words</li> */}
      {/*     </ul> */}
      {/*   </div> */}
      {/* </div>} */}
    </div>
  </>
}
