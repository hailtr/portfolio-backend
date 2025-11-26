import { useNavigate } from "react-router-dom";
import { useState } from "react";

const ProjectCard = ({ project, language, debugExpanded }) => {
  const navigate = useNavigate();
  const [isHovered, setIsHovered] = useState(debugExpanded || false);

  const handleClick = () => {
    navigate(`/project/${project.slug}`);
  };

  // Strip HTML tags for plain text description
  const stripHtml = (html) => {
    const tmp = document.createElement("div");
    tmp.innerHTML = html;
    return tmp.textContent || tmp.innerText || "";
  };

  // Find featured image, fallback to first image, then desktop_image
  const featuredImage = project.images?.find(img => img.is_featured)?.url
    || project.images?.[0]?.url
    || project.desktop_image
    || "/placeholder.jpg";

  return (
    <div
      className={`job-card ${debugExpanded ? "debug-expanded" : ""}`}
      onClick={handleClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => !debugExpanded && setIsHovered(false)}
    >
      <div className="job-card-inner">
        <div className="job-card-media-container">
          {isHovered && project.preview_video ? (
            <video
              src={project.preview_video}
              className="job-media-preview"
              autoPlay
              loop
              muted
              playsInline
            />
          ) : (
            <img
              src={featuredImage}
              alt={project.title}
              className="job-media-preview"
              onError={(e) => {
                e.target.src = "/placeholder.jpg";
              }}
            />
          )}
        </div>

        <div className="job-card-hover-info">
          <h3>{project.title}</h3>
          {project.subtitle && <h4>{project.subtitle}</h4>}

          {project.description && (
            <div className="job-card-hover-description">
              {stripHtml(project.description)}
            </div>
          )}

          {project.tags && project.tags.length > 0 && (
            <div className="job-tags-preview">
              {project.tags.slice(0, 5).map((tag, idx) => (
                <span key={idx} className="relative-skill-small">
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProjectCard;
