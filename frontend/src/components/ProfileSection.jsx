const ProfileSection = ({ language }) => {
  const translations = {
    es: {
      role: 'Data Analyst',
      tagline: 'Transformando datos en decisiones estratégicas',
    },
    en: {
      role: 'Data Analyst',
      tagline: 'Transforming data into strategic decisions',
    }
  }

  const t = translations[language] || translations.es

  return (
    <section id="home" className="section">
      <div className="home-section">
        <div className="profile">
          <div className="profile-picture-wrapper">
            <img 
              src="/images/profilepicture.jpg" 
              alt="Foto personal" 
              className="profile-picture"
            />
          </div>
          <div className="profile-greating">
            <h2>
              <span className="name">Rafael</span> Ortiz
            </h2>
            <h1>{t.role}</h1>
            <p className="tagline">{t.tagline}</p>
            <p>
              <span className="country-before">Santiago de Chile, Chile</span>
              <span className="country-after"> Caracas, Venezuela</span>
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}

export default ProfileSection

