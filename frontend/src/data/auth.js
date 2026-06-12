// Auth locale simple — pour sécuriser sans backend
// Mots de passe stockés en dur (frontend seulement — à remplacer par un vrai backend en prod)
export const ROLES = {
  admin:     'admin',
  formateur: 'formateur',
}

const CREDENTIALS = {
  admin2026:     ROLES.admin,
  formateur2026: ROLES.formateur,
}

const SESSION_KEY = 'pls_session'

export function login(password) {
  const role = CREDENTIALS[password]
  if (!role) return null
  const session = { role, loginAt: new Date().toISOString() }
  sessionStorage.setItem(SESSION_KEY, JSON.stringify(session))
  return role
}

export function logout() {
  sessionStorage.removeItem(SESSION_KEY)
}

export function getSession() {
  try {
    return JSON.parse(sessionStorage.getItem(SESSION_KEY) || 'null')
  } catch {
    return null
  }
}

export function isAdmin() {
  return getSession()?.role === ROLES.admin
}

export function isFormateur() {
  const role = getSession()?.role
  return role === ROLES.formateur || role === ROLES.admin
}
