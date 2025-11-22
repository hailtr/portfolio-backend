const ContactOverlay = ({ show, onClose, language }) => {
  const translations = {
    es: {
      message: "¡Hablemos!",
      email: "lustigrfortiz@gmail.com",
    },
    en: {
      message: "Let's talk!",
      email: "lustigrfortiz@gmail.com",
    },
  };

  const t = translations[language] || translations.es;

  return (
    <div
      className={`contact-overlay ${show ? "active" : ""}`}
      id="contactOverlay"
    >
      <div className="contact-card">
        <h3>{t.message}</h3>
        <p>
          📧 <a href="mailto:lustigrfortiz@gmail.com">{t.email}</a>
        </p>
        <p>
          🔗{" "}
          <a
            href="https://www.linkedin.com/in/rafaelortizaguilar/"
            target="_blank"
            rel="noopener noreferrer"
          >
            LinkedIn
          </a>
        </p>
      </div>
    </div>
  );
};

export default ContactOverlay;
