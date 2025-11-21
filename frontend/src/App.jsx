import { useState, useEffect } from 'react'
import { Routes, Route, useLocation } from 'react-router-dom'
import Navbar from './components/Navbar'
import ProfileSection from './components/ProfileSection'
import ProjectsSection from './components/ProjectsSection'
import AboutSection from './components/AboutSection'
import Footer from './components/Footer'
import Loader from './components/Loader'
import ContactOverlay from './components/ContactOverlay'
import BackgroundShapes from './components/BackgroundShapes'
import ProjectDetail from './pages/ProjectDetail'
import API_BASE_URL from './config'
import { useCachedFetch } from './hooks/useCachedFetch' // <--- IMPORTANTE: Importar el hook
import './App.css'

function App() {
  const [language, setLanguage] = useState('es')
  const [showContact, setShowContact] = useState(false)
  const location = useLocation()

  // 1. REEMPLAZO DEL FETCH MANUAL POR EL HOOK CON CACHÉ
  // Esto carga los proyectos, pero revisa LocalStorage primero.
  const { 
    data: projectsData, 
    loading, 
    error 
  } = useCachedFetch(
    `${API_BASE_URL}/entities?lang=${language}&type=project`,
    `home_projects_${language}` // Clave única para guardar en caché
  )

  // Aseguramos que projects sea siempre un array para evitar crash en ProjectsSection
  const projects = projectsData || []

  // Scroll Reveal Animation (Mantenemos tu lógica, funciona con el loading del hook)
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

    // Pequeño timeout para asegurar que el DOM se pintó
    setTimeout(() => {
        document.querySelectorAll('.reveal-section').forEach((el) => {
            observer.observe(el)
        })
    }, 100)

    return () => observer.disconnect()
  }, [loading, location]) // Se ejecuta cuando termina de cargar

  const toggleLanguage = () => {
    setLanguage(lang => lang === 'es' ? 'en' : 'es')
  }

  const toggleContact = () => {
    setShowContact(!showContact)
  }

  // 2. MANEJO DE ERROR GLOBAL (RATE LIMIT)
  // Si te banean, mostramos esto en lugar de que la app explote
  if (error === "RATELIMIT" && location.pathname === '/') {
    return (
      <div style={{ 
        height: '100vh', 
        display: 'flex', 
        flexDirection: 'column',
        justifyContent: 'center', 
        alignItems: 'center',
        color: 'white',
        background: 'var(--main-darkblue)' 
      }}>
        <h1>Demasiada velocidad</h1>
        <p>Se han recibido demasiadas peticiones. Espera unos minutos.</p>
      </div>
    )
  }

  // 3. LOADER
  // Mantenemos tu lógica: Solo mostramos loader full screen si estamos en Home
  if (loading && location.pathname === '/') {
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
      
      <Routes>
        <Route path="/" element={
          <main className="visible">
            <ProfileSection language={language} />
            {/* Pasamos los proyectos cacheados */}
            <ProjectsSection language={language} projects={projects} />
            <AboutSection language={language} />
          </main>
        } />
        
        <Route path="/project/:slug" element={
          <main className="visible">
             {/* ProjectDetail usará su propio useCachedFetch internamente */}
            <ProjectDetail language={language} />
          </main>
        } />
      </Routes>

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