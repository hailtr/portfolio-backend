import { useState, useEffect } from "react";
import { Routes, Route, useLocation } from "react-router-dom";
import { motion, useScroll, useSpring } from "framer-motion";
import Navbar from "./components/Navbar";
import ProfileSection from "./components/ProfileSection";
import ProjectsSection from "./components/ProjectsSection";
import AboutSection from "./components/AboutSection";
import Footer from "./components/Footer";
import Loader from "./components/Loader";
import ContactOverlay from "./components/ContactOverlay";
import BackgroundShapes from "./components/BackgroundShapes";
import ProjectDetail from "./pages/ProjectDetail";
import API_BASE_URL from "./config";
import { useCachedFetch } from "./hooks/useCachedFetch";
import "./App.css";

function App() {
  const [language, setLanguage] = useState("es");
  const [showContact, setShowContact] = useState(false);
  const location = useLocation();
  const { scrollYProgress } = useScroll();
  const scaleX = useSpring(scrollYProgress, {
    stiffness: 100,
    damping: 30,
    restDelta: 0.001,
  });

  const {
    data: projectsData,
    loading,
    error,
  } = useCachedFetch(
    `${API_BASE_URL}/projects?lang=${language}`,
    `home_projects_${language}`,
  );

  const projects = projectsData || [];

  useEffect(() => {
    if (loading) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
          }
        });
      },
      { threshold: 0.1 },
    );

    setTimeout(() => {
      document.querySelectorAll(".reveal-section").forEach((el) => {
        observer.observe(el);
      });
    }, 100);

    return () => observer.disconnect();
  }, [loading, location]);

  const toggleLanguage = () => {
    setLanguage((lang) => (lang === "es" ? "en" : "es"));
  };

  const toggleContact = () => {
    setShowContact(!showContact);
  };

  if (error === "RATELIMIT" && location.pathname === "/") {
    return (
      <div
        style={{
          height: "100vh",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          color: "white",
          background: "var(--main-darkblue)",
        }}
      >
        <h1>Demasiada velocidad</h1>
        <p>Se han recibido demasiadas peticiones. Espera unos minutos.</p>
      </div>
    );
  }

  if (loading && location.pathname === "/") {
    return <Loader language={language} />;
  }

  return (
    <div className="App">
      <motion.div
        className="progress-bar"
        style={{
          scaleX,
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          height: "4px",
          background: "var(--accent-cyan)",
          transformOrigin: "0%",
          zIndex: 10000,
        }}
      />
      <BackgroundShapes />
      <Navbar
        language={language}
        toggleLanguage={toggleLanguage}
        toggleContact={toggleContact}
      />

      <Routes location={location} key={location.pathname}>
        <Route
          path="/"
          element={
            <motion.main
              className="visible"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <ProfileSection language={language} />
              <ProjectsSection language={language} projects={projects} />
              <AboutSection language={language} />
            </motion.main>
          }
        />

        <Route
          path="/project/:slug"
          element={
            <motion.main
              className="visible"
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5 }}
            >
              <ProjectDetail language={language} />
            </motion.main>
          }
        />
      </Routes>

      <Footer language={language} />
      <ContactOverlay
        show={showContact}
        onClose={() => setShowContact(false)}
        language={language}
      />
    </div>
  );
}

export default App;
