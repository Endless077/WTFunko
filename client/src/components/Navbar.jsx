import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./Navbar.css";

export const Navbar = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState("");

  useEffect(() => {
    const user = localStorage.getItem("user");
    if (user) {
      const { username } = JSON.parse(user);
      setIsLoggedIn(true);
      setUsername(username);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("cart");
    setIsLoggedIn(false);
    setUsername("");
    window.location.reload();
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
                <Link to="/userInfo" className="btn btn-outline-dark">
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
              to="https://github.com/Endless077/WTFunko"
              className="btn btn-outline-dark ms-2"
              onClick={handleLogout}
            >
              <i
                className="fa fa-question-circle"
                style={{ padding: "5px" }}
              ></i>
              About us
            </Link>
          </div>
        </div>
      </nav>
    </>
  );
};
