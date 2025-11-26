const Footer = ({ language }) => {
  const currentYear = new Date().getFullYear();

  const translations = {
    es: {
      credit: `© Rafael Ortiz | 2023 - ${currentYear}`,
      disclaimer: "Portafolio en desarrollo continuo",
    },
    en: {
      credit: `© Rafael Ortiz | 2023 - ${currentYear}`,
      disclaimer: "Portfolio under continuous development",
    },
  };

  const t = translations[language] || translations.es;

  return (
    <footer className="site-footer">
      <p>{t.credit}</p>
      <p>{t.disclaimer}</p>
    </footer>
  );
};

export default Footer;
