import React from "react";
import ReactDOM from "react-dom/client";
import "bootstrap/dist/css/bootstrap.min.css"; // Importa il CSS di Bootstrap
import Home from "./Home.tsx";

// Assicurati che l'elemento con id 'root' esista nel tuo file index.html
ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <Home />
  </React.StrictMode>
);
