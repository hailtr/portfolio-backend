const Loader = ({ language }) => {
  const translations = {
    es: {
      title: 'Cargando...',
      subtitle: 'Preparando tu experiencia',
      delay: 'Esto está tomando más tiempo de lo esperado...'
    },
    en: {
      title: 'Loading...',
      subtitle: 'Preparing your experience',
      delay: 'This is taking longer than expected...'
    }
  }

  const t = translations[language] || translations.es

  return (
    <div id="loader">
      <div className="spinner"></div>
      <p>{t.title}</p>
      <p>{t.subtitle}</p>
    </div>
  )
}

export default Loader

