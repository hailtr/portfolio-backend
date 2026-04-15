import { useEffect, useRef } from "react";

const ContactOverlay = ({ show, onClose, language }) => {
  const overlayRef = useRef(null);

  const translations = {
    es: {
      message: "Hablemos!",
      email: "lustigrfortiz@gmail.com",
      close: "Cerrar",
    },
    en: {
      message: "Let's talk!",
      email: "lustigrfortiz@gmail.com",
      close: "Close",
    },
  };

  const t = translations[language] || translations.es;

  // ESC key handler
  useEffect(() => {
    if (!show) return;
    const handleKeyDown = (e) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [show, onClose]);

  // Click outside to close
  useEffect(() => {
    if (!show) return;
    const handleClickOutside = (e) => {
      if (overlayRef.current && !overlayRef.current.contains(e.target)) {
        onClose();
      }
    };
    // Delay to avoid closing on the same click that opened it
    const timer = setTimeout(() => {
      document.addEventListener("mousedown", handleClickOutside);
    }, 100);
    return () => {
      clearTimeout(timer);
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [show, onClose]);

  return (
    <div
      ref={overlayRef}
      className={`contact-overlay ${show ? "active" : ""}`}
      id="contactOverlay"
      role="dialog"
      aria-modal="true"
      aria-label={t.message}
    >
      <div className="contact-card">
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <h3>{t.message}</h3>
          <button
            onClick={onClose}
            aria-label={t.close}
            style={{
              background: "none",
              border: "none",
              color: "var(--accent-cyan)",
              fontSize: "2rem",
              cursor: "pointer",
              padding: "0.5rem",
              lineHeight: 1,
            }}
          >
            &times;
          </button>
        </div>
        <p>
          <span role="img" aria-label="Email">&#x1F4E7;</span>{" "}
          <a href="mailto:lustigrfortiz@gmail.com">{t.email}</a>
        </p>
        <p>
          <span role="img" aria-label="Link">&#x1F517;</span>{" "}
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
