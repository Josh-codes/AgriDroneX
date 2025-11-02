import React, { useState, useEffect } from 'react'
import { MapContainer, TileLayer, Marker, useMapEvents } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import './MapSelector.css'

// Fix for default marker icon in Webpack/Vite
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'

delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
})

function LocationMarker({ position, setPosition, setLocationName }) {
  useMapEvents({
    click(e) {
      const newPosition = [e.latlng.lat, e.latlng.lng]
      setPosition(newPosition)
      
      // Reverse geocoding to get location name
      fetch(`https://nominatim.openstreetmap.org/reverse?lat=${e.latlng.lat}&lon=${e.latlng.lng}&format=json`)
        .then(res => res.json())
        .then(data => {
          setLocationName(data.display_name)
        })
        .catch(err => console.error('Error getting location name:', err))
    },
  })

  return position ? <Marker position={position} /> : null
}

const MapSelector = ({ onLocationSelect, initialPosition = [19.0760, 72.8777] }) => {
  const [position, setPosition] = useState(initialPosition)
  const [locationName, setLocationName] = useState('')
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    if (position && locationName) {
      onLocationSelect({
        latitude: position[0],
        longitude: position[1],
        locationName: locationName
      })
    }
  }, [position, locationName, onLocationSelect])

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!searchQuery.trim()) return

    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(searchQuery)}&format=json&limit=1`
      )
      const data = await response.json()
      
      if (data && data.length > 0) {
        const newPosition = [parseFloat(data[0].lat), parseFloat(data[0].lon)]
        setPosition(newPosition)
        setLocationName(data[0].display_name)
      } else {
        alert('Location not found')
      }
    } catch (error) {
      console.error('Error searching location:', error)
      alert('Error searching location')
    }
  }

  return (
    <div className="map-selector">
      <form className="map-search-form" onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Search for a location..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="map-search-input"
        />
        <button type="submit" className="map-search-btn">Search</button>
      </form>
      
      {locationName && (
        <div className="selected-location">
          <strong>Selected:</strong> {locationName}
          <br />
          <small>Lat: {position[0].toFixed(6)}, Lng: {position[1].toFixed(6)}</small>
        </div>
      )}
      
      <div className="map-container-wrapper">
        <MapContainer 
          center={position} 
          zoom={13} 
          style={{ height: '400px', width: '100%', borderRadius: '8px' }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <LocationMarker 
            position={position} 
            setPosition={setPosition}
            setLocationName={setLocationName}
          />
        </MapContainer>
      </div>
      
      <p className="map-instruction">
        <i>Click on the map to select a location or search above</i>
      </p>
    </div>
  )
}

export default MapSelector
