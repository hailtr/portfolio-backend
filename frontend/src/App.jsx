import { useState, useEffect } from 'react'
import Navbar from './components/Navbar'
import ProfileSection from './components/ProfileSection'
import ProjectsSection from './components/ProjectsSection'
import AboutSection from './components/AboutSection'
import Footer from './components/Footer'
import Loader from './components/Loader'
import ContactOverlay from './components/ContactOverlay'
import BackgroundShapes from './components/BackgroundShapes'
import API_BASE_URL from './config'
import './App.css'

function App() {
  const [language, setLanguage] = useState('es')
  const [loading, setLoading] = useState(true)
  const [projects, setProjects] = useState([])
  const [showContact, setShowContact] = useState(false)

  useEffect(() => {
    // Fetch projects from API and wait for them
    setLoading(true)
    fetch(`${API_BASE_URL}/entities?lang=${language}`)
      .then(res => res.json())
      .then(data => {
        setProjects(data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching projects:', err)
        setLoading(false)
      })
  }, [language])

  // Add scroll reveal animation
  useEffect(() => {
    if (loading) return

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible')
          }
        })
      },
      { threshold: 0.1 }
    )

    document.querySelectorAll('.reveal-section').forEach((el) => {
      observer.observe(el)
    })

    return () => observer.disconnect()
  }, [loading])

  const toggleLanguage = () => {
    setLanguage(lang => lang === 'es' ? 'en' : 'es')
  }

  const toggleContact = () => {
    setShowContact(!showContact)
  }

  if (loading) {
    return <Loader language={language} />
  }

  return (
    <div className="App">
      <BackgroundShapes />
      <Navbar 
        language={language} 
        toggleLanguage={toggleLanguage}
        toggleContact={toggleContact}
      />
      
      <main className="visible">
        <ProfileSection language={language} />
        <ProjectsSection language={language} projects={projects} />
        <AboutSection language={language} />
      </main>

      <Footer language={language} />
      <ContactOverlay 
        show={showContact} 
        onClose={() => setShowContact(false)}
        language={language}
      />
    </div>
  )
}

export default App
