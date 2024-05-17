// index.jsx
import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import App from "./App.jsx";
import Cart from "./components/Cart.jsx";
import ProductInfo from "./components/ProductInfo.jsx";
import Login from "./components/Login.jsx";
import { DevSupport } from "@react-buddy/ide-toolbox";
import { ComponentPreviews, useInitial } from "./dev/index.js";
import "../node_modules/bootstrap/dist/css/bootstrap.min.css";
import "../node_modules/font-awesome/css/font-awesome.min.css";

// Definizione delle rotte
const routes = [
  { path: "/", element: <App /> },
  { path: "/cart", element: <Cart /> },
  { path: "/product/:id", element: <ProductInfo /> },
  { path: "/login", element: <Login /> },
];

// Rendering dell'applicazione con React Router
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <DevSupport
      ComponentPreviews={ComponentPreviews}
      useInitialHook={useInitial}
    >
      <Router>
        <Routes>
          {routes.map(({ path, element }, index) => (
            <Route key={index} path={path} element={element} />
          ))}
        </Routes>
      </Router>
    </DevSupport>
  </React.StrictMode>
);
