import CatalogueAFS from './pages/CatalogueAFS'
import './App.css'

export default function App() {
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
            <a className="nav-link active" href="#">Catalogue AFS</a>
            <a className="nav-link" href="#">Sessions</a>
            <a className="nav-link" href="#">Stagiaires</a>
          </nav>
        </div>
      </header>
      <main className="main">
        <CatalogueAFS />
      </main>
    </div>
  )
}
