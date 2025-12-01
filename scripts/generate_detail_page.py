"""Generate a basic PaperDetail React component that consumes papers.json."""

from __future__ import annotations

from pathlib import Path

TEMPLATE = """import papers from '../data/papers.json'
import './PaperDetail.css'

export default function PaperDetail({ paperId }) {
  const paper = papers.find((item) => item.id === paperId) || papers[0]

  if (!paper) {
    return <div className="paper-detail">Paper not found.</div>
  }

  return (
    <section className="paper-detail">
      <p className="paper-detail__label">Paper Detail</p>
      <h2>{paper.title}</h2>
      <p className="paper-detail__meta">
        Submitted {paper.submittedAt} · {paper.categories.join(', ')}
      </p>
      <p className="paper-detail__authors">{paper.authors.join(', ')}</p>
      <p className="paper-detail__abstract">{paper.abstract}</p>
      <div className="paper-detail__actions">
        <a className="primary" href={paper.pdfUrl} target="_blank" rel="noreferrer">
          View PDF
        </a>
        <button onClick={() => navigator.clipboard.writeText(generateBibTex(paper))}>Copy BibTeX</button>
        <button onClick={() => navigator.clipboard.writeText(generateCitation(paper))}>Copy Citation</button>
      </div>
    </section>
  )
}

function generateBibTex(paper) {
  return `@article{${paper.id},
  title={${paper.title}},
  author={${paper.authors.join(' and ')}},
  year={${paper.submittedAt.split('-')[0]}},
  archivePrefix={arXiv},
  primaryClass={${paper.categories[0]}},
}`
}

function generateCitation(paper) {
  return `${paper.authors[0]} et al. ${paper.title}. arXiv:${paper.id} (${paper.submittedAt}).`
}
"""

CSS = """.paper-detail {
  background: #fff;
  border-radius: 18px;
  padding: 2rem;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.paper-detail__label {
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.1em;
  color: #94a3b8;
  margin: 0;
}
.paper-detail__meta {
  color: #475569;
}
.paper-detail__authors {
  font-weight: 500;
  color: #0f172a;
}
.paper-detail__abstract {
  color: #334155;
  line-height: 1.6;
}
.paper-detail__actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}
.paper-detail__actions a,
.paper-detail__actions button {
  border: none;
  border-radius: 999px;
  padding: 0.6rem 1.2rem;
  cursor: pointer;
}
.paper-detail__actions a.primary {
  background: #0ea5e9;
  color: #fff;
  text-decoration: none;
}
"""


def main() -> None:
  component = Path("frontend/src/pages")
  component.mkdir(parents=True, exist_ok=True)
  (component / "PaperDetail.jsx").write_text(TEMPLATE, encoding="utf-8")
  styles = Path("frontend/src/pages/PaperDetail.css")
  styles.write_text(CSS, encoding="utf-8")
  print("Generated PaperDetail component and styles.")


if __name__ == "__main__":
  main()

