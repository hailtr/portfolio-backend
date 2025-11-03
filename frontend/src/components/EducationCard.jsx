const EducationCard = ({ education }) => {
  return (
    <div className="education-card glass round-border animated-glass">
      <div className="experience-header">
        <h1>{education.institution}</h1>
        <h3>{education.title}</h3>
      </div>
      <p>
        <i className="fa-solid fa-calendar"></i> {education.date}
      </p>
      <div className="skill-logo-name">
        {education.skills.map((skill, idx) => (
          <span key={idx} className="relative-skill">
            {skill}
          </span>
        ))}
      </div>
    </div>
  )
}

export default EducationCard

