import { useState, useEffect } from "react";
import { motion, useMotionValue, useTransform, AnimatePresence } from "framer-motion";
import API_BASE_URL from "../config";

const RoleCycler = ({ roles }) => {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((i) => (i + 1) % roles.length);
    }, 3000);
    return () => clearInterval(interval);
  }, [roles.length]);

  return (
    <AnimatePresence mode="wait">
      <motion.span
        key={roles[index]}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        transition={{ duration: 0.4 }}
      >
        {roles[index]}
      </motion.span>
    </AnimatePresence>
  );
};

const ProfileSection = ({ language }) => {
  const [profile, setProfile] = useState({
    name: "Rafael Ortiz",
    role: "Data Engineer",
    tagline: "Transforming data into strategic decisions",
    location: { city: "Caracas", country: "Venezuela" },
  });
  const [loading, setLoading] = useState(true);

  // Parallax effect logic
  const x = useMotionValue(0);
  const y = useMotionValue(0);
  const rotateX = useTransform(y, [-100, 100], [10, -10]);
  const rotateY = useTransform(x, [-100, 100], [-10, 10]);

  const handleMouseMove = (event) => {
    const rect = event.currentTarget.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    x.set(event.clientX - centerX);
    y.set(event.clientY - centerY);
  };

  const handleMouseLeave = () => {
    x.set(0);
    y.set(0);
  };

  useEffect(() => {
    // Fetch profile from API
    fetch(`${API_BASE_URL}/profile?lang=${language}`)
      .then((res) => res.json())
      .then((data) => {
        setProfile(data);
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
      });
  }, [language]);

  if (loading) {
    return (
      <section className="section">
        <div className="home-section" id="home">
          <div className="profile">
            <div className="profile-picture-wrapper">
              <div className="skeleton skeleton-circle" style={{ width: "100%", height: "100%", borderRadius: "50%" }} />
            </div>
            <div className="profile-greating" style={{ gap: "1.5rem" }}>
              <div className="skeleton" style={{ width: "60%", height: "6rem" }} />
              <div className="skeleton" style={{ width: "80%", height: "4rem" }} />
              <div className="skeleton" style={{ width: "70%", height: "2rem" }} />
            </div>
          </div>
        </div>
      </section>
    );
  }

  const roles = language === "es"
    ? [
        profile.role === "Data Engineer" ? "Ingeniero de Datos" : profile.role,
        "Experto en Python",
        "Arquitecto Cloud",
      ]
    : [
        profile.role,
        "Python Expert",
        "Cloud Architect",
      ];

  return (
    <section className="section">
      <div className="home-section" id="home">
        <div className="profile">
          <motion.div
            className="profile-picture-wrapper"
            onMouseMove={handleMouseMove}
            onMouseLeave={handleMouseLeave}
            style={{
              rotateX,
              rotateY,
              perspective: 1000,
              cursor: "pointer",
            }}
            whileHover={{ scale: 1.05 }}
            transition={{ type: "spring", stiffness: 400, damping: 30 }}
          >
            <img
              src="/images/profilepicture.jpg"
              alt={language === "es" ? "Foto personal" : "Profile picture"}
              className="profile-picture"
              style={{ pointerEvents: "none" }}
            />
          </motion.div>
          <div className="profile-greating">
            <h2>
              <span className="name">{profile.name.split(" ")[0]}</span>{" "}
              {profile.name.split(" ")[1]}
            </h2>
            <h1 style={{ minHeight: "60px" }}>
              <RoleCycler roles={roles} />
            </h1>
            <p className="tagline">{profile.tagline}</p>
            <p>
              <span className="country-before">Santiago de Chile, Chile</span>
              <span className="country-after">
                {" "}
                {profile.location?.city}, {profile.location?.country}
              </span>
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ProfileSection;
