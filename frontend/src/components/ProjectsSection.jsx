import { useState, useRef, useEffect } from 'react'
import ProjectCard from './ProjectCard'

const ProjectsSection = ({ language, projects }) => {
  const [filter, setFilter] = useState('all')
  const galleryRef = useRef(null)

  const translations = {
    es: {
      title: 'Proyectos',
      all: 'Todos',
      projects: 'Proyectos',
      jobs: 'Trabajos',
      learning: 'Aprendizaje'
    },
    en: {
      title: 'Projects',
      all: 'All',
      projects: 'Projects',
      jobs: 'Jobs',
      learning: 'Learning'
    }
  }

  const t = translations[language] || translations.es

  const filterMap = {
    all: 'all',
    projects: 'proyectos',
    jobs: 'trabajo',
    learning: 'aprendizaje'
  }

  const filteredProjects = filter === 'all' 
    ? projects 
    : projects.filter(p => p.category === filter)

  const handleScroll = (direction) => {
    if (galleryRef.current) {
      const scrollAmount = 400
      const newPosition = galleryRef.current.scrollLeft + (direction === 'next' ? scrollAmount : -scrollAmount)
      galleryRef.current.scrollTo({
        left: newPosition,
        behavior: 'smooth'
      })
    }
  }

  const handleFilterChange = (newFilter) => {
    setFilter(filterMap[newFilter] || newFilter)
  }

  useEffect(() => {
    const gallery = galleryRef.current
    if (!gallery) return

    const updateFades = () => {
      const leftFade = gallery.previousElementSibling?.previousElementSibling
      const rightFade = gallery.previousElementSibling

      if (leftFade && rightFade) {
        leftFade.classList.toggle('visible', gallery.scrollLeft > 10)
        rightFade.classList.toggle('visible', 
          gallery.scrollLeft < gallery.scrollWidth - gallery.clientWidth - 10
        )
      }
    }

    gallery.addEventListener('scroll', updateFades)
    updateFades()

    return () => gallery.removeEventListener('scroll', updateFades)
  }, [filteredProjects])

  return (
    <section className="section reveal-section">
      <div className="job-section">
        <div className="content-container">
          <h2 id="job">{t.title}</h2>
          <div className="experience-gallery-wrapper">
            <div className="experience-fade left"></div>
            <div className="experience-fade right"></div>
            
            <div className="job-header">
              <div className="experience-filters">
                <button 
                  data-filter="all"
                  className={`glass animated-glass round-border ${filter === 'all' ? 'active' : ''}`}
                  onClick={() => handleFilterChange('all')}
                >
                  {t.all}
                </button>
                <button 
                  data-filter="proyectos"
                  className={`glass animated-glass round-border ${filter === 'proyectos' ? 'active' : ''}`}
                  onClick={() => handleFilterChange('projects')}
                >
                  {t.projects}
                </button>
                <button 
                  data-filter="trabajo"
                  className={`glass animated-glass round-border ${filter === 'trabajo' ? 'active' : ''}`}
                  onClick={() => handleFilterChange('jobs')}
                >
                  {t.jobs}
                </button>
                <button 
                  data-filter="aprendizaje"
                  className={`glass animated-glass round-border ${filter === 'aprendizaje' ? 'active' : ''}`}
                  onClick={() => handleFilterChange('learning')}
                >
                  {t.learning}
                </button>
              </div>

            </div>

            <div className="experience-gallery" ref={galleryRef}>
              {filteredProjects.map((project) => (
                <ProjectCard
                  key={project.id}
                  project={project}
                  language={language}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default ProjectsSection

