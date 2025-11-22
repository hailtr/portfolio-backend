import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import API_BASE_URL from "../config";

const Navbar = ({ language, toggleLanguage, toggleContact }) => {
  const [menuOpen, setMenuOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const translations = {
    es: {
      home: "Inicio",
      projects: "Proyectos",
      about: "Sobre mí",
      contact: "Contacto",
      viewCV: "Ver CV",
    },
    en: {
      home: "Home",
      projects: "Projects",
      about: "About",
      contact: "Contact",
      viewCV: "View CV",
    },
  };

  const t = translations[language] || translations.es;

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  const handleNavClick = (e) => {
    e.preventDefault();
    const targetId = e.target.getAttribute("href");

    if (targetId === "#contact") {
      toggleContact();
      setMenuOpen(false);
      return;
    }

    // If we're not on the homepage, navigate there first
    if (location.pathname !== "/") {
      navigate("/");
      // Wait for navigation, then scroll
      setTimeout(() => {
        const element = document.querySelector(targetId);
        if (element) {
          element.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      }, 300);
    } else {
      const element = document.querySelector(targetId);
      if (element) {
        element.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }

    setMenuOpen(false);
  };

  return (
    <div className="banner-top glass animated-glass">
      <p className="logo">
        <span style={{ color: "cyan" }}>RAFAEL</span>ORTIZ
      </p>

      <button
        className="menu-toggle"
        aria-label="Abrir menú"
        onClick={toggleMenu}
      >
        &#9776;
      </button>

      <nav id="nav-banner" className={menuOpen ? "active" : ""}>
        <ul className="nav-list">
          <li className="nav-link">
            <a className="nlink" href="#home" onClick={handleNavClick}>
              {t.home}
            </a>
          </li>
          <li className="nav-link">
            <a className="nlink" href="#job" onClick={handleNavClick}>
              {t.projects}
            </a>
          </li>
          <li className="nav-link">
            <a className="nlink" href="#about" onClick={handleNavClick}>
              {t.about}
            </a>
          </li>
          <li className="nav-link">
            <a className="nlink" href="#contact" onClick={handleNavClick}>
              {t.contact}
            </a>
          </li>
        </ul>
      </nav>

      <div className="banner-actions">
        <button
          id="lang-toggle"
          className="lang-switcher"
          onClick={toggleLanguage}
        >
          EN/ES
        </button>
        <a
          href={`${API_BASE_URL.replace("/api", "")}/cv?lang=${language}`}
          target="_blank"
          rel="noopener"
        >
          <button type="button" className="download-curriculum">
            {t.viewCV}
          </button>
        </a>
      </div>
    </div>
  );
};

export default Navbar;
