import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import './Navbar.css'

const Navbar = () => {
  const location = useLocation()

  const isActive = (path) => location.pathname === path

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-left">
          <Link to="/" className="nav-link">Home</Link>
          <Link to="/services" className={`nav-link ${isActive('/services') ? 'active' : ''}`}>Services</Link>
        </div>
        
        <div className="navbar-center">
          <Link to="/" className="logo">
            <div className="logo-icon">☀</div>
            <span className="logo-text">AgriDroneX</span>
          </Link>
        </div>
        
        <div className="navbar-right">
          <Link to="/insights" className={`nav-link ${isActive('/insights') ? 'active' : ''}`}>Insights</Link>
          <Link to="/about" className="nav-link">About Us</Link>
          <Link to="/contact" className="nav-link">Contact</Link>
          <Link to="/weather" className="nav-link weather-button">Weather</Link>
        </div>
      </div>
    </nav>
  )
}

export default Navbar

