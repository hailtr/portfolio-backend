import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import API_BASE_URL from '../config'

const ProjectDetail = ({ language }) => {
  const { slug } = useParams()
  const navigate = useNavigate()
  const [project, setProject] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${API_BASE_URL}/entities/${slug}?lang=${language}`)
      .then(res => res.json())
      .then(data => {
        setProject(data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching project:', err)
        setLoading(false)
      })
  }, [slug, language])

  if (loading) {
    return (
      <div className="project-detail-loading">
        <div className="spinner"></div>
      </div>
    )
  }

  if (!project) {
    return (
      <div className="project-detail-error">
        <h1>Project not found</h1>
        <button onClick={() => navigate('/')}>Go back home</button>
      </div>
    )
  }

  const currentTranslation = project.current || {}

  return (
    <div className="project-detail-page">
      <button className="back-button" onClick={() => navigate('/#job')}>
        ← {language === 'es' ? 'Volver' : 'Back'}
      </button>

      <div className="project-detail-container">
        <div className="project-detail-header">
          <h1 className="project-detail-title">{currentTranslation.title}</h1>
          {currentTranslation.subtitle && (
            <h2 className="project-detail-subtitle">{currentTranslation.subtitle}</h2>
          )}
        </div>

        {/* Images */}
        {(project.desktop_image || project.mobile_image) && (
          <div className="project-detail-images">
            {project.desktop_image && (
              <div className="project-image-large">
                <img src={project.desktop_image} alt={`${currentTranslation.title} desktop`} />
              </div>
            )}
            {project.mobile_image && (
              <div className="project-image-mobile-view">
                <img src={project.mobile_image} alt={`${currentTranslation.title} mobile`} />
              </div>
            )}
          </div>
        )}

        {/* Description */}
        <div className="project-detail-content">
          <div 
            className="project-detail-description"
            dangerouslySetInnerHTML={{ __html: currentTranslation.description }}
          />
        </div>

        {/* Tags */}
        {project.tags && project.tags.length > 0 && (
          <div className="project-detail-tags">
            <h3>{language === 'es' ? 'Tecnologías' : 'Technologies'}</h3>
            <div className="tags-container">
              {project.tags.map((tag, idx) => (
                <span key={idx} className="relative-skill">
                  {tag}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Links - if you have URL field */}
        {project.url && (
          <div className="project-detail-links">
            <a 
              href={project.url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="project-link-button"
            >
              {language === 'es' ? 'Ver proyecto en vivo' : 'View live project'} →
            </a>
          </div>
        )}
      </div>
    </div>
  )
}

export default ProjectDetail

