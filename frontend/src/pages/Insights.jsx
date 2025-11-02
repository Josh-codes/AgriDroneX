import React, { useState } from 'react'
import './Insights.css'
import ChatButton from '../components/ChatButton'

const Insights = () => {
  const [expandedIndex, setExpandedIndex] = useState(null)

  const faqs = [
    {
      question: "What is precision agriculture and how do drones help?",
      answer: "Precision agriculture uses technology to optimize field-level management with regard to crop farming. Drones provide aerial imagery, multispectral analysis, and real-time monitoring to help farmers make data-driven decisions."
    },
    {
      question: "How often should I conduct drone surveys of my fields?",
      answer: "For optimal results, we recommend weekly surveys during the growing season. This frequency allows for early detection of issues like disease, pests, or irrigation problems before they become widespread."
    },
    {
      question: "What data do I receive from a drone survey?",
      answer: "You'll receive high-resolution imagery, crop health maps using NDVI (Normalized Difference Vegetation Index), field boundaries, growth analysis, and actionable insights with recommendations."
    },
    {
      question: "Can drones detect crop diseases before they're visible?",
      answer: "Yes! Multispectral imaging can detect plant stress indicators days or even weeks before visible symptoms appear, allowing for early intervention and treatment."
    },
    {
      question: "How accurate is drone data compared to traditional methods?",
      answer: "Drone data provides centimeter-level accuracy and can cover entire fields in minutes. Traditional ground surveys are limited by time and may miss patterns only visible from above."
    },
    {
      question: "What's the ROI timeline for implementing drone technology?",
      answer: "Most farmers see ROI within the first growing season through reduced input costs, increased yields, and early problem detection. Average yield increases range from 15-35%."
    },
    {
      question: "Do I need special training to use drone data?",
      answer: "No special training required! Our platform presents data in easy-to-understand formats with clear recommendations. We also provide onboarding support and regular check-ins."
    },
    {
      question: "How does weather affect drone operations?",
      answer: "Drones can operate in moderate weather conditions but flights are limited during high winds (>25 mph), heavy rain, or severe storms. We monitor weather and reschedule when necessary."
    },
    {
      question: "Can drones be used for precision spraying?",
      answer: "Yes, equipped with spray systems, drones can target specific areas, reducing chemical usage by up to 90% compared to traditional methods while minimizing environmental impact."
    },
    {
      question: "Is my data secure and private?",
      answer: "Absolutely. All farm data is encrypted, stored securely, and never shared with third parties. You maintain complete ownership and control of your information."
    }
  ]

  const toggleFAQ = (index) => {
    setExpandedIndex(expandedIndex === index ? null : index)
  }

  return (
    <div className="insights-page">
      <div className="insights-container">
        <h1 className="insights-title">Frequently Asked Questions</h1>
        <div className="faq-list">
          {faqs.map((faq, index) => (
            <div 
              key={index} 
              className={`faq-item ${expandedIndex === index ? 'expanded' : ''}`}
              onClick={() => toggleFAQ(index)}
            >
              <div className="faq-question">
                <span>{faq.question}</span>
                <span className="faq-caret">▼</span>
              </div>
              {expandedIndex === index && (
                <div className="faq-answer">
                  <p>{faq.answer}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
      <ChatButton />
    </div>
  )
}

export default Insights

