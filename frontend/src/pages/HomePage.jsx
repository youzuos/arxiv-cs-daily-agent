import { useEffect, useMemo, useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
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

export default function HomePage() {
  const navigate = useNavigate()
  console.log('Fallback papers count:', fallbackPapers?.length || 0)
  const [papers, setPapers] = useState(fallbackPapers)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [activeCategory, setActiveCategory] = useState('ALL')
  const [selectedDate, setSelectedDate] = useState(null)
  const [menuOpen, setMenuOpen] = useState(false)

  useEffect(() => {
    const fetchPapers = async () => {
      // 先直接使用本地数据，确保立即显示
      console.log('📚 Using local papers data:', fallbackPapers.length, 'papers')
      setPapers(fallbackPapers)
      setLoading(false)
      
      // 然后尝试从后端获取最新数据（可选）
      const controller = new AbortController()
      const timeoutId = setTimeout(() => {
        controller.abort()
      }, 3000) // 3秒超时

      try {
        const res = await fetch('http://127.0.0.1:8000/papers', {
          signal: controller.signal
        })
        clearTimeout(timeoutId)
        if (!res.ok) throw new Error(`Backend responded with ${res.status}`)
        const payload = await res.json()
        console.log('✅ Backend returned papers:', payload?.papers?.length || 0)
        if (payload?.papers?.length && payload.papers.length > 0) {
          setPapers(payload.papers)
          setError(null) // 清除错误信息
        }
      } catch (err) {
        clearTimeout(timeoutId)
        // 静默失败，因为已经使用了本地数据
        if (err.name !== 'AbortError') {
          console.log('ℹ️ Backend not available, using local data')
        }
      }
    }
    fetchPapers()
  }, [])

  const latestDates = useMemo(() => {
    const dates = [...new Set(papers.map((paper) => paper.submittedAt))]
    return dates.sort((a, b) => b.localeCompare(a)) // 最新的在前
  }, [papers])

  const filteredPapers = useMemo(() => {
    let result = papers
    console.log('Total papers:', papers.length, 'Category:', activeCategory, 'Date:', selectedDate)
    // 按分类过滤
    if (activeCategory !== 'ALL') {
      result = result.filter((paper) => paper.categories.includes(activeCategory))
      console.log('After category filter:', result.length)
    }
    // 按日期过滤
    if (selectedDate) {
      result = result.filter((paper) => paper.submittedAt === selectedDate)
      console.log('After date filter:', result.length)
    }
    console.log('Final filtered papers:', result.length)
    return result
  }, [papers, activeCategory, selectedDate])

  const activeCategoryTitle =
    activeCategory === 'ALL'
      ? 'Latest Computer Science Papers'
      : `${categoryMap[activeCategory]?.title || activeCategory} Papers`

  const handlePaperClick = (paperId) => {
    navigate(`/paper/${paperId}`)
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
          <Link to="/" className="active">
            Home
          </Link>
          <a href="#papers">All Papers</a>
          <div className="nav-categories">
            <button type="button" onClick={() => setMenuOpen((prev) => !prev)}>
              Categories ▾
            </button>
            {menuOpen && (
              <div className="nav-dropdown">
                {categories.map((cat) => (
                  <button
                    key={cat.id}
                    className={cat.id === activeCategory ? 'active' : ''}
                    type="button"
                    onClick={() => {
                      setActiveCategory(cat.id)
                      setMenuOpen(false)
                    }}
                  >
                    {cat.id} · {cat.title}
                  </button>
                ))}
              </div>
            )}
          </div>
        </nav>
        <button className="cta" onClick={() => {
          document.getElementById('papers')?.scrollIntoView({ behavior: 'smooth' })
        }}>
          View Latest Papers
        </button>
      </header>

      <section className="hero" id="home">
        <div>
          <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>arXiv CS Daily</h1>
          <h2 style={{ fontSize: '1.5rem', marginBottom: '1rem', fontWeight: 'normal' }}>
            Track the latest computer science research papers from arXiv.org
          </h2>
          <p style={{ fontSize: '1.1rem', color: '#666', lineHeight: '1.6' }}>
            Browse by category or view the most recent submissions across all CS fields.
          </p>
          <button 
            style={{ 
              marginTop: '1.5rem', 
              padding: '0.75rem 2rem', 
              fontSize: '1rem',
              backgroundColor: '#0066cc',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
            onClick={() => {
              document.getElementById('papers')?.scrollIntoView({ behavior: 'smooth' })
            }}
          >
            View Latest Papers
          </button>
        </div>
      </section>

      <section className="categories">
        <div className="section-heading">
          <h3>Computer Science Categories</h3>
          <p>arXiv's Computer Science (cs) archive is organized into the following subject categories:</p>
        </div>
        <div className="grid">
          {categories.map((cat) => (
            <article
              key={cat.id}
              className={`category-card ${activeCategory === cat.id ? 'active' : ''}`}
              onClick={() => setActiveCategory(cat.id)}
            >
              <p className="category-id">{cat.id}</p>
              <h4>{cat.title}</h4>
              <p>{cat.description}</p>
              <button 
                type="button"
                onClick={(e) => {
                  e.stopPropagation()
                  navigate(`/category/${cat.id}`)
                }}
              >
                Browse Papers
              </button>
            </article>
          ))}
        </div>
      </section>

      <section className="paper-feed" id="papers">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Daily feed</p>
            <h3>{activeCategoryTitle}</h3>
            <p className="active-filter">
              Filtering by: {activeCategory}
              {selectedDate && ` · ${selectedDate}`}
            </p>
          </div>
          <label className="filter">
            <span>Publication Date</span>
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
          {error && <p className="error-text">{error}</p>}
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
                <button onClick={() => handlePaperClick(paper.id)}>View Details</button>
              </div>
            </article>
            ))}
        </div>
      </section>
    </div>
  )
}

