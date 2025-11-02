import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [projects, setProjects] = useState([])
  const [language, setLanguage] = useState('es')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Fetch projects from API
    fetch(`/api/entities?lang=${language}`)
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

  const toggleLanguage = () => {
    setLanguage(lang => lang === 'es' ? 'en' : 'es')
  }

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  return (
    <div className="App">
      <header>
        <h1>Rafael Ortiz</h1>
        <button onClick={toggleLanguage} className="lang-toggle">
          {language === 'es' ? 'EN' : 'ES'}
        </button>
      </header>

      <main>
        <section className="hero">
          <h2>{language === 'es' ? 'Portafolio' : 'Portfolio'}</h2>
          <p>{language === 'es' ? 'Proyectos y experiencia' : 'Projects and experience'}</p>
        </section>

        <section className="projects">
          {projects.map(project => (
            <article key={project.id} className="project-card">
              {project.category && (
                <span className="category">{project.category}</span>
              )}
              <h3>{project.title}</h3>
              <p className="subtitle">{project.subtitle}</p>
              <div 
                className="description" 
                dangerouslySetInnerHTML={{ __html: project.description }}
              />
              
              {project.tags && project.tags.length > 0 && (
                <div className="tags">
                  {project.tags.map((tag, idx) => (
                    <span key={idx} className="tag">{tag}</span>
                  ))}
                </div>
              )}
            </article>
          ))}
        </section>
      </main>

      <footer>
        <p>© 2025 Rafael Ortiz</p>
      </footer>
    </div>
  )
}

export default App

