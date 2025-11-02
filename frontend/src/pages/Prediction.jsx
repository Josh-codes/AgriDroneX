import React, { useState } from 'react'
import axios from 'axios'
import './Prediction.css'
import ChatButton from '../components/ChatButton'

const Prediction = () => {
  const [selectedFile, setSelectedFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      setSelectedFile(file)
      setError(null)
      setResult(null)
      
      // Create preview
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreview(reader.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!selectedFile) {
      setError('Please select an image file')
      return
    }

    setLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append('image', selectedFile)

    try {
      const response = await axios.post('/api/predict/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to process image. Please try again.')
      console.error('Prediction error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="prediction-page">
      <div className="prediction-container">
        <h1 className="prediction-title">Crop Disease Detection</h1>
        <p className="prediction-subtitle">
          Upload an image of your crop to analyze for diseases and get detailed insights
        </p>

        <form onSubmit={handleSubmit} className="prediction-form">
          <div className="upload-section">
            <div className="upload-area">
              {preview ? (
                <div className="preview-container">
                  <img src={preview} alt="Preview" className="preview-image" />
                  <button
                    type="button"
                    className="remove-image"
                    onClick={() => {
                      setSelectedFile(null)
                      setPreview(null)
                    }}
                  >
                    ×
                  </button>
                </div>
              ) : (
                <>
                  <input
                    type="file"
                    id="image-upload"
                    accept="image/*"
                    onChange={handleFileChange}
                    className="file-input"
                  />
                  <label htmlFor="image-upload" className="upload-label">
                    <div className="upload-icon">📷</div>
                    <p>Click to upload or drag and drop</p>
                    <p className="upload-hint">PNG, JPG, JPEG up to 10MB</p>
                  </label>
                </>
              )}
            </div>
          </div>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <button
            type="submit"
            className="predict-button"
            disabled={!selectedFile || loading}
          >
            {loading ? 'Analyzing...' : 'Analyze Image'}
          </button>
        </form>

        {result && (
          <div className="result-section">
            <h2 className="result-title">Analysis Results</h2>
            <div className="result-card">
              <div className="result-header">
                <span className="result-label">Prediction:</span>
                <span className={`result-value ${result.is_blight ? 'blight' : 'healthy'}`}>
                  {result.label || (result.is_blight ? 'Blight Detected' : 'No Blight')}
                </span>
              </div>
              
              <div className="result-details">
                <div className="detail-item">
                  <span className="detail-label">Method:</span>
                  <span className="detail-value">{result.method || 'model'}</span>
                </div>
                
                {result.prob !== undefined && (
                  <div className="detail-item">
                    <span className="detail-label">Confidence:</span>
                    <span className="detail-value">
                      {(result.prob * 100).toFixed(1)}%
                    </span>
                  </div>
                )}
                
                {result.score !== undefined && (
                  <div className="detail-item">
                    <span className="detail-label">Score:</span>
                    <span className="detail-value">
                      {(result.score * 100).toFixed(1)}%
                    </span>
                  </div>
                )}
              </div>

              {result.is_blight && (
                <div className="recommendations">
                  <h3>Recommendations:</h3>
                  <ul>
                    <li>Isolate affected plants immediately</li>
                    <li>Apply appropriate fungicide treatment</li>
                    <li>Improve air circulation around crops</li>
                    <li>Monitor weather conditions (high humidity favors blight)</li>
                    <li>Consider crop rotation for next season</li>
                    <li>Remove and dispose of severely affected plant parts</li>
                  </ul>
                </div>
              )}

              {!result.is_blight && (
                <div className="recommendations healthy">
                  <h3>Status:</h3>
                  <p>Your crop appears healthy! Continue monitoring regularly for early detection of any issues.</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
      <ChatButton />
    </div>
  )
}

export default Prediction

