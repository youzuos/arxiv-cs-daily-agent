import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import PaperDetail from './PaperDetail'
import '../App.css'
import fallbackPapers from '../data/papers.json'

export default function DetailPage() {
  const { paperId } = useParams()
  const navigate = useNavigate()
  const [papers, setPapers] = useState(fallbackPapers)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchPapers = async () => {
      setPapers(fallbackPapers)
      setLoading(false)
      
      // 尝试从后端获取最新数据
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 3000)
      try {
        const res = await fetch('http://127.0.0.1:8000/papers', {
          signal: controller.signal
        })
        clearTimeout(timeoutId)
        if (res.ok) {
          const payload = await res.json()
          if (payload?.papers?.length) {
            setPapers(payload.papers)
          }
        }
      } catch (err) {
        clearTimeout(timeoutId)
        // 静默失败，使用本地数据
        console.log('Using local data for detail page')
      }
    }
    fetchPapers()
  }, [])

  const paper = papers.find((p) => p.id === paperId)

  if (loading) {
    return <div className="app-shell"><p>Loading...</p></div>
  }

  if (!paper) {
    return (
      <div className="app-shell">
        <header className="banner">
          <div className="brand">
            <span className="logo-dot" />
            <div>
              <p className="eyebrow">Daily Tracker</p>
              <h1>arXiv CS Daily</h1>
            </div>
          </div>
          <nav>
            <Link to="/">Home</Link>
          </nav>
        </header>
        <div style={{ padding: '2rem', textAlign: 'center' }}>
          <h2>Paper Not Found</h2>
          <p>The paper you're looking for doesn't exist.</p>
          <Link to="/" style={{ color: '#0066cc', textDecoration: 'underline' }}>
            ← Back to Home
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="app-shell">
      <header className="banner">
        <div className="brand">
          <span className="logo-dot" />
          <div>
            <p className="eyebrow">Daily Tracker</p>
            <h1>arXiv CS Daily</h1>
          </div>
        </div>
        <nav>
          <Link to="/">Home</Link>
          <Link to="/#papers">All Papers</Link>
        </nav>
        <button className="cta" onClick={() => navigate('/')}>
          ← Back to Home
        </button>
      </header>

      <section className="detail-panel" style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
        <PaperDetail paper={paper} />
      </section>
    </div>
  )
}

