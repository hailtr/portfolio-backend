const ExperienceCard = ({ experience }) => {
  return (
    <div className="experience-card glass round-border animated-glass">
      <div className="experience-header">
        <h1>{experience.company}</h1>
        <h3>{experience.role}</h3>
      </div>
      <p>
        <i className="fa-solid fa-location-dot"></i> {experience.location}
      </p>
      <div className="skill-logo-name">
        {experience.skills.map((skill, idx) => (
          <span key={idx} className="relative-skill">
            {skill}
          </span>
        ))}
      </div>
    </div>
  )
}

export default ExperienceCard

