import Navbar from "../components/Navbar"
import arrowIcon from "../assets/arrow.svg"
import { useState, useEffect, useRef } from 'react'
import style from "./Paragraph.module.css"
import { api } from "../api/axios.js"


export default function Paragraph() {
  const [showToast, setShowToast] = useState(false)

  useEffect(() => {
    // show a small apology/toast when the paragraph page mounts
    setShowToast(true)
    const t = setTimeout(() => setShowToast(false), 6000)
    return () => clearTimeout(t)
  }, [])

  const FIELDS = [
    { label: 'Definition', key: 'definition' },
    { label: 'Part Of Speech', key: 'part_of_speech' },
    { label: 'Synonyms', key: 'synonyms' },
    { label: 'Antonyms', key: 'antonyms' },
    { label: 'Usage', key: 'usage' },
    { label: 'Examples', key: 'examples' },
    { label: 'Register', key: 'register' },
    { label: 'Connotation', key: 'connotation' },
    { label: 'Collocations', key: 'collocations' },
    { label: 'Plural', key: 'word_forms.plural' },
    { label: 'Past', key: 'word_forms.past' },
    { label: 'Comparative', key: 'word_forms.comparative' },
    { label: 'Derivatives', key: 'derivatives' },
    { label: 'Etymology', key: 'etymology' },
    { label: 'Notes', key: 'notes' },
  ];
  const [paragraphs, setParagraphs] = useState([]);
  const [currPara, setCurrPara] = useState([]);
  const [hoveredWord, setHoveredWord] = useState(null)
  const [details, setDetails] = useState({
    text: "",
    part_of_speech: "",
    definition: "",

    synonyms: [],
    antonyms: [],

    usage: "",
    examples: [],

    register: "",        // formal, informal, slang
    connotation: "",     // positive, negative, neutral

    collocations: [],

    word_forms: {
      plural: "",
      past: "",
      comparative: "",
    },

    derivatives: [],

    etymology: "",
    notes: "",
  });
  const hoverTimeout = useRef(null)
  const hoveredTimeout2 = useRef(null)

  useEffect(() => {
    api.get('/paragraph/').then((res) => {
      setParagraphs(res.data);
      console.log(res.data);
    })
  }, [])

  const handleOnMouseEnter = (w, i) => {
    const word = w.replace(/[^a-zA-Z]/g, '').toLowerCase()
    hoverTimeout.current = setTimeout(() => {
      setHoveredWord(i);
      api.get(`/words/by-slug/${word}/`).then((res) => {
        console.log(res.data);
        if (Array.isArray(res.data)) {
          setDetails(res.data[0])
        } else {
          setDetails(res.data);

        }
      })
    }, 500);
    hoveredTimeout2.current = setTimeout(() => {
      api.post("/user-words/", { word, status: "weak" })
    }, 1000)
  }

  const handleOnMouseLeave = () => {
    clearTimeout(hoverTimeout.current);
    clearTimeout(hoveredTimeout2.current);
    setHoveredWord(null);
  }

  const get = (obj, path) => {
    const res = path.split('.').reduce((o, k) => o?.[k], obj);
    if (Array.isArray(res)) {
      return res.join(", ");
    }
    return res;
  };
  return <> <Navbar />
    <div className={`${style.page} font-sans`}>
      {showToast && (
        <div className="fixed bottom-4 right-4 bg-gray-800 text-white px-4 py-2 rounded shadow" role="status">
          Sorry — our servers are a bit slow right now. We're working on it.
        </div>
      )}
      <div className={style.sidebar}>
        {paragraphs.map((p) => (
          <div className={style.sidebarButton} key={p.id} onClick={() => { setCurrPara(p.word_list) }}>{p.title}</div>
        ))}
      </div>
      {currPara.length !== 0 && <div className={style.contentWrapper}>
        <div className={style.content}>
            {currPara.map((w, i) => (
              <span
                className={hoveredWord === i ? style.hovered : ''}
                onMouseEnter={() => { handleOnMouseEnter(w, i) }}
                onMouseLeave={handleOnMouseLeave}
              >{`${w} `}
              </span>
            ))}
          </div>
      </div>}
      {currPara.length !== 0 ? <div className={style.contentWrapper}>
        <div className={style.details}>
           <h3 className="font-bold text-2xl p-1">{details.text}</h3>
           <div>
             {FIELDS.map(({ label, key }) => {
               const val = get(details, key);
               console.log(val, key);
               return (
                 <>
                   <span key={`${key}-label`} className={style.label}>{label}:</span>
                   <span key={`${key}-value`} className={style.value}>{val || "-"}</span>
                 </>
               );
             })}
           </div>
          </div>
         </div> : <div className="h-[90%] w-full">
          <div className="text-3xl items-center justify-center flex text-left font-sans h-full">
            <ul className={`${style.instructions} gap-5 flex flex-col`}>
              <li className={style.instruction}>Select a Paragraph</li>
              <li className="flex justify-center rotate-180"><img src={arrowIcon} alt="icon" className="h-10 w-10"/></li>
              <li className={style.instruction}>Read</li>
              <li className="flex justify-center rotate-180"><img src={arrowIcon} alt="icon" className="h-10 w-10"/></li>
              <li className={style.instruction}>Hover to learn about unfamiliar words</li>
              <li className="flex justify-center rotate-180"><img src={arrowIcon} alt="icon" className="h-10 w-10"/></li>
              <li className={style.instruction}>Click to add to weak words</li>
            </ul>
          </div>
        </div>}

    </div>
    </>
}
