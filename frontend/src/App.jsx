import { useState, useRef, useEffect, useCallback } from 'react'
import './App.css'

const API_BASE = '/api'

const hasSpeechRecognition = !!(window.SpeechRecognition || window.webkitSpeechRecognition)

export default function App() {
  const [transcript, setTranscript] = useState('')
  const [interim, setInterim] = useState('')
  const [isListening, setIsListening] = useState(false)
  const [status, setStatus] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [noteUrl, setNoteUrl] = useState('')
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
      setNoteUrl('')
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
    setNoteUrl('')
    setError('')

    try {
      const res = await fetch(`${API_BASE}/transcribe-text`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript: text }),
      })
      if (!res.ok) throw new Error('Submission failed')
      const data = await res.json()
      setNoteUrl(data.url)
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
    setNoteUrl('')
    setError('')

    const formData = new FormData()
    formData.append('file', file, file.name)

    try {
      const res = await fetch(`${API_BASE}/transcribe`, { method: 'POST', body: formData })
      if (!res.ok) throw new Error('Upload failed')
      const data = await res.json()
      setNoteUrl(data.url)
    } catch (err) {
      setError('Error: ' + err.message)
    } finally {
      setIsUploading(false)
      e.target.value = ''
    }
  }

  const copyLink = async () => {
    await navigator.clipboard.writeText(noteUrl)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const submitDisabled = !transcript.trim() || isListening || isSubmitting

  return (
    <div className="container">
      <h1>Op Note Dictation</h1>

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
          <p className="note-url">{noteUrl}</p>
          <button className="btn copy-btn" onClick={copyLink}>
            {copied ? 'Copied!' : 'Copy Link'}
          </button>
        </div>
      )}
    </div>
  )
}
