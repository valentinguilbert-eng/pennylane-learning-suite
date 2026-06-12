import { auth as authApi } from './api.js'

export const ROLES = {
  admin:     'admin',
  formateur: 'formateur',
}

const SESSION_KEY = 'pls_session'

export async function login(email, password) {
  const data = await authApi.login(email, password)
  // data = { token, user: { id, email, nom, prenom, role } }
  localStorage.setItem(SESSION_KEY, JSON.stringify(data))
  return data.user.role
}

export function logout() {
  localStorage.removeItem(SESSION_KEY)
}

export function getSession() {
  try {
    return JSON.parse(localStorage.getItem(SESSION_KEY) || 'null')
  } catch {
    return null
  }
}

export function getCurrentUser() {
  return getSession()?.user || null
}

export function isAdmin() {
  return getCurrentUser()?.role === ROLES.admin
}

export function isFormateur() {
  const role = getCurrentUser()?.role
  return role === ROLES.formateur || role === ROLES.admin
}
