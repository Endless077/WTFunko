// Navbar
import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";

import "./Navbar.css";

export const Navbar = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const user = localStorage.getItem("user");
    if (user) {
      try {
        const userParse = JSON.parse(user);
        if (userParse && typeof userParse === 'object' && userParse.username) {
          setIsLoggedIn(true);
          setUsername(userParse.username);
        } else {
          console.error('Invalid data in localStorage:', userParse);
          // Handle case where data in localStorage is not in expected format
          localStorage.removeItem("user")
        }
      } catch (error) {
        console.error('Error parsing localStorage:', error);
        // Handle error if parsing localStorage fails
        localStorage.removeItem("user")
      }
    }
  }, []);
  

  const handleLogout = () => {
    localStorage.clear();
    setIsLoggedIn(false);
    setUsername("");
    navigate("/");
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-light py-3">
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
              <Link
                to={`/profile/${username}`}
                className="btn btn-outline-dark"
              >
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
          <a
            href="https://github.com/Endless077/WTFunko"
            className="btn btn-outline-dark ms-2"
          >
            <i className="fa fa-question-circle" style={{ padding: "5px" }}></i>
            About us
          </a>
        </div>
      </div>
    </nav>
  );
};
