import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import './Services.css'
import ChatButton from '../components/ChatButton'

const Services = () => {
  const [expandedCards, setExpandedCards] = useState({
    standard: true,
    premium: false
  })

  const toggleFeatures = (plan) => {
    setExpandedCards(prev => ({
      ...prev,
      [plan]: !prev[plan]
    }))
  }

  const standardFeatures = [
    'Monthly drone surveys',
    'Basic crop health analysis',
    'Weather monitoring',
    'Email support',
    'Field mapping up to 100 acres',
    'Standard resolution imagery'
  ]

  const premiumFeatures = [
    'Weekly drone surveys',
    'Advanced crop health analysis with AI',
    'Real-time weather monitoring',
    '24/7 Priority support',
    'Unlimited field mapping',
    'High-resolution multispectral imagery',
    'Custom analytics dashboard',
    'Precision spraying recommendations',
    'Yield prediction models',
    'Mobile app access'
  ]

  return (
    <div className="services-page">
      <div className="services-container">
        <h1 className="services-title">Our Services</h1>
        <p className="services-subtitle">Choose the plan that fits your farming needs</p>
        
        <div className="pricing-cards">
          {/* Standard Plan */}
          <div className="pricing-card standard">
            <h2 className="card-title">Standard Plan</h2>
            <p className="card-subtitle">Perfect for small to medium-sized farms</p>
            <div className="card-price">
              <span className="price-amount">$299</span>
              <span className="price-period">/month</span>
            </div>
            <div className="card-features">
              <div 
                className="features-header" 
                onClick={() => toggleFeatures('standard')}
              >
                <span>View Features</span>
                <span className="caret">{expandedCards.standard ? '▲' : '▼'}</span>
              </div>
              {expandedCards.standard && (
                <ul className="features-list">
                  {standardFeatures.map((feature, index) => (
                    <li key={index}>
                      <span className="checkmark">✓</span>
                      {feature}
                    </li>
                  ))}
                </ul>
              )}
            </div>
            <Link to="/prediction" className="card-button standard-btn">
              Get Started
            </Link>
          </div>

          {/* Premium Plan */}
          <div className="pricing-card premium">
            <div className="popular-badge">Most Popular</div>
            <h2 className="card-title">Premium Plan</h2>
            <p className="card-subtitle">Advanced features for professional farmers</p>
            <div className="card-price">
              <span className="price-amount">$599</span>
              <span className="price-period">/month</span>
            </div>
            <div className="card-features">
              <div 
                className="features-header" 
                onClick={() => toggleFeatures('premium')}
              >
                <span>View Features</span>
                <span className="caret">{expandedCards.premium ? '▲' : '▼'}</span>
              </div>
              {expandedCards.premium && (
                <ul className="features-list">
                  {premiumFeatures.map((feature, index) => (
                    <li key={index}>
                      <span className="checkmark">✓</span>
                      {feature}
                    </li>
                  ))}
                </ul>
              )}
            </div>
            <Link to="/prediction" className="card-button premium-btn">
              Get Started
            </Link>
          </div>
        </div>
      </div>
      <ChatButton />
    </div>
  )
}

export default Services

