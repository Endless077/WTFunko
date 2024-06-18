// Import React
import React from "react";
import ReactDOM from "react-dom/client";

// Support
import { DevSupport } from "@react-buddy/ide-toolbox";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { ComponentPreviews, useInitial } from "./dev/index.js";
import "../node_modules/bootstrap/dist/css/bootstrap.min.css";
import "../node_modules/font-awesome/css/font-awesome.min.css";

// Main App
import App from "./App.jsx";

// Product
import Cart from "./components/CartComponent/Cart.jsx";
import ProductInfo from "./components/ProductComponent/ProductInfoComponent/ProductInfo.jsx";

// User
import Login from "./components/LoginComponent/Login.jsx";
import Register from "./components/RegisterComponent/Register.jsx";
import UserInfo from "./components/UserInfoComponent/UserInfo.jsx";

/* ********************************************************************************************* */

// Routes
const routes = [
  { path: "/", element: <App /> },
  { path: "/cart", element: <Cart /> },
  { path: "/productInfo/:id", element: <ProductInfo /> },
  { path: "/login", element: <Login /> },
  { path: "/register", element: <Register /> },
  { path: "/profile", element: <UserInfo /> },
];

// Startup React Project
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
