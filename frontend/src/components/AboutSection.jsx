import SkillsTree from './SkillsTree'
import EducationCard from './EducationCard'
import ExperienceCard from './ExperienceCard'

const AboutSection = ({ language }) => {
  const translations = {
    es: {
      skills: 'Habilidades',
      education: 'Educación',
      experience: 'Experiencia'
    },
    en: {
      skills: 'Skills',
      education: 'Education',
      experience: 'Experience'
    }
  }

  const t = translations[language] || translations.es

  const educationData = [
    {
      institution: 'IUGT',
      title: language === 'es' ? 'Técnico Superior en Informática' : 'Higher Technician in Computer Science',
      date: '2018-2024',
      skills: [
        'Python',
        'SQL', 
        'Java',
        'Machine Learning',
        'Data Analysis',
        'Agile',
        language === 'es' ? 'Análisis de Sistemas' : 'Systems Analysis',
        language === 'es' ? 'Estructuras de Datos' : 'Data Structures',
        'C'
      ]
    }
  ]

  const experienceData = [
    {
      company: 'ThermoGroup C.A',
      role: 'Data Analyst',
      location: 'Venezuela',
      skills: ['Python', 'DAX', 'PowerBI', 'ProfitPlus', 'PostgreSQL', 'Django']
    },
    {
      company: 'Austranet',
      role: language === 'es' ? 'Analista de Sistemas' : 'Systems Analyst',
      location: 'Chile',
      skills: ['Python', 'SQL Server', 'Windows Server', 'PRTG', 'Azure AppService', 'Azure Functions', 'PowerQuery']
    }
  ]

  return (
    <section className="section reveal-section">
      <div className="aboutme-section">
        <div className="content-container reveal-section visible" id="about">
          <h2>{t.skills}</h2>
          <SkillsTree language={language} />
        </div>

        <div className="content-container reveal-section">
          <h2>{t.experience}</h2>
          <div className="experienceitems">
            {experienceData.map((exp, idx) => (
              <ExperienceCard key={idx} experience={exp} />
            ))}
          </div>
        </div>

        <div className="content-container reveal-section">
          <h2>{t.education}</h2>
          <div className="educationitems">
            {educationData.map((edu, idx) => (
              <EducationCard key={idx} education={edu} />
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}

export default AboutSection

