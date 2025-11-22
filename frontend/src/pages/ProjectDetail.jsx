import { useParams, useNavigate } from "react-router-dom";
import API_BASE_URL from "../config";
import { useCachedFetch } from "../hooks/useCachedFetch";
import FullScreenLoader from "../components/FullScreenLoader";
import "../ProjectDetail.css";

const ProjectDetail = ({ language }) => {
  const { slug } = useParams();
  const navigate = useNavigate();

  const {
    data: project,
    loading,
    error,
  } = useCachedFetch(
    `${API_BASE_URL}/entities/${slug}?lang=${language}`,
    `project_${slug}_${language}`
  );

  if (loading) return <FullScreenLoader message="Cargando proyecto..." />;

  if (error) {
    const isRateLimit = error === "RATELIMIT" || error === "ratelimit";
    return (
      <div className="project-detail-error">
        <h1>{isRateLimit ? "⏳ Demasiada velocidad" : "Project not found"}</h1>
        <p>
          {isRateLimit
            ? "Has hecho muchas peticiones. Por favor espera unos minutos."
            : "No pudimos encontrar el proyecto que buscas."}
        </p>
        <button className="pd-back-btn" onClick={() => navigate("/#job")}>
          {language === "es" ? "Volver" : "Back"}
        </button>
      </div>
    );
  }

  if (!project) return null;

  const t = project.current || {};
  const images =
    project.images ||
    [project.desktop_image, project.mobile_image].filter(Boolean);

  return (
    <div className="pd-wrapper">
      <nav className="pd-nav">
        <button className="pd-back-btn" onClick={() => navigate("/#job")}>
          ← {language === "es" ? "Volver" : "Back"}
        </button>
      </nav>

      <div className="pd-container">
        <header className="pd-header">
          <h1 className="pd-title">{t.title}</h1>
          {t.subtitle && <p className="pd-subtitle">{t.subtitle}</p>}
        </header>

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
              {project.tags?.map((tag, i) => (
                <span key={i} className="pd-tag">
                  {tag}
                </span>
              ))}
            </div>
            {project.url && (
              <a
                href={project.url}
                target="_blank"
                rel="noreferrer"
                className="pd-cta-btn"
              >
                Live Demo ↗
              </a>
            )}
          </aside>

          <article
            className="pd-description"
            dangerouslySetInnerHTML={{ __html: t.description }}
          />
        </div>
      </div>
    </div>
  );
};

export default ProjectDetail;
