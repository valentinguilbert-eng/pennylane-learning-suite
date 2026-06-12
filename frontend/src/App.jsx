import { useState } from 'react'
import { getSession, logout, ROLES } from './data/auth'
import Login from './pages/Login'
import CatalogueAFS from './pages/CatalogueAFS'
import Sessions from './pages/Sessions'
import Stagiaires from './pages/Stagiaires'
import Documents from './pages/Documents'
import TableauDeBord from './pages/TableauDeBord'
import VeilleFormateur from './pages/VeilleFormateur'
import BanqueQuestions from './pages/BanqueQuestions'
import './App.css'

const PAGES_ADMIN = [
  { id: 'catalogue',   label: 'Catalogue AFS' },
  { id: 'sessions',    label: 'Sessions' },
  { id: 'stagiaires',  label: 'Stagiaires' },
  { id: 'documents',   label: 'Documents Qualiopi' },
  { id: 'questions',   label: 'Questionnaires' },
  { id: 'veille',      label: 'Veille juridique' },
]

const PAGES_FORMATEUR = [
  { id: 'veille',    label: 'Veille juridique' },
  { id: 'catalogue', label: 'Catalogue AFS' },
]

function PennylaneLogo() {
  return (
    <svg className="logo-svg" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Pennylane">
      <path d="M20 8 A12 12 0 0 0 20 32" stroke="#00F872" strokeWidth="5" strokeLinecap="round" fill="none"/>
      <path d="M20 12 A8 8 0 0 1 20 28" stroke="#ffffff" strokeWidth="5" strokeLinecap="round" fill="none"/>
    </svg>
  )
}

function RoleBadge({ role }) {
  if (role === ROLES.admin) return <span className="role-badge role-admin">Admin</span>
  return <span className="role-badge role-formateur">Formateur</span>
}

export default function App() {
  const [session, setSession] = useState(getSession())
  const [page, setPage] = useState(null)

  function handleLogin(role) {
    setSession({ role })
    setPage(role === ROLES.admin ? 'catalogue' : 'veille')
  }

  function handleLogout() {
    logout()
    setSession(null)
    setPage(null)
  }

  if (!session) return <Login onLogin={handleLogin} />

  const isAdmin = session.role === ROLES.admin
  const pages = isAdmin ? PAGES_ADMIN : PAGES_FORMATEUR
  const currentPage = page || pages[0].id

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
            {pages.map(p => (
              <button
                key={p.id}
                className={`nav-link ${currentPage === p.id ? 'active' : ''}`}
                onClick={() => setPage(p.id)}
              >
                {p.label}
                {p.id === 'tableau' && isAdmin && <span className="nav-dot" />}
              </button>
            ))}
          </nav>
          <div className="header-user">
            <RoleBadge role={session.role} />
            <button className="btn-logout" onClick={handleLogout} title="Se déconnecter">
              Déconnexion
            </button>
          </div>
        </div>
      </header>
      <main className="main">
        {currentPage === 'catalogue'  && <CatalogueAFS />}
        {currentPage === 'sessions'   && <Sessions />}
        {currentPage === 'stagiaires' && <Stagiaires />}
        {currentPage === 'documents'  && <Documents />}
        {currentPage === 'questions'  && <BanqueQuestions />}
        {currentPage === 'veille'     && (isAdmin ? <TableauDeBord /> : <VeilleFormateur />)}
      </main>
    </div>
  )
}
