import React from 'react'
import './Contact.css'
import ChatButton from '../components/ChatButton'

const Contact = () => {
  return (
    <div className="contact-page">
      <div className="contact-container">
        <h1 className="contact-title">Contact Us</h1>
        <div className="contact-content">
          <div className="contact-info">
            <div className="contact-item">
              <span className="contact-icon">📍</span>
              <div>
                <h3>Address</h3>
                <p>123 AgriTech Plaza, Innovation District, Tech City 12345</p>
              </div>
            </div>
            <div className="contact-item">
              <span className="contact-icon">📞</span>
              <div>
                <h3>Phone</h3>
                <p>+1 (555) 123-4567</p>
              </div>
            </div>
            <div className="contact-item">
              <span className="contact-icon">✉️</span>
              <div>
                <h3>Email</h3>
                <p>info@agridronex.com</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <ChatButton />
    </div>
  )
}

export default Contact

