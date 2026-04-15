import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import API_BASE_URL from "../config";
import SkillsTree from "./SkillsTree";
import EducationCard from "./EducationCard";
import ExperienceCard from "./ExperienceCard";

const AboutSection = ({ language }) => {
  const [experienceData, setExperienceData] = useState([]);
  const [educationData, setEducationData] = useState([]);
  const [loading, setLoading] = useState(true);

  const translations = {
    es: {
      skills: "Habilidades",
      education: "Educación",
      experience: "Experiencia",
    },
    en: {
      skills: "Skills",
      education: "Education",
      experience: "Experience",
    },
  };

  const t = translations[language] || translations.es;

  useEffect(() => {
    const abortController = new AbortController();
    let isMounted = true;

    // Fetch work experience
    fetch(`${API_BASE_URL}/experience?lang=${language}`, {
      signal: abortController.signal
    })
      .then((res) => res.json())
      .then((data) => {
        if (!isMounted) return; // Prevent setState on unmounted component
        const formatted = data.map((item) => ({
          company: item.company,
          role: item.title,
          location: item.location,
          skills: item.tags || [],
          startDate: item.startDate,
          endDate: item.endDate,
          current: item.current,
          description: item.description
        }));
        setExperienceData(formatted);
      })
      .catch((err) => {
        if (err.name === 'AbortError') return; // Ignore abort errors
        console.error("Error fetching experience:", err);
      });

    // Fetch education
    fetch(`${API_BASE_URL}/education?lang=${language}`, {
      signal: abortController.signal
    })
      .then((res) => res.json())
      .then((data) => {
        if (!isMounted) return; // Prevent setState on unmounted component
        const formatted = data.map((item) => {
          // Format date helper inside the map to use it immediately
          const formatDate = (dateString) => {
            if (!dateString) return "";
            try {
              const date = new Date(dateString);

              // Check if valid date
              if (isNaN(date.getTime())) {
                console.warn("Invalid date:", dateString);
                return dateString;
              }

              // Format: "01/2024" (MM/YYYY) using UTC to avoid timezone shifts
              return new Intl.DateTimeFormat(language === 'es' ? 'es-ES' : 'en-US', {
                month: '2-digit',
                year: 'numeric',
                timeZone: 'UTC'
              }).format(date);
            } catch (e) {
              console.error("Format error:", e);
              return dateString;
            }
          };

          // Format date
          let dateStr = "";
          if (item.current) {
            dateStr = item.startDate
              ? `${formatDate(item.startDate)} - ${language === "es" ? "Presente" : "Present"}`
              : language === "es"
                ? "Presente"
                : "Present";
          } else if (item.endDate && item.startDate) {
            // Both dates: show range
            dateStr = `${formatDate(item.startDate)} - ${formatDate(item.endDate)}`;
          } else if (item.endDate) {
            // Only end date (courses): show just the date
            dateStr = formatDate(item.endDate);
          } else if (item.startDate) {
            // Only start date
            dateStr = formatDate(item.startDate);
          }

          return {
            institution: item.institution || "",
            title: `${item.title} ${language === "es" ? "en" : "in"} ${item.subtitle}`,
            date: dateStr,
            location: item.location || "",
            skills: item.courses || [],
          };
        });
        setEducationData(formatted);
        setLoading(false);
      })
      .catch((err) => {
        if (err.name === 'AbortError') return; // Ignore abort errors
        console.error("Error fetching education:", err);
        if (isMounted) setLoading(false);
      });

    // Cleanup function
    return () => {
      isMounted = false;
      abortController.abort();
    };
  }, [language]);

  return (
    <section className="section reveal-section">
      <div className="aboutme-section">
        <div className="content-container reveal-section visible" id="about">
          <h2>{t.skills}</h2>
          <SkillsTree language={language} />
        </div>

        <div className="content-container reveal-section">
          <h2>{t.experience}</h2>
          <motion.div
            className="experienceitems"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.2 }}
            variants={{
              hidden: {},
              visible: {
                transition: {
                  staggerChildren: 0.2,
                },
              },
            }}
          >
            {experienceData.map((exp, idx) => (
              <motion.div
                key={idx}
                variants={{
                  hidden: { opacity: 0, x: -50 },
                  visible: { opacity: 1, x: 0 },
                }}
                transition={{ duration: 0.5 }}
                style={{ display: "contents" }}
              >
                <ExperienceCard experience={exp} />
              </motion.div>
            ))}
          </motion.div>
        </div>

        <div className="content-container reveal-section">
          <h2>{t.education}</h2>
          <motion.div
            className="educationitems"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.2 }}
            variants={{
              hidden: {},
              visible: {
                transition: {
                  staggerChildren: 0.15,
                },
              },
            }}
          >
            {educationData.map((edu, idx) => (
              <motion.div
                key={idx}
                variants={{
                  hidden: { opacity: 0, y: 30 },
                  visible: { opacity: 1, y: 0 },
                }}
                transition={{ duration: 0.5 }}
                style={{ display: "contents" }}
              >
                <EducationCard education={edu} />
              </motion.div>
            ))}
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default AboutSection;
