const ProjectCard = ({ project, isExpanded, onToggle, language }) => {
  return (
    <div 
      className={`job-card glass round-border ${isExpanded ? 'expanded' : ''}`}
      onClick={!isExpanded ? onToggle : undefined}
    >
      {isExpanded && (
        <button className="job-close" onClick={onToggle}>
          ✕
        </button>
      )}

      <div className="job-card-image-container">
        {project.desktop_image && (
          <img 
            src={project.desktop_image} 
            alt={`${project.title} desktop`}
            className="job-image-desktop"
          />
        )}
        {project.mobile_image && (
          <img 
            src={project.mobile_image} 
            alt={`${project.title} mobile`}
            className="job-image-mobile"
          />
        )}
      </div>

      <div className="job-card-content">
        <h3>{project.title}</h3>
        {project.subtitle && <h4>{project.subtitle}</h4>}
        
        <div className="job-description">
          <div dangerouslySetInnerHTML={{ __html: project.description }} />
        </div>

        {isExpanded && project.tags && project.tags.length > 0 && (
          <div className="job-tags">
            {project.tags.map((tag, idx) => (
              <span key={idx} className="relative-skill">
                {tag}
              </span>
            ))}
          </div>
        )}

        {isExpanded && project.url && (
          <div className="job-tags">
            <a 
              href={project.url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="relative-skill"
            >
              {language === 'es' ? 'Ver proyecto' : 'View project'} →
            </a>
          </div>
        )}
      </div>
    </div>
  )
}

export default ProjectCard

