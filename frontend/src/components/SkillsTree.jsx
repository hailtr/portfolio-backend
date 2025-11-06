import { getIconConfig } from '../utils/iconUtils'

const SkillsTree = ({ language }) => {
  const translations = {
    es: {
      languages: 'Lenguajes',
      dataTools: 'Herramientas de Datos', 
      webStack: 'Stack Web',
      cloudInfra: 'Cloud & Infraestructura',
      methodologies: 'Metodologías'
    },
    en: {
      languages: 'Languages',
      dataTools: 'Data Tools',
      webStack: 'Web Stack', 
      cloudInfra: 'Cloud & Infrastructure',
      methodologies: 'Methodologies'
    }
  }

  const t = translations[language] || translations.es

  // Skills configuration - icons are resolved automatically via iconUtils
  const skills = {
    languages: [
      { name: 'Python', roles: ['data_analyst', 'ml_engineer', 'data_engineer'] },
      { name: 'SQL', roles: ['data_analyst', 'ml_engineer', 'data_engineer'] },
      { name: 'R', roles: ['data_analyst', 'ml_engineer'] },
      { name: 'JavaScript', roles: ['data_analyst', 'ml_engineer', 'data_engineer'] },
      { name: 'Java', roles: ['mobileDev'] }
    ],
    
    dataTools: [
      // Análisis
      { name: 'Pandas', roles: ['data_analyst', 'ml_engineer'] },
      { name: 'NumPy', roles: ['data_analyst', 'ml_engineer'] },
      { name: 'DAX', roles: ['data_analyst'], description: 'Power BI formulas' },
      
      // Visualización
      { name: 'Power BI', roles: ['data_analyst'] },
      { name: 'Tableau', roles: ['data_analyst'] },
      { name: 'Excel', roles: ['data_analyst'] },
      
      // ML/AI
      { name: 'TensorFlow', roles: ['ml_engineer'] },
      { name: 'Scikit-learn', roles: ['ml_engineer'] },
      
      // Bases de Datos
      { name: 'PostgreSQL', roles: ['data_engineer', 'ml_engineer'] },
      { name: 'MongoDB', roles: ['data_engineer'] },
      { name: 'Supabase', roles: ['data_engineer'] }
    ],
    
    webStack: [
      { name: 'React', roles: ['data_analyst', 'ml_engineer', 'data_engineer'] },
      { name: 'Flask', roles: ['ml_engineer', 'data_engineer'] },
      { name: 'Django', roles: ['data_engineer'] },
      { name: 'HTML', roles: ['data_analyst', 'ml_engineer', 'data_engineer'] },
      { name: 'CSS', roles: ['data_analyst', 'ml_engineer', 'data_engineer'] }
    ],
    
    cloudInfra: [
      { name: 'Docker', roles: ['ml_engineer', 'data_engineer'] },
      { name: 'Azure', roles: ['data_engineer', 'ml_engineer'] },
      { name: 'Kubernetes', roles: ['data_engineer'] },
      { name: 'Google Cloud', roles: ['data_engineer', 'ml_engineer'] }
    ],
    
    methodologies: [
      { name: 'Git', roles: ['data_analyst', 'ml_engineer', 'data_engineer'] },
      { name: 'MLOps', roles: ['ml_engineer'] },
      { name: 'Data Modeling', roles: ['data_engineer', 'data_analyst'] },
      { name: 'Agile', roles: ['data_analyst', 'ml_engineer', 'data_engineer'] }
    ]
  }

  const renderSkill = (skill, key) => {
    const iconConfig = getIconConfig(skill.name, skill.filter)
    
    return (
      <div 
        key={key}
        className="skill-tree-skill"
      >
        {/* Render inline SVG if available, otherwise use img tag */}
        {iconConfig.inlineSvg ? (
          <div 
            className={`skill-logo ${iconConfig.filter}`}
            dangerouslySetInnerHTML={{ __html: iconConfig.inlineSvg }}
            style={{ 
              width: '25px', 
              height: '25px', 
              display: 'inline-block',
              lineHeight: 0
            }}
          />
        ) : iconConfig.url ? (
          <img 
            className={`skill-logo ${iconConfig.filter || 'filter-white'}`}
            src={iconConfig.url} 
            alt={`Logo ${skill.name}`}
            height="25" 
            width="25"
            loading="lazy"
            onError={(e) => {
              e.target.style.display = 'none'
              console.warn(`Icon not found for: ${skill.name}`)
            }}
          />
        ) : null}
        <p>{skill.name}</p>
      </div>
    )
  }

  const categories = [
    { key: 'languages', skills: skills.languages, title: t.languages },
    { key: 'dataTools', skills: skills.dataTools, title: t.dataTools },
    { key: 'webStack', skills: skills.webStack, title: t.webStack },
    { key: 'cloudInfra', skills: skills.cloudInfra, title: t.cloudInfra },
    { key: 'methodologies', skills: skills.methodologies, title: t.methodologies }
  ]

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
            {category.skills.map(skill => renderSkill(skill, skill.name))}
          </div>
        </div>
      ))}
    </div>
  )
}

export default SkillsTree
