import papers from '../data/papers.json'
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
