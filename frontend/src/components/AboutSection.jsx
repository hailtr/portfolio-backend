import { useState, useEffect } from "react";
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
    // Fetch work experience
    fetch(`${API_BASE_URL}/entities?lang=${language}&type=experience`)
      .then((res) => res.json())
      .then((data) => {
        const formatted = data.map((item) => ({
          company: item.company || "",
          role: item.title || "",
          location: item.location || "",
          skills: item.tags || [],
        }));
        setExperienceData(formatted);
      })
      .catch((err) => console.error("Error fetching experience:", err));

    // Fetch education
    fetch(`${API_BASE_URL}/entities?lang=${language}&type=education`)
      .then((res) => res.json())
      .then((data) => {
        const formatted = data.map((item) => {
          // Format date
          let dateStr = "";
          if (item.current) {
            dateStr = item.startDate
              ? `${item.startDate} - ${language === "es" ? "Presente" : "Present"}`
              : language === "es"
                ? "Presente"
                : "Present";
          } else if (item.endDate && item.startDate) {
            // Both dates: show range
            dateStr = `${item.startDate} - ${item.endDate}`;
          } else if (item.endDate) {
            // Only end date (courses): show just the year
            dateStr = item.endDate;
          } else if (item.startDate) {
            // Only start date
            dateStr = item.startDate;
          }

          return {
            institution: item.institution || "",
            title: `${item.subtitle} ${language === "es" ? "en" : "in"} ${item.title}`,
            date: dateStr,
            location: item.location || "",
            skills: item.courses || [],
          };
        });
        setEducationData(formatted);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching education:", err);
        setLoading(false);
      });
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
          <div className="experienceitems">
            {experienceData.map((exp, idx) => (
              <ExperienceCard key={idx} experience={exp} />
            ))}
          </div>
        </div>

        <div className="content-container reveal-section">
          <h2>{t.education}</h2>
          <div className="educationitems">
            {educationData.map((edu, idx) => (
              <EducationCard key={idx} education={edu} />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default AboutSection;
