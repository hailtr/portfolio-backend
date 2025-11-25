import { memo } from "react";
import { getIconConfig } from "../utils/iconUtils";

const SkillsTree = memo(({ language }) => {
  const translations = {
    es: {
      languages: "Lenguajes",
      dataTools: "Herramientas de Datos",
      webStack: "Stack Web",
      cloudInfra: "Cloud & Infraestructura",
      methodologies: "Metodologías",
    },
    en: {
      languages: "Languages",
      dataTools: "Data Tools",
      webStack: "Web Stack",
      cloudInfra: "Cloud & Infrastructure",
      methodologies: "Methodologies",
    },
  };

  const t = translations[language] || translations.es;

  // Skills configuration - icons are resolved automatically via iconUtils
  const skills = {
    languages: [
      { name: "Python" },
      { name: "SQL" },
      { name: "R" },
      { name: "JavaScript" },
      { name: "Java" },
    ],

    dataTools: [
      // Análisis
      { name: "Pandas" },
      { name: "NumPy" },
      { name: "DAX", description: "Power BI formulas" },

      // Visualización
      { name: "Power BI" },
      { name: "Tableau" },
      { name: "Excel" },

      // ML/AI
      { name: "TensorFlow" },
      { name: "Scikit-learn" },

      // Bases de Datos
      { name: "PostgreSQL" },
      { name: "MongoDB" },
      { name: "Supabase" },
    ],

    webStack: [
      { name: "React" },
      { name: "Flask" },
      { name: "Django" },
      { name: "HTML" },
      { name: "CSS" },
    ],

    cloudInfra: [
      { name: "Docker" },
      { name: "Azure" },
      { name: "Kubernetes" },
      { name: "Google Cloud" },
    ],

    methodologies: [
      { name: "Git" },
      { name: "MLOps" },
      { name: "Data Modeling" },
      { name: "Agile" },
    ],
  };

  const renderSkill = (skill, key) => {
    const iconConfig = getIconConfig(skill.name, skill.filter);

    return (
      <div key={key} className="skill-tree-skill">
        {/* Render inline SVG if available, otherwise use img tag */}
        {iconConfig.inlineSvg ? (
          <div
            className={`skill-logo ${iconConfig.filter}`}
            dangerouslySetInnerHTML={{ __html: iconConfig.inlineSvg }}
            style={{
              width: "25px",
              height: "25px",
              display: "inline-block",
              lineHeight: 0,
            }}
          />
        ) : iconConfig.url ? (
          <img
            className={`skill-logo ${iconConfig.filter || "filter-white"}`}
            src={iconConfig.url}
            alt={`Logo ${skill.name}`}
            height="25"
            width="25"
            loading="lazy"
            onError={(e) => {
              e.target.style.display = "none";
              console.warn(`Icon not found for: ${skill.name}`);
            }}
          />
        ) : null}
        <p>{skill.name}</p>
      </div>
    );
  };

  const categories = [
    { key: "languages", skills: skills.languages, title: t.languages },
    { key: "dataTools", skills: skills.dataTools, title: t.dataTools },
    { key: "webStack", skills: skills.webStack, title: t.webStack },
    { key: "cloudInfra", skills: skills.cloudInfra, title: t.cloudInfra },
    {
      key: "methodologies",
      skills: skills.methodologies,
      title: t.methodologies,
    },
  ];

  return (
    <div className="skills-container">
      {categories.map((category, idx) => (
        <div
          key={category.key}
          className="skill-category glass animated-glass round-border"
          style={{ animationDelay: `${idx * 0.1}s` }}
        >
          <h3 className="skill-category-title">{category.title}</h3>
          <div className="skill-category-items">
            {category.skills.map((skill) => renderSkill(skill, skill.name))}
          </div>
        </div>
      ))}
    </div>
  );
});

SkillsTree.displayName = 'SkillsTree';

export default SkillsTree;
