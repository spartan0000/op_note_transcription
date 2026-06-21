import { useState, useRef, useCallback } from 'react'
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom'
import NotePage from './NotePage.jsx'
import LoginPage from './LoginPage.jsx'
import RegisterPage from './RegisterPage.jsx'
import './App.css'

const API_BASE = '/api'

const hasSpeechRecognition = !!(window.SpeechRecognition || window.webkitSpeechRecognition)

function isTokenValid(token) {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.exp * 1000 > Date.now()
  } catch {
    return false
  }
}

function ProtectedRoute({ children }) {
  const token = localStorage.getItem('token')
  if (!token || !isTokenValid(token)) {
    localStorage.removeItem('token')
    return <Navigate to="/login" replace />
  }
  return children
}

function HomePage() {
  const navigate = useNavigate()
  const [transcript, setTranscript] = useState('')
  const [interim, setInterim] = useState('')
  const [isListening, setIsListening] = useState(false)
  const [status, setStatus] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [noteId, setNoteId] = useState('')
  const [error, setError] = useState('')
  const [copied, setCopied] = useState(false)

  const recognitionRef = useRef(null)
  const isListeningRef = useRef(false)
  const finalTranscriptRef = useRef('')

  const initRecognition = useCallback(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    const rec = new SpeechRecognition()
    rec.continuous = true
    rec.interimResults = true
    rec.lang = 'en-US'

    rec.onstart = () => {
      setStatus('Listening...')
    }

    rec.onresult = (event) => {
      let interimText = ''
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const text = event.results[i][0].transcript
        if (event.results[i].isFinal) {
          finalTranscriptRef.current += text + ' '
        } else {
          interimText += text
        }
      }
      setTranscript(finalTranscriptRef.current)
      setInterim(interimText)
    }

    rec.onerror = (event) => {
      if (event.error !== 'no-speech') {
        setError('Speech recognition error: ' + event.error)
        stopListening()
      }
    }

    // Chrome stops after silence — restart if still in listening mode
    rec.onend = () => {
      if (isListeningRef.current) rec.start()
    }

    return rec
  }, [])

  const stopListening = useCallback(() => {
    isListeningRef.current = false
    setIsListening(false)
    if (recognitionRef.current) {
      recognitionRef.current.onend = null
      recognitionRef.current.stop()
    }
    setStatus('')
    setInterim('')
  }, [])

  const toggleDictation = useCallback(() => {
    if (!hasSpeechRecognition) return

    if (!isListeningRef.current) {
      isListeningRef.current = true
      setIsListening(true)
      finalTranscriptRef.current = transcript
      setNoteId('')
      setError('')
      recognitionRef.current = initRecognition()
      recognitionRef.current.start()
    } else {
      stopListening()
    }
  }, [transcript, initRecognition, stopListening])

  const handleTranscriptChange = (e) => {
    setTranscript(e.target.value)
    finalTranscriptRef.current = e.target.value
  }

  const handleSubmit = async () => {
    const text = transcript.trim()
    if (!text) return
    setIsSubmitting(true)
    setNoteId('')
    setError('')

    try {
      const res = await fetch(`${API_BASE}/transcribe-text`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript: text }),
      })
      if (!res.ok) throw new Error('Submission failed')
      const data = await res.json()
      setNoteId(data.note_id)
    } catch (err) {
      setError('Error: ' + err.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleUpload = async (e) => {
    const file = e.target.files?.[0]
    if (!file) return
    setIsUploading(true)
    setNoteId('')
    setError('')

    const formData = new FormData()
    formData.append('file', file, file.name)

    try {
      const res = await fetch(`${API_BASE}/transcribe`, { method: 'POST', body: formData })
      if (!res.ok) throw new Error('Upload failed')
      const data = await res.json()
      setNoteId(data.note_id)
    } catch (err) {
      setError('Error: ' + err.message)
    } finally {
      setIsUploading(false)
      e.target.value = ''
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  const noteUrl = noteId ? `${window.location.origin}/note/${noteId}` : ''

  const copyLink = async () => {
    await navigator.clipboard.writeText(noteUrl)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const submitDisabled = !transcript.trim() || isListening || isSubmitting

  return (
    <div className="container">
      <div className="page-header">
        <h1>Op Note Dictation</h1>
        <button className="btn logout-btn" onClick={handleLogout}>Log Out</button>
      </div>

      {!hasSpeechRecognition && (
        <p className="browser-warning">
          Speech recognition is not available. Please use Chrome or Edge.
        </p>
      )}

      <button
        className={`btn dictate-btn ${isListening ? 'recording' : ''}`}
        onClick={toggleDictation}
        disabled={!hasSpeechRecognition}
      >
        {isListening ? 'Stop Dictating' : 'Start Dictating'}
      </button>

      {status && <div className="status">{status}</div>}

      <textarea
        className="transcript"
        placeholder="Transcript will appear here as you speak..."
        value={transcript}
        onChange={handleTranscriptChange}
      />

      {interim && <div className="interim">{interim}</div>}

      <button
        className="btn submit-btn"
        onClick={handleSubmit}
        disabled={submitDisabled}
      >
        {isSubmitting ? 'Processing...' : 'Submit Note'}
      </button>

      <div className="divider">
        <hr /><span>or upload a file</span><hr />
      </div>

      <label className={`btn upload-btn ${isUploading ? 'disabled' : ''}`}>
        {isUploading ? 'Processing...' : 'Upload & Transcribe'}
        <input
          type="file"
          accept="audio/*"
          onChange={handleUpload}
          disabled={isUploading}
          hidden
        />
      </label>

      {error && <div className="error">{error}</div>}

      {noteUrl && (
        <div className="result">
          <p>Your note is ready:</p>
          <a className="note-url" href={noteUrl} target="_blank" rel="noreferrer">{noteUrl}</a>
          <button className="btn copy-btn" onClick={copyLink}>
            {copied ? 'Copied!' : 'Copy Link'}
          </button>
        </div>
      )}
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/" element={<ProtectedRoute><HomePage /></ProtectedRoute>} />
        <Route path="/note/:noteId" element={<ProtectedRoute><NotePage /></ProtectedRoute>} />
      </Routes>
    </BrowserRouter>
  )
}
