import { useEffect, useState, useRef } from "react";
import { api } from "../api/axios.js"
import { useSearchParams } from "react-router-dom";
import style from "./Read.module.css"

export default function Read() {
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
  const [currPara, setCurrPara] = useState([]);
  const [searchParams] = useSearchParams();
  const para_id = searchParams.get("para_id");   // ?name=John
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

  const get = (obj, path) => {
    const res = path.split('.').reduce((o, k) => o?.[k], obj);
    if (Array.isArray(res)) {
      return res.join(", ");
    }
    return res;
  };

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

  useEffect(() => {
    api.get(`/paragraph/${para_id}`).then((res) => {
      setCurrPara(res.data.word_list)
      console.log(res.data);
    })
  }, [])

  return <div> 
    <div className={style.contentWrapper}>
        <div className={style.content}>
          {currPara && currPara.map((w, i) => (
            <span
              className={hoveredWord === i ? style.hovered : ''}
              onMouseEnter={() => { handleOnMouseEnter(w, i) }}
              onMouseLeave={handleOnMouseLeave}
            >{`${w} `}
            </span>
          ))}
        </div>
      </div>
      {currPara && currPara.length !== 0 ? <div className={style.contentWrapper}>
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
      </div> : <></>}
</div>
}
