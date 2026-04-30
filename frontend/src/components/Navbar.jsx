import { Link, useNavigate } from "react-router-dom"
import arrowIcon from "../assets/arrow.svg"
import style from "./Navbar.module.css"
import { useState } from "react";
function Navbar() {
  const [instructions, setInstructions] = useState(false)
  const navigate = useNavigate();
  const handleLogout = () => {
    localStorage.clear("access");
    navigate("/login");
  }
  return <nav className="flex h-[65px] items-center py-2 px-8 gap-5">
    <Link to="/">
      <div className="w-10 h-10 bg-black flex items-center justify-center">
        <svg xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24" viewBox="0 0 24 24" fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="w-6 stroke-white h-6"><path d="M12 7v14"></path><path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z"></path></svg></div></Link>
    <div className="h-fit">
      <ul className="flex justify-evenly gap-3 text-black">
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/paragraph">Paragraphs</Link>
        </li>
        <li>
          <Link to="/quiz">Quiz</Link>
        </li>
      </ul>
    </div>
    <div className="ml-auto">
      <span onClick={() => {setInstructions(true)}} className="cursor-pointer">Instructions</span>
      <span onClick={handleLogout} className="cursor-pointer ml-8">Log Out</span>
    </div>
    {instructions && <div>
      <div className="h-[85%] w-[75%] absolute left-[15%] top-[10%] bg-white border-2 border-black">
              <span className="absolute right-3 top-2 bg-black text-white cursor-pointer rounded font-bold h-6 w-6" onClick={() => {setInstructions(false)}}>x</span>
              <div className="text-3xl items-center justify-center flex text-left font-sans h-full">
                <ul className={`${style.instructions} gap-5 flex flex-col`}>
                  <li className={style.instruction}>Select a Paragraph</li>
                  <li className="flex justify-center rotate-180"><img src={arrowIcon} alt="icon" className="h-10 w-10" /></li>
                  <li className={style.instruction}>Read</li>
                  <li className="flex justify-center rotate-180"><img src={arrowIcon} alt="icon" className="h-10 w-10" /></li>
                  <li className={style.instruction}>Hover to learn about unfamiliar words</li>
                  <li className="flex justify-center rotate-180"><img src={arrowIcon} alt="icon" className="h-10 w-10" /></li>
                  <li className={style.instruction}>Click to add to weak words</li>
                  <li className="flex justify-center rotate-180"><img src={arrowIcon} alt="icon" className="h-10 w-10" /></li>
                  <li className={style.instruction}>Generate quiz based on your weak words</li>
                </ul>
              </div>
            </div>
    </div>}
  </nav>
}
export default Navbar
