import React, { useState } from "react";
import { FaSearch } from "react-icons/fa";
import { Link } from "react-router-dom";
import "./Navbar.css";

export const Navbar = () => {


  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState("");

  const handleLogin = () => {
    setIsLoggedIn(true);
    setUsername(username);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUsername(""); // Svuota il nome utente quando l'utente esegue il logout
  };

  return (
    <>
    <nav className="navbar navbar-expand-lg navbar-light py-3 bg-white">
      <div className="container">
        <Link className="navbar-brand fw-bold fs-4" to="/">
          <img
            src="/assets/WTF.png"
            className="navbar-brand"
            alt="Brand Logo"
          />
        </Link>
        <div className="buttons">
          {isLoggedIn ? (
            <>
              <Link to="/profile" className="btn btn-outline-dark">
                <i className="fa fa-user me-1"></i>
                {username}
              </Link>
              <button
                onClick={handleLogout}
                className="btn btn-outline-dark ms-2"
              >
                Logout
              </button>
            </>
          ) : (
            <Link to="/login" className="btn btn-outline-dark">
              <i className="fa fa-sign-in me-1"></i>
              Login
            </Link>
          )}
          <Link to="/cart" className="btn btn-outline-dark ms-2">
            <i className="fa fa-shopping-cart me-1"></i>
            Cart
          </Link>
          <Link
            to="/"
            className="btn btn-outline-dark ms-2"
            onClick={handleLogout}
          >
            <i className="fa fa-question-circle" style={{ padding: "5px" }}></i>
            About us
          </Link>
        </div>
      </div>
    </nav>

    </>  
  );
};
