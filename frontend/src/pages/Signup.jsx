import { auth } from "../api/axios.js"
import { useEffect, useState } from "react";
import { useNavigate, Link } from 'react-router-dom'
import style from "./Signup.module.css"

export default function SignUp() {
  const [form, setForm] = useState({
    username: "",
    password: "",
  });
  const [registered, setRegistered] = useState(false);
  const [error, setError] = useState(null);
  async function handleSubmit(e) {
    e.preventDefault();
    try {
      const res = await auth.post("register/", {username: form.username, password: form.password});
      console.log(res, res.data);
      if (res.status === 201) {
        setRegistered(true);
      }
    } catch (err) {
      console.log(err.response);
      if (err.response.status === 400) {
        console.log(err.response.data.username)
        setError(err.response.data.username[0]);
      }
    }
     
  }
  function handleChange(e) {
      setForm({
        ...form,
        [e.target.name]: e.target.value,
      });
    }
  return <div className="w-full h-screen flex justify-center items-center flex-col gap-5">
      { registered === true ? <div className="flex flex-col gap-9">
      <h2 className="text-4xl leading-relaxed">Welcome <span className="italic text-white bg-black inline-block px-2 py-0.5 skew-x-[-9deg]">{form.username}</span></h2> 
      <span className="text-2xl italic">Successfully Registered!!<br/>Please Login to to continue</span>
      <Link to="/login"><button>Log In</button></Link>
      </div> : <form onSubmit={handleSubmit} className="flex flex-col m-auto gap-9 justify-center items-center">
        <h2 className="text-3xl">Register</h2>
        {error && <span className="text-red-400 text-[0.75rem]">{error}</span>}
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={form.username}
          onChange={handleChange}
          required
        />

        <input
          type="password"
          name="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          required
        />

        <button type="submit">
          Register 
        </button>
        <Link to="/login"><span className="text-gray-500 font-light">Already registered?</span></Link>
      </form> }
  </div> 
}
