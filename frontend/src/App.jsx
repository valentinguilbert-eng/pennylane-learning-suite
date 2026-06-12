import { useState } from 'react'
import CatalogueAFS from './pages/CatalogueAFS'
import Sessions from './pages/Sessions'
import Stagiaires from './pages/Stagiaires'
import './App.css'

const PAGES = [
  { id: 'catalogue', label: 'Catalogue AFS' },
  { id: 'sessions', label: 'Sessions' },
  { id: 'stagiaires', label: 'Stagiaires' },
  { id: 'documents', label: 'Documents', disabled: true },
]

export default function App() {
  const [page, setPage] = useState('catalogue')

  return (
    <div className="app">
      <header className="header">
        <div className="header-inner">
          <div className="header-logo">
            <span className="logo-icon">◎</span>
            <span className="logo-text">pennylane</span>
            <span className="logo-sep">|</span>
            <span className="logo-suite">Learning Suite</span>
          </div>
          <nav className="header-nav">
            {PAGES.map(p => (
              <button
                key={p.id}
                className={`nav-link ${page === p.id ? 'active' : ''} ${p.disabled ? 'disabled' : ''}`}
                onClick={() => !p.disabled && setPage(p.id)}
                disabled={p.disabled}
                title={p.disabled ? 'Prochainement' : undefined}
              >
                {p.label}
                {p.disabled && <span className="nav-soon">bientôt</span>}
              </button>
            ))}
          </nav>
        </div>
      </header>
      <main className="main">
        {page === 'catalogue' && <CatalogueAFS />}
        {page === 'sessions' && <Sessions />}
        {page === 'stagiaires' && <Stagiaires />}
      </main>
    </div>
  )
}
