import { Link } from "react-router-dom";

const NotFound = ({ language }) => {
  const t = {
    es: {
      title: "404",
      message: "La pagina que buscas no existe.",
      back: "Volver al inicio",
    },
    en: {
      title: "404",
      message: "The page you're looking for doesn't exist.",
      back: "Back to home",
    },
  }[language] || {
    title: "404",
    message: "Page not found.",
    back: "Back to home",
  };

  return (
    <div className="not-found-page">
      <h1>{t.title}</h1>
      <p>{t.message}</p>
      <Link to="/">{t.back}</Link>
    </div>
  );
};

export default NotFound;
