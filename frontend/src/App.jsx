import { Routes, Route } from 'react-router-dom'
import './App.css'
import Home from './pages/Home'
import ProtectedRoute from './routes/ProtectedRoute'
import Login from './pages/Login'
import SignUp from './pages/Signup.jsx'
import Navbar from './components/Navbar.jsx'
import { lazy, Suspense } from 'react'

const Paragraph = lazy(() => import('./pages/Paragraph'))
const Quiz = lazy(() => import('./pages/Quiz'))
const Read = lazy(() => import('./pages/Read.jsx'))

function App() {

  return (<>
    <Navbar />
    <Routes>
      <Route path="/" element={<ProtectedRoute><Home /></ProtectedRoute>} />
      <Route path="/paragraph" element={<ProtectedRoute><Suspense fallback={<div>Loading...</div>}><Paragraph /></Suspense></ProtectedRoute>} />
      <Route path="/paragraph/read" element={<ProtectedRoute><Suspense fallback={<div>Loading...</div>}><Read /></Suspense></ProtectedRoute>} />
      <Route path="/quiz" element={<ProtectedRoute><Suspense fallback={<div>Loading...</div>}><Quiz /></Suspense></ProtectedRoute>} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<SignUp />} />
    </Routes>
</>
  )
}

export default App
