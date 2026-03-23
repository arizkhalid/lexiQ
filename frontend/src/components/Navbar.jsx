import style from "./Navbar.module.css"
import { Link } from "react-router-dom"
function Navbar() {
  return <nav className="flex h-[65px] items-center p-2 gap-5">
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
          <Link to="/paragraph">Paragraph</Link>
        </li>
        <li>
          <Link to="/quiz">Quiz</Link>
        </li>
      </ul>
    </div>
  </nav>
}
export default Navbar
