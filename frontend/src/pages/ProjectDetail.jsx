import { useParams, useNavigate } from 'react-router-dom'
import API_BASE_URL from '../config'
import { useCachedFetch } from '../hooks/useCachedFetch' // <--- IMPORTANTE
import FullScreenLoader from '../components/FullScreenLoader' // <--- IMPORTANTE
import '../ProjectDetail.css'

const ProjectDetail = ({ language }) => {
  const { slug } = useParams()
  const navigate = useNavigate()

  const { data: project, loading, error } = useCachedFetch(
    `${API_BASE_URL}/entities/${slug}?lang=${language}`, 
    `project_${slug}_${language}` // Clave única para el caché
  )

  if (loading) return <FullScreenLoader message="Cargando proyecto..." />

  if (error === "RATELIMIT") {
    return (
      <div className="pd-error">
        <h1>Demasiadas peticiones</h1>
        <p>El servidor está descansando. Intenta de nuevo en unos minutos.</p>
        <button className="pd-back-btn" onClick={() => navigate('/#job')}>Volver</button>
      </div>
    )
  }

  if (error || !project) {
    return <div className="pd-error">Proyect not found</div>
  }

  // --- RENDERIZADO ---

  if (loading) {
    return (
      <div className="pd-loading">
        <div className="spinner"></div>
        <p style={{marginTop: '1rem', color: '#fff'}}>Cargando proyecto...</p>
      </div>
    )
  }

  // UI para cuando te banean por Rate Limit
  if (error === "ratelimit") {
    return (
      <div className="pd-error">
        <h1>⏳ Demasiada velocidad</h1>
        <p>Has hecho muchas peticiones. Por favor espera unos minutos.</p>
        <button className="pd-back-btn" onClick={() => navigate('/#job')}>Volver al inicio</button>
      </div>
    )
  }

  if (error || !project) {
    return (
      <div className="pd-error">
        <h1>Project not found</h1>
        <button className="pd-back-btn" onClick={() => navigate('/#job')}>Volver</button>
      </div>
    )
  }

  // ... (El resto de tu renderizado normal sigue igual)
  const t = project.current || {}
  const images = project.images || [project.desktop_image, project.mobile_image].filter(Boolean)

  return (
     <div className="pd-wrapper">
        {/* ... todo tu JSX de contenido ... */}
        <nav className="pd-nav">
            <button className="pd-back-btn" onClick={() => navigate('/#job')}>
            ← {language === 'es' ? 'Volver' : 'Back'}
            </button>
        </nav>

        <div className="pd-container">
            <header className="pd-header">
            <h1 className="pd-title">{t.title}</h1>
            {t.subtitle && <p className="pd-subtitle">{t.subtitle}</p>}
            </header>

            {/* Galería */}
            {images.length > 0 && (
            <div className="pd-gallery">
                {images.map((img, idx) => (
                <div key={idx} className="pd-image-frame">
                    <img src={img} alt={`Screenshot ${idx}`} />
                </div>
                ))}
            </div>
            )}

            <div className="pd-content-grid">
            <aside className="pd-sidebar">
                <h3>Stack</h3>
                <div className="pd-tags">
                {project.tags?.map((tag, i) => <span key={i} className="pd-tag">{tag}</span>)}
                </div>
                {project.url && (
                <a href={project.url} target="_blank" rel="noreferrer" className="pd-cta-btn">
                    Live Demo ↗
                </a>
                )}
            </aside>

            <article className="pd-description" dangerouslySetInnerHTML={{ __html: t.description }} />
            </div>
        </div>
     </div>
  )
}

export default ProjectDetail