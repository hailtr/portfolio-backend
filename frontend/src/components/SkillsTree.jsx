const SkillsTree = ({ language }) => {
  const translations = {
    es: {
      programming: 'Programación',
      databases: 'Bases de Datos',
      dataViz: 'Visualización de Datos',
      webDev: 'Desarrollo Web',
      mobileDev: 'Desarrollo Móvil',
      infrastructure: 'Infraestructura'
    },
    en: {
      programming: 'Programming',
      databases: 'Databases',
      dataViz: 'Data Visualization',
      webDev: 'Web Development',
      mobileDev: 'Mobile Development',
      infrastructure: 'Infrastructure'
    }
  }

  const t = translations[language] || translations.es

  const skills = {
    programming: [
      { name: 'Python', logo: './svg/python.svg' },
      { name: 'Java', logo: './svg/java.svg' },
      { name: 'DAX', logo: './svg/powerbi.svg' },
      { name: 'R', logo: './svg/r.svg', filter: 'filter-white' }
    ],
    databases: [
      { name: 'SQL Server', logo: './svg/sql.svg' },
      { name: 'PostgreSQL', logo: './svg/postgresql.svg' },
      { name: 'MongoDB', logo: './svg/mongodb.svg', filter: 'filter-white' },
      { name: 'Supabase', logo: './svg/supabase.svg', filter: 'filter-white' },
      { name: 'SQL Lite', logo: './svg/sqllite.svg' }
    ],
    dataViz: [
      { name: 'PowerBI', logo: './svg/powerbi.svg' },
      { name: 'Tableau', logo: './svg/tableau.svg' },
      { name: 'Excel', logo: './svg/excel.svg' },
      { name: 'Google Analytics', logo: './svg/google-analytics.svg' }
    ],
    webDev: [
      { name: 'HTML', svg: '<svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="m3 2 1.578 17.824L12 22l7.467-2.175L21 2H3Zm14.049 6.048H9.075l.172 2.016h7.697l-.626 6.565-4.246 1.381-4.281-1.455-.288-2.932h2.024l.16 1.411 2.4.815 2.346-.763.297-3.005H7.416l-.562-6.05h10.412l-.217 2.017Z"/></svg>' },
      { name: 'CSS', logo: './svg/css.svg' },
      { name: 'JavaScript', logo: './svg/javascript.svg' },
      { name: 'Django', logo: './svg/django-logo-negative.svg' }
    ],
    mobileDev: [
      { name: 'Java', logo: './svg/java.svg' }
    ],
    infrastructure: [
      { name: 'Azure AppService', logo: './svg/azure.svg' },
      { name: 'Azure Kubernetes', logo: './svg/azure-aks.svg' },
      { name: 'Docker', logo: './svg/docker.svg' },
      { name: 'Google Drive', logo: './svg/google-drive.svg' }
    ]
  }

  const renderSkill = (skill) => (
    <div className="skill-tree-skill" key={skill.name}>
      {skill.svg ? (
        <div dangerouslySetInnerHTML={{ __html: skill.svg }} style={{ width: '25px', height: '25px' }} />
      ) : (
        <img 
          className={`skill-logo ${skill.filter || ''}`}
          src={skill.logo} 
          alt={`Logo ${skill.name}`}
          height="25" 
          width="25"
          loading="lazy"
        />
      )}
      <p>{skill.name}</p>
    </div>
  )

  const categories = [
    { key: 'programming', skills: skills.programming, title: t.programming },
    { key: 'databases', skills: skills.databases, title: t.databases },
    { key: 'dataViz', skills: skills.dataViz, title: t.dataViz },
    { key: 'webDev', skills: skills.webDev, title: t.webDev },
    { key: 'mobileDev', skills: skills.mobileDev, title: t.mobileDev },
    { key: 'infrastructure', skills: skills.infrastructure, title: t.infrastructure }
  ]

  return (
    <div className="skills-container">
      {categories.map((category, idx) => (
        <div key={category.key} className="skill-category glass animated-glass round-border" style={{ animationDelay: `${idx * 0.1}s` }}>
          <h3 className="skill-category-title">{category.title}</h3>
          <div className="skill-category-items">
            {category.skills.map(renderSkill)}
          </div>
        </div>
      ))}
    </div>
  )
}

export default SkillsTree

