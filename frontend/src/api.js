const API_URL = import.meta.env.VITE_API_URL || 'https://tarot-interpreter.onrender.com'

export const getImageUrl = (filename) => `${API_URL}/images/${filename}`

export async function dailyReading() {
  const res = await fetch(`${API_URL}/reading/daily`, { method: 'POST' })
  if (!res.ok) throw new Error('Reading failed')
  return res.json()
}

export async function threeCardReading(question) {
  const res = await fetch(`${API_URL}/reading/three-card`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  })
  if (!res.ok) throw new Error('Reading failed')
  return res.json()
}

export async function celticCrossReading(question) {
  const res = await fetch(`${API_URL}/reading/celtic-cross`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  })
  if (!res.ok) throw new Error('Reading failed')
  return res.json()
}
