import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { ComponentPreviews, useInitial } from "./dev/index.js";
import "../node_modules/bootstrap/dist/css/bootstrap.min.css";
import "../node_modules/font-awesome/css/font-awesome.min.css";
//importing Routes
import App from "./App.jsx";
import Cart from "./components/CartComponent/Cart.jsx";
import ProductInfo from "./components/ProductInfoComponent/ProductInfo.jsx";
import Login from "./components/LoginComponent/Login.jsx";
import Register from "./components/RegisterComponent/Register.jsx";


import { DevSupport } from "@react-buddy/ide-toolbox";

// Defining of routes
const routes = [
  { path: "/", element: <App /> },
  { path: "/cart", element: <Cart /> },
  { path: "/productInfo/:id", element: <ProductInfo /> },
  { path: "/login", element: <Login /> },
  { path: "/register", element: <Register /> },
];

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <DevSupport ComponentPreviews={ComponentPreviews} useInitialHook={useInitial}>
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
