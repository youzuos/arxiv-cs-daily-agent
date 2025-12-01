import { BrowserRouter, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import DetailPage from './pages/DetailPage'
import CategoryPage from './pages/CategoryPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/category/:categoryId" element={<CategoryPage />} />
        <Route path="/paper/:paperId" element={<DetailPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
