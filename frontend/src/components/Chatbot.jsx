import React, { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import './Chatbot.css'

const Chatbot = ({ isOpen, onClose }) => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I\'m your agricultural assistant. I can help you with crop recommendations, farming advice, and answer questions about agriculture. What would you like to know?'
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [location, setLocation] = useState(null)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    // Get user's location on component mount
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          })
        },
        (error) => {
          console.log('Location access denied or unavailable')
        }
      )
    }
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleSend = async (e) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage = { role: 'user', content: input.trim() }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const requestData = {
        message: userMessage.content
      }

      // Add location if available
      if (location) {
        requestData.location = `Latitude: ${location.latitude}, Longitude: ${location.longitude}`
      }

      const response = await axios.post('/api/chat/', requestData, {
        headers: {
          'Content-Type': 'application/json',
        }
      })

      const assistantMessage = {
        role: 'assistant',
        content: response.data.response
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Chat error:', error)
      const errorMessage = {
        role: 'assistant',
        content: error.response?.data?.error || 'Sorry, I encountered an error. Please try again later.'
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const quickQuestions = [
    'What crops are best for my area?',
    'How to prevent crop diseases?',
    'When is the best time to plant tomatoes?',
    'What is precision agriculture?'
  ]

  const handleQuickQuestion = (question) => {
    setInput(question)
    // Auto-send after setting input
    setTimeout(() => {
      const form = document.querySelector('.chatbot-form')
      if (form) {
        const event = new Event('submit', { bubbles: true, cancelable: true })
        form.dispatchEvent(event)
      }
    }, 100)
  }

  if (!isOpen) return null

  return (
    <div className="chatbot-overlay" onClick={onClose}>
      <div className="chatbot-container" onClick={(e) => e.stopPropagation()}>
        <div className="chatbot-header">
          <div className="chatbot-title">
            <span className="chatbot-icon">🌾</span>
            <h3>AgriDroneX Assistant</h3>
          </div>
          <button className="chatbot-close" onClick={onClose}>×</button>
        </div>

        <div className="chatbot-messages">
          {messages.map((msg, index) => (
            <div key={index} className={`chatbot-message ${msg.role}`}>
              <div className="message-content">
                {msg.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className="chatbot-message assistant">
              <div className="message-content loading">
                <span className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="chatbot-quick-questions">
          <p>Quick questions:</p>
          <div className="quick-questions-grid">
            {quickQuestions.map((q, index) => (
              <button
                key={index}
                className="quick-question-btn"
                onClick={() => handleQuickQuestion(q)}
                disabled={loading}
              >
                {q}
              </button>
            ))}
          </div>
        </div>

        <form className="chatbot-form" onSubmit={handleSend}>
          <input
            type="text"
            className="chatbot-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about crops, farming, or agriculture..."
            disabled={loading}
          />
          <button
            type="submit"
            className="chatbot-send"
            disabled={!input.trim() || loading}
          >
            Send
          </button>
        </form>
      </div>
    </div>
  )
}

export default Chatbot
