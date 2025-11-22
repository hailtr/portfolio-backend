import { useState, useEffect } from "react";
import { motion, useMotionValue, useTransform } from "framer-motion";
import Typewriter from "typewriter-effect";
import API_BASE_URL from "../config";

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
      .catch((err) => {
        console.error("Error fetching profile:", err);
        setLoading(false);
      });
  }, [language]);

  if (loading) {
    return null; // or a skeleton loader
  }

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
              alt="Foto personal"
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
              <Typewriter
                options={{
                  strings: [
                    profile.role,
                    language === "es" ? "Experto en Python" : "Python Expert",
                    language === "es"
                      ? "Arquitecto Cloud"
                      : "Cloud Architect",
                  ],
                  autoStart: true,
                  loop: true,
                  delay: 50,
                  deleteSpeed: 30,
                }}
              />
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
