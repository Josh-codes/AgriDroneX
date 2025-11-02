import React from 'react'
import { Link } from 'react-router-dom'
import './Home.css'
import ChatButton from '../components/ChatButton'

const Home = () => {
  return (
    <div className="home">
      {/* Hero Section with Background Image */}
      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">Precision Agriculture from Above</h1>
          <p className="hero-subtitle">Advanced drone technology for smarter, more efficient farming.</p>
          <div className="hero-buttons">
            <Link to="/services" className="btn btn-primary">Explore Services</Link>
            <Link to="/services" className="btn btn-secondary">Get Started</Link>
          </div>
        </div>
      </section>

      {/* Transform Your Farm Section */}
      <section className="transform-section">
        <div className="transform-content">
          <div className="transform-text">
            <h2 className="transform-title">
              Transform Your<br />
              Farm with<br />
              <span className="text-green">Precision</span><br />
              <span className="text-green">Agriculture</span>
            </h2>
            <p className="transform-description">
              Harness the power of drone technology to maximize crop yields, reduce costs, and make data-driven decisions for sustainable farming.
            </p>
            <div className="transform-buttons">
              <Link to="/services" className="btn btn-primary">Explore Services</Link>
              <Link to="/services" className="btn btn-outline">Get Started</Link>
            </div>
          </div>
          <div className="transform-image">
            <div className="drone-placeholder">
              <img src="https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=600" alt="Agricultural Drone" />
            </div>
          </div>
        </div>
      </section>

      {/* Why Choose Us Section */}
      <section className="why-choose-section">
        <div className="why-choose-content">
          <h2 className="section-title">Why Choose AgriDroneX?</h2>
          <p className="section-subtitle">Advanced technology meets agricultural expertise</p>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🌱</div>
              <h3 className="feature-title">Crop Monitoring</h3>
              <p className="feature-description">Real-time crop health analysis with multispectral imaging</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📈</div>
              <h3 className="feature-title">Yield Optimization</h3>
              <p className="feature-description">Data-driven insights to maximize your harvest potential</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">⚡</div>
              <h3 className="feature-title">Quick Response</h3>
              <p className="feature-description">Rapid deployment for urgent field assessments</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🛡️</div>
              <h3 className="feature-title">Precision Spraying</h3>
              <p className="feature-description">Targeted application reduces costs and environmental impact</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Banner */}
      <section className="cta-banner">
        <div className="cta-content">
          <h2 className="cta-title">Ready to Revolutionize Your Farm?</h2>
          <p className="cta-subtitle">Join hundreds of farmers who have increased their yields by up to 35% with AgriDroneX</p>
          <Link to="/services" className="btn btn-cta">Schedule a Demo</Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <div className="footer-column">
            <div className="footer-logo">
              <div className="footer-logo-icon">☀</div>
              <span className="footer-logo-text">AgriDroneX</span>
            </div>
            <p className="footer-description">
              Transforming agriculture with precision drone technology for sustainable farming.
            </p>
          </div>
          <div className="footer-column">
            <h4 className="footer-heading">QUICK LINKS</h4>
            <ul className="footer-links">
              <li><Link to="/">Home</Link></li>
              <li><Link to="/services">Services</Link></li>
              <li><Link to="/insights">Insights</Link></li>
              <li><Link to="/about">About Us</Link></li>
              <li><Link to="/contact">Contact</Link></li>
            </ul>
          </div>
          <div className="footer-column">
            <h4 className="footer-heading">CONTACT US</h4>
            <div className="footer-contact">
              <p><span className="contact-icon">📍</span> 123 AgriTech Plaza, Innovation District, Tech City 12345</p>
              <p><span className="contact-icon">📞</span> +1 (555) 123-4567</p>
              <p><span className="contact-icon">✉️</span> info@agridronex.com</p>
            </div>
          </div>
        </div>
        <div className="footer-bottom">
          <p>© 2025 AgriDroneX. All rights reserved.</p>
        </div>
      </footer>

      <ChatButton />
    </div>
  )
}

export default Home

