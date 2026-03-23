import { useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import './App.css'
import Home from './pages/Home'
import Paragraph from './pages/Paragraph'
import Quiz from './pages/Quiz'

function App() {

  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/paragraph" element={<Paragraph />} />
      <Route path="/quiz" element={<Quiz />} />
    </Routes>
  )
}

export default App
