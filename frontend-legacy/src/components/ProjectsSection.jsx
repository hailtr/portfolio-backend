import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import ProjectCard from "./ProjectCard";

const ProjectsSection = ({ language, projects }) => {
  const [filter, setFilter] = useState("all");
  const [visibleCount, setVisibleCount] = useState(6);

  const translations = {
    es: {
      title: "Proyectos",
      all: "Todos",
      projects: "Proyectos",
      jobs: "Trabajos",
      learning: "Aprendizaje",
      loadMore: "Ver más proyectos",
    },
    en: {
      title: "Projects",
      all: "All",
      projects: "Projects",
      jobs: "Jobs",
      learning: "Learning",
      loadMore: "Load more projects",
    },
  };

  const t = translations[language] || translations.es;

  const filterMap = {
    all: "all",
    projects: "project",
    jobs: "work",
    learning: "study",
  };

  const filteredProjects =
    filter === "all" ? projects : projects.filter((p) => p.category === filter);

  const visibleProjects = filteredProjects.slice(0, visibleCount);

  const handleFilterChange = (newFilter) => {
    setFilter(filterMap[newFilter] || newFilter);
    setVisibleCount(6); // Reset visible count on filter change
  };

  const handleLoadMore = () => {
    setVisibleCount((prev) => prev + 6);
  };

  return (
    <section className="section reveal-section">
      <div className="job-section">
        <div className="content-container">
          <h2 id="job">{t.title}</h2>
          <div className="experience-gallery-wrapper">
            <div className="job-header">
              <div className="experience-filters">
                <button
                  data-filter="all"
                  className={`glass animated-glass round-border ${filter === "all" ? "active" : ""}`}
                  onClick={() => handleFilterChange("all")}
                >
                  {t.all}
                </button>
                <button
                  data-filter="project"
                  className={`glass animated-glass round-border ${filter === "project" ? "active" : ""}`}
                  onClick={() => handleFilterChange("projects")}
                >
                  {t.projects}
                </button>
                <button
                  data-filter="work"
                  className={`glass animated-glass round-border ${filter === "work" ? "active" : ""}`}
                  onClick={() => handleFilterChange("jobs")}
                >
                  {t.jobs}
                </button>
                <button
                  data-filter="study"
                  className={`glass animated-glass round-border ${filter === "study" ? "active" : ""}`}
                  onClick={() => handleFilterChange("learning")}
                >
                  {t.learning}
                </button>
              </div>
            </div>

            <motion.div
              key={filter} // Force re-mount when filter changes
              className="experience-gallery"
              initial="hidden"
              animate="visible"
              variants={{
                hidden: { opacity: 0 }, // Parent needs actual animation property
                visible: {
                  opacity: 1, // This triggers the state change
                  transition: {
                    staggerChildren: 0.1,
                    duration: 0.2, // Quick fade for parent
                  },
                },
              }}
            >
              {visibleProjects.map((project) => (
                <motion.div
                  key={project.id}
                  variants={{
                    hidden: { opacity: 0, scale: 0.9, y: 20 },
                    visible: { opacity: 1, scale: 1, y: 0 },
                  }}
                  transition={{ duration: 0.4 }}
                >
                  <ProjectCard project={project} language={language} />
                </motion.div>
              ))}
            </motion.div>

            {visibleCount < filteredProjects.length && (
              <div style={{ textAlign: "center", marginTop: "2rem" }}>
                <button
                  className="download-curriculum"
                  onClick={handleLoadMore}
                >
                  {t.loadMore}
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
};

export default ProjectsSection;
