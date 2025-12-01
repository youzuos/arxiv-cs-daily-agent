import { useEffect, useMemo, useState } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import '../App.css'
import fallbackPapers from '../data/papers.json'

const categories = [
  { id: 'ALL', title: 'All Papers', description: 'Browse every tracked submission.' },
  { id: 'cs.AI', title: 'Artificial Intelligence', description: 'Learning, reasoning, robotics, multi-agent systems.' },
  { id: 'cs.AR', title: 'Hardware Architecture', description: 'Systems design, accelerators, compute hardware.' },
  { id: 'cs.CC', title: 'Computational Complexity', description: 'Algorithms, proofs, and theoretical CS.' },
  { id: 'cs.CV', title: 'Computer Vision', description: 'Vision transformers, 3D perception, multimodality.' },
  { id: 'cs.LG', title: 'Machine Learning', description: 'Foundation models, optimization, generalization.' },
  { id: 'cs.SE', title: 'Software Engineering', description: 'Dev tools, testing, programming languages.' }
]

const categoryMap = categories.reduce((acc, cat) => {
  acc[cat.id] = cat
  return acc
}, {})

export default function CategoryPage() {
  const { categoryId } = useParams()
  const navigate = useNavigate()
  const [papers, setPapers] = useState(fallbackPapers)
  const [loading, setLoading] = useState(true)
  const [selectedDate, setSelectedDate] = useState(null)

  const category = categoryMap[categoryId || 'ALL']

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
        console.log('Using local data for category page')
      }
    }
    fetchPapers()
  }, [])

  const latestDates = useMemo(() => {
    const dates = [...new Set(papers.map((paper) => paper.submittedAt))]
    return dates.sort((a, b) => b.localeCompare(a))
  }, [papers])

  const filteredPapers = useMemo(() => {
    let result = papers
    // 按分类过滤
    if (categoryId && categoryId !== 'ALL') {
      result = result.filter((paper) => paper.categories.includes(categoryId))
    }
    // 按日期过滤
    if (selectedDate) {
      result = result.filter((paper) => paper.submittedAt === selectedDate)
    }
    return result
  }, [papers, categoryId, selectedDate])

  const handlePaperClick = (paperId) => {
    navigate(`/paper/${paperId}`)
  }

  if (!category && categoryId !== 'ALL') {
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
          <h2>Category Not Found</h2>
          <p>The category you're looking for doesn't exist.</p>
          <Link to="/" style={{ color: '#0066cc', textDecoration: 'underline' }}>
            ← Back to Home
          </Link>
        </div>
      </div>
    )
  }

  const pageTitle = categoryId === 'ALL' 
    ? 'All Papers' 
    : `${category.title} Papers`
  
  const pageSubtitle = categoryId === 'ALL'
    ? 'Showing all papers from arXiv'
    : `Showing the latest papers from arXiv in the category`

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
          <div className="nav-categories">
            <button type="button">Categories ▾</button>
          </div>
        </nav>
        <button className="cta" onClick={() => navigate('/')}>
          ← Back to Home
        </button>
      </header>

      <section className="paper-feed" style={{ padding: '2rem 0' }}>
        <div className="section-heading">
          <div>
            <h2 style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>{pageTitle}</h2>
            <p style={{ color: '#666', marginBottom: '1rem' }}>{pageSubtitle}</p>
          </div>
          <label className="filter">
            <span>Publication Date:</span>
            <select value={selectedDate || ''} onChange={(e) => setSelectedDate(e.target.value)}>
              <option value="">All Dates</option>
              {latestDates.map((date) => (
                <option key={date} value={date}>
                  {date}
                </option>
              ))}
            </select>
          </label>
        </div>
        <div className="paper-grid">
          {loading && <p>Loading latest submissions…</p>}
          {!loading && filteredPapers.length === 0 && (
            <p>No papers found in this category.</p>
          )}
          {!loading &&
            filteredPapers.map((paper) => (
            <article key={paper.id} className="paper-card">
              <p className="paper-date">{paper.submittedAt}</p>
              <h4>
                <Link 
                  to={`/paper/${paper.id}`}
                  style={{ textDecoration: 'none', color: 'inherit', cursor: 'pointer' }}
                >
                  {paper.title}
                </Link>
              </h4>
              <p className="paper-authors">{paper.authors.join(', ')}</p>
              <p className="paper-summary">{paper.abstract}</p>
              <div className="paper-tags">
                {paper.categories.map((tag) => (
                  <span key={tag}>{tag}</span>
                ))}
              </div>
              <div className="paper-actions">
                <a href={paper.pdfUrl} target="_blank" rel="noreferrer">
                  PDF
                </a>
                <button onClick={() => handlePaperClick(paper.id)}>Details</button>
              </div>
            </article>
            ))}
        </div>
      </section>
    </div>
  )
}

