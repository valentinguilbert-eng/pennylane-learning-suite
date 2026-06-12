import { useState } from 'react'
import CatalogueAFS from './pages/CatalogueAFS'
import Sessions from './pages/Sessions'
import Stagiaires from './pages/Stagiaires'
import Documents from './pages/Documents'
import './App.css'

const PAGES = [
  { id: 'catalogue', label: 'Catalogue AFS' },
  { id: 'sessions', label: 'Sessions' },
  { id: 'stagiaires', label: 'Stagiaires' },
  { id: 'documents', label: 'Documents Qualiopi' },
]

function PennylaneLogo() {
  return (
    <svg className="logo-svg" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Pennylane">
      {/* Demi-cercle gauche — pupille dirigeant */}
      <path d="M20 8 A12 12 0 0 0 20 32" stroke="#00F872" strokeWidth="5" strokeLinecap="round" fill="none"/>
      {/* Demi-cercle droit — pupille expert-comptable */}
      <path d="M20 12 A8 8 0 0 1 20 28" stroke="#ffffff" strokeWidth="5" strokeLinecap="round" fill="none"/>
    </svg>
  )
}

export default function App() {
  const [page, setPage] = useState('catalogue')

  return (
    <div className="app">
      <header className="header">
        <div className="header-inner">
          <div className="header-logo">
            <div className="logo-wordmark">
              <PennylaneLogo />
              <span className="logo-text">pennylane</span>
            </div>
            <div className="logo-sep" />
            <span className="logo-suite">Learning Suite · AFS</span>
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
        {page === 'documents' && <Documents />}
      </main>
    </div>
  )
}
