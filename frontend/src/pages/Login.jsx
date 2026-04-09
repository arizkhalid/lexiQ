import { auth } from "../api/axios.js"
import { useEffect, useState } from "react";
import { useNavigate, Link } from 'react-router-dom'
import style from "./Login.module.css"

export default function Login() {
  const navigate = useNavigate();
  useEffect(() => {
    const login = localStorage.getItem("access");
    if (login) {
      navigate("/");
    }
  }, [])
  const [form, setForm] = useState({
    username: "",
    password: "",
  });

  function handleChange(e) {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  }

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      const res = await auth.post("token/", {
        username: form.username,
        password: form.password,
      });

      const tokens = res.data;
      localStorage.setItem("access", tokens.access);
      navigate("/");
    } catch (err) {
      console.error(err);
    }
  }

  return (
    <div className="w-full h-screen flex justify-center items-center flex-col gap-5">
      <form onSubmit={handleSubmit} className="flex flex-col m-auto gap-9 justify-center items-center">
        <h2 className="text-3xl">Login</h2>

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
          Login
        </button>
        <Link to="/signup"><span className="text-gray-500 font-light">or SignUp Here!</span></Link>
      </form>
    </div>
  );
}

