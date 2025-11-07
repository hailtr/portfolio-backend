import { useState, useEffect } from 'react'
import API_BASE_URL from '../config'

const ProfileSection = ({ language }) => {
  const [profile, setProfile] = useState({
    name: 'Rafael Ortiz',
    role: 'Data Engineer',
    tagline: 'Transforming data into strategic decisions',
    location: { city: 'Caracas', country: 'Venezuela' }
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Fetch profile from API
    fetch(`${API_BASE_URL}/profile?lang=${language}`)
      .then(res => res.json())
      .then(data => {
        setProfile(data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching profile:', err)
        setLoading(false)
      })
  }, [language])

  if (loading) {
    return null // or a skeleton loader
  }

  return (
    <section className="section">
      <div className="home-section" id="home">
        <div className="profile">
          <div className="profile-picture-wrapper">
            <img 
              src="/images/profilepicture.jpg" 
              alt="Foto personal" 
              className="profile-picture"
            />
          </div>
          <div className="profile-greating">
            <h2>
              <span className="name">{profile.name.split(' ')[0]}</span> {profile.name.split(' ')[1]}
            </h2>
            <h1>{profile.role}</h1>
            <p className="tagline">{profile.tagline}</p>
            <p>
              <span className="country-before">Santiago de Chile, Chile</span>
              <span className="country-after"> {profile.location?.city}, {profile.location?.country}</span>
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}

export default ProfileSection

