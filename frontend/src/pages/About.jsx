import React from 'react'
import './About.css'
import ChatButton from '../components/ChatButton'

const About = () => {
  return (
    <div className="about-page">
      <div className="about-container">
        <h1 className="about-title">About Us</h1>
        <div className="about-content">
          <p className="about-text">
            AgriDroneX is at the forefront of agricultural technology, providing farmers 
            with cutting-edge drone solutions for precision agriculture. Our mission is 
            to revolutionize farming by making advanced technology accessible and practical 
            for farmers of all scales.
          </p>
          <p className="about-text">
            With a team of experts in agriculture, technology, and data science, we combine 
            deep industry knowledge with innovative solutions to help farmers maximize yields, 
            reduce costs, and make sustainable farming decisions.
          </p>
        </div>
      </div>
      <ChatButton />
    </div>
  )
}

export default About

