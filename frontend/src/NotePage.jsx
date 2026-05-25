import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import './App.css'

const API_BASE = '/api'

const FIELD_LABELS = {
  preop_diagnosis: 'Pre-op Diagnosis',
  postop_diagnosis: 'Post-op Diagnosis',
  anesthesia: 'Anesthesia',
  date_of_dictation: 'Date of Dictation',
  date_of_procedure: 'Date of Procedure',
  procedures: 'Procedures',
  procedure_description: 'Procedure Description',
  ebl: 'Estimated Blood Loss (mL)',
  specimens: 'Specimens',
}

export default function NotePage() {
  const { noteId } = useParams()
  const [note, setNote] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${API_BASE}/note/${noteId}`)
      .then(res => {
        if (!res.ok) throw new Error(res.status === 404 ? 'Note not found or expired' : 'Failed to load note')
        return res.json()
      })
      .then(data => setNote(data))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [noteId])

  return (
    <div className="container">
      <Link to="/" className="back-link">← New Note</Link>
      <h1>Op Note</h1>

      {loading && <p className="status">Loading...</p>}
      {error && <p className="error">{error}</p>}

      {note && (
        <>
          <div className="note-card">
            {Object.entries(FIELD_LABELS).map(([key, label]) => {
              const val = note.structured_data?.[key]
              let display = '—'
              if (Array.isArray(val)) {
                const filtered = val.filter(Boolean)
                if (filtered.length > 0) display = filtered.join(', ')
              } else if (val != null && val !== '') {
                display = String(val)
              }
              return (
                <div className="note-field" key={key}>
                  <span className="note-label">{label}</span>
                  <span className="note-value">{display}</span>
                </div>
              )
            })}
          </div>

          {note.transcription && (
            <div className="transcription-section">
              <h2>Transcription</h2>
              <p className="transcription-text">{note.transcription}</p>
            </div>
          )}
        </>
      )}
    </div>
  )
}
