import React, { useState } from 'react'
import Chatbot from './Chatbot'
import './ChatButton.css'

const ChatButton = () => {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <div className="chat-button" onClick={() => setIsOpen(true)}>
        <div className="chat-icon">💬</div>
      </div>
      <Chatbot isOpen={isOpen} onClose={() => setIsOpen(false)} />
    </>
  )
}

export default ChatButton

