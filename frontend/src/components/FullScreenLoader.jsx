// src/components/FullScreenLoader.jsx
import React from "react";
import "../App.css";

const FullScreenLoader = ({ message = "Cargando..." }) => {
  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        background: "var(--main-darkblue)", // Usa tu variable de color
        zIndex: 9999,
      }}
    >
      <div className="spinner"></div>
      <p
        style={{
          marginTop: "1.5rem",
          color: "var(--accent-cyan)",
          fontSize: "1.4rem",
          fontWeight: 500,
        }}
      >
        {message}
      </p>
    </div>
  );
};

export default FullScreenLoader;
