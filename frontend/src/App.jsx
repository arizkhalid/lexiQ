import { useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import './App.css'
import Home from './pages/Home'
import Paragraph from './pages/Paragraph'
import Quiz from './pages/Quiz'
import ProtectedRoute from './routes/ProtectedRoute'
import Login from './pages/Login'
import SignUp from './pages/Signup.jsx'

function App() {

  return (
    <Routes>
      <Route path="/" element={<ProtectedRoute><Home /></ProtectedRoute>} />
      <Route path="/paragraph" element={<ProtectedRoute><Paragraph /></ProtectedRoute>} />
      <Route path="/quiz" element={<ProtectedRoute><Quiz /></ProtectedRoute>} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<SignUp />} />
    </Routes>
  )
}

export default App
