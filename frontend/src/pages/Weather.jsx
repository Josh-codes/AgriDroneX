import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './Weather.css'
import ChatButton from '../components/ChatButton'
import MapSelector from '../components/MapSelector'

const Weather = () => {
  const [farms, setFarms] = useState([])
  const [selectedFarm, setSelectedFarm] = useState(null)
  const [weatherData, setWeatherData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    location_name: '',
    latitude: '',
    longitude: '',
    crop: ''
  })
  const [crops, setCrops] = useState([])

  useEffect(() => {
    fetchFarms()
    fetchCrops()
  }, [])

  const fetchCrops = async () => {
    try {
      const response = await axios.get('/api/crops/')
      setCrops(response.data)
    } catch (error) {
      console.error('Error fetching crops:', error)
    }
  }

  const fetchFarms = async () => {
    try {
      const response = await axios.get('/api/farms/')
      setFarms(response.data)
    } catch (error) {
      console.error('Error fetching farms:', error)
    }
  }

  const fetchWeather = async (farmId) => {
    setLoading(true)
    try {
      const response = await axios.get(`/api/farms/${farmId}/weather/`)
      setWeatherData(response.data)
      setSelectedFarm(farmId)
    } catch (error) {
      console.error('Error fetching weather:', error)
      alert('Failed to fetch weather data')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateFarm = async (e) => {
    e.preventDefault()
    
    // Validate that location is selected
    if (!formData.latitude || !formData.longitude) {
      alert('Please select a location on the map')
      return
    }
    
    try {
      await axios.post('/api/farms/', formData, {
        headers: {
          'Content-Type': 'application/json',
        }
      })
      setShowCreateForm(false)
      setFormData({ name: '', location_name: '', latitude: '', longitude: '', crop: '' })
      fetchFarms()
      alert('Farm created successfully!')
    } catch (error) {
      console.error('Error creating farm:', error)
      alert('Failed to create farm')
    }
  }

  const handleLocationSelect = (locationData) => {
    setFormData({
      ...formData,
      latitude: locationData.latitude,
      longitude: locationData.longitude,
      location_name: locationData.locationName
    })
  }

  const handleDeleteFarm = async (farmId) => {
    if (!window.confirm('Are you sure you want to delete this farm?')) return
    
    try {
      await axios.delete(`/api/farms/${farmId}/`)
      fetchFarms()
      if (selectedFarm === farmId) {
        setSelectedFarm(null)
        setWeatherData(null)
      }
    } catch (error) {
      console.error('Error deleting farm:', error)
      alert('Failed to delete farm')
    }
  }

  return (
    <div className="weather-page">
      <div className="weather-container">
        <h1 className="weather-title">Weather Dashboard</h1>
        <p className="weather-subtitle">Monitor weather conditions for your farms</p>

        <div className="weather-content">
          <div className="farms-sidebar">
            <div className="sidebar-header">
              <h2>Your Farms</h2>
              <button 
                className="add-farm-btn"
                onClick={() => setShowCreateForm(!showCreateForm)}
              >
                + Add Farm
              </button>
            </div>

            {showCreateForm && (
              <form className="create-farm-form" onSubmit={handleCreateFarm}>
                <input
                  type="text"
                  placeholder="Farm Name"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  required
                />
                
                <MapSelector 
                  onLocationSelect={handleLocationSelect}
                  initialPosition={[19.0760, 72.8777]}
                />
                
                {formData.location_name && (
                  <div className="location-info">
                    <strong>Location:</strong> {formData.location_name}
                  </div>
                )}
                
                <select
                  value={formData.crop}
                  onChange={(e) => setFormData({...formData, crop: e.target.value})}
                  required
                >
                  <option value="">Select Crop</option>
                  {crops.map(crop => (
                    <option key={crop.id} value={crop.id}>{crop.name}</option>
                  ))}
                </select>
                <div className="form-buttons">
                  <button type="submit" className="submit-btn">Create Farm</button>
                  <button type="button" onClick={() => setShowCreateForm(false)} className="cancel-btn">Cancel</button>
                </div>
              </form>
            )}

            <div className="farms-list">
              {farms.map(farm => (
                <div key={farm.id} className="farm-item">
                  <div className="farm-info">
                    <h3>{farm.name}</h3>
                    <p>{farm.location_name}</p>
                    {farm.crop && <span className="crop-badge">{farm.crop}</span>}
                  </div>
                  <div className="farm-actions">
                    <button 
                      className="view-weather-btn"
                      onClick={() => fetchWeather(farm.id)}
                      disabled={loading}
                    >
                      View Weather
                    </button>
                    <button 
                      className="delete-btn"
                      onClick={() => handleDeleteFarm(farm.id)}
                    >
                      ×
                    </button>
                  </div>
                </div>
              ))}
              {farms.length === 0 && (
                <p className="no-farms">No farms yet. Add your first farm above!</p>
              )}
            </div>
          </div>

          <div className="weather-main">
            {loading && <div className="loading">Loading weather data...</div>}
            {!loading && weatherData && (
              <div className="weather-display">
                <h2 className="weather-location">{weatherData.location}</h2>
                
                <div className="current-weather">
                  <div className="weather-icon">
                    {weatherData.current?.weather_condition === 'Clear' ? '☀️' :
                     weatherData.current?.weather_condition === 'Clouds' ? '☁️' :
                     weatherData.current?.weather_condition === 'Rain' ? '🌧️' : '🌤️'}
                  </div>
                  <div className="weather-temp">
                    <span className="temp-value">{Math.round(weatherData.current?.temperature || 0)}°</span>
                    <span className="temp-unit">C</span>
                  </div>
                  <div className="weather-description">
                    {weatherData.current?.weather_description || 'N/A'}
                  </div>
                </div>

                <div className="weather-details-grid">
                  <div className="detail-card">
                    <span className="detail-label">Feels Like</span>
                    <span className="detail-value">{Math.round(weatherData.current?.feels_like || 0)}°C</span>
                  </div>
                  <div className="detail-card">
                    <span className="detail-label">Humidity</span>
                    <span className="detail-value">{Math.round(weatherData.current?.humidity || 0)}%</span>
                  </div>
                  <div className="detail-card">
                    <span className="detail-label">Wind Speed</span>
                    <span className="detail-value">{Math.round(weatherData.current?.wind_speed || 0)} m/s</span>
                  </div>
                  <div className="detail-card">
                    <span className="detail-label">Pressure</span>
                    <span className="detail-value">{Math.round(weatherData.current?.pressure || 0)} hPa</span>
                  </div>
                </div>

                {weatherData.forecast && weatherData.forecast.length > 0 && (
                  <div className="forecast-section">
                    <h3>5-Day Forecast</h3>
                    <div className="forecast-grid">
                      {weatherData.forecast.slice(0, 5).map((day, index) => (
                        <div key={index} className="forecast-day">
                          <div className="forecast-date">
                            {new Date(day.timestamp).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })}
                          </div>
                          <div className="forecast-icon">
                            {day.weather_condition === 'Clear' ? '☀️' :
                             day.weather_condition === 'Clouds' ? '☁️' :
                             day.weather_condition === 'Rain' ? '🌧️' : '🌤️'}
                          </div>
                          <div className="forecast-temp">
                            {Math.round(day.temperature)}°C
                          </div>
                          <div className="forecast-desc">{day.weather_description}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {weatherData.insights && weatherData.insights.length > 0 && (
                  <div className="insights-section">
                    <h3>Farming Insights</h3>
                    <div className="insights-list">
                      {weatherData.insights.map((insight, index) => (
                        <div key={index} className="insight-card">
                          <span className={`insight-priority priority-${insight.priority}`}>
                            {insight.priority === 3 ? 'High' : insight.priority === 2 ? 'Medium' : 'Low'}
                          </span>
                          <h4>{insight.title}</h4>
                          <p>{insight.description}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
            {!loading && !weatherData && (
              <div className="no-weather">
                <p>Select a farm to view weather data</p>
              </div>
            )}
          </div>
        </div>
      </div>
      <ChatButton />
    </div>
  )
}

export default Weather
