// components/Navbar.jsx
import React, { useState } from "react";
import { FaSearch } from "react-icons/fa";
import { Link } from "react-router-dom";
import "./Navbar.css";

export const Navbar = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-light py-3 bg-white">
      <div className="container">
        <Link className="navbar-brand fw-bold fs-4" to="/">
          <img
            src="/assets/WTF.png"
            className="navbar-brand"
            alt="Brand Logo"
          />
        </Link>
        <div className="search-bar">
          <div className="input-group">
            <input
              type="text"
              className="form-control"
              placeholder="Search a Product..."
              aria-label="Search"
              aria-describedby="search-icon"
            />
            <button
              className="btn btn-outline-dark"
              type="button"
              id="search-icon"
            >
              <FaSearch />
            </button>
          </div>
        </div>
        <div className="buttons">
          {isLoggedIn ? (
            <Link to="/profile" className="btn btn-outline-dark">
              <i className="fa fa-user me-1"></i>
              Profile
            </Link>
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
          <a href="" className="btn btn-outline-dark ms-2">
            <i className="fa fa-question-circle" style={{ padding: "5px" }}></i>
            About us
          </a>
        </div>
      </div>
    </nav>
  );
};
