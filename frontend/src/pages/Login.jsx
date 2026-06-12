import { useState } from 'react'
import { login } from '../data/auth'
import './Login.css'

export default function Login({ onLogin }) {
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  function handleSubmit(e) {
    e.preventDefault()
    setLoading(true)
    setError('')
    setTimeout(() => {
      const role = login(password)
      if (role) {
        onLogin(role)
      } else {
        setError('Mot de passe incorrect.')
        setLoading(false)
      }
    }, 400)
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-logo">
          <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" className="login-svg">
            <circle cx="20" cy="20" r="20" fill="#00F872"/>
            <rect x="13" y="13" width="3.5" height="18" rx="1.75" fill="#003D3D"/>
            <path d="M16.5 14.5 C16.5 14.5 24.5 14.5 24.5 20.5 C24.5 26.5 16.5 26.5 16.5 26.5" stroke="#003D3D" strokeWidth="3.5" strokeLinecap="round" fill="none"/>
          </svg>
          <span className="login-wordmark">pennylane</span>
        </div>
        <h1 className="login-title">Learning Suite · AFS</h1>
        <p className="login-subtitle">Accès sécurisé</p>

        <form className="login-form" onSubmit={handleSubmit}>
          <div className="login-field">
            <label htmlFor="password">Mot de passe</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={e => { setPassword(e.target.value); setError('') }}
              placeholder="••••••••••"
              autoFocus
              autoComplete="current-password"
            />
          </div>
          {error && <p className="login-error">{error}</p>}
          <button className="login-btn" type="submit" disabled={loading || !password}>
            {loading ? 'Connexion…' : 'Se connecter'}
          </button>
        </form>

        <p className="login-hint">
          Administrateur : <code>admin2026</code><br />
          Formateur : <code>formateur2026</code>
        </p>
      </div>
    </div>
  )
}
