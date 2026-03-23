import Navbar from "../components/Navbar"
import { Link } from "react-router-dom"
import style from "./Home.module.css"
import Footer from "../components/Footer"
function BookSVG() {
  return <svg xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24" viewBox="0 0 24 24" fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
        className="w-6 stroke-black h-6">
<path d="M12 7v14"></path><path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z"></path></svg>
}
export default function Home() {
  return <>
    <Navbar />
    <section className="flex flex-col gap-8 font-sans">
      <div className="max-w-[800px] mx-auto mt-[100px]">
        <h1>
          The Best Way To Improve Your English Vocabulary
        </h1>
        <div className="flex gap-5 justify-center items-center text-white mt-8">
          <Link to="/paragraph"><button className={style.button}>
            Read Paragraph
          </button></Link>
          <button className={style.button}>
            Take Quiz
          </button>
        </div>
      </div>
      <div className="flex flex-col gap-8 max-w-[800px] mx-auto">
        <h1>How it works?</h1>
        <div className="flex gap-9 items-center justify-center">
          <div className={style.stepBox}>
            <BookSVG />
            <span>Read</span>
            <p>Choose from the given paragraphs or upload your own</p>
          </div>
          <div className={style.stepBox}>
            <BookSVG />
            <span>Hover</span>
            <p>Hover over the words you find difficult to see  their meaning, or click to seem other gramatical details</p>
          </div>
          <div className={style.stepBox}>
            <BookSVG />
            <span>Solve</span>
            <p>Take an AI generated quiz that is based on the words you find difficult, We will keep track of what you do and dont know!</p>
          </div>
        </div>
      </div>
    </section>
    <Footer />
  </>
}
