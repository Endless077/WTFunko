import React, { useState } from "react";
import { Navbar } from "../Navbar";
import { Link, useNavigate } from "react-router-dom";
import Swal from "sweetalert2";
import "./Login.css";
import { config, getApiUrl } from "../../utils";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      if (username.length < 4 || username.length > 20) {
        throw new Error("Username must be between 4 and 20 characters.");
      }else if(!validatePassword(password)) {
        throw new Error(
          "Password must contain at least one uppercase letter, one special character, one number, and be at least 6 characters long."
        );
      }

      const user = { username, email: username, password };
      
      const response = await fetch(getApiUrl(config.endpoints.login.url), {
        method: config.endpoints.login.method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(user),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Login failed. Please try again later.");
      }

      localStorage.setItem("user", JSON.stringify(data));

      Swal.fire({
        icon: "success",
        title: "Login Successful",
        text: `Welcome ${data.username}`,
        timer: 3000,
        timerProgressBar: true,
        showConfirmButton: false,
        allowOutsideClick: false,
        willClose: () => {
          navigate("/");
        },
      });
    } catch (error) {
      console.error("Error during login:", error);
      setError(error.message);

      Swal.fire({
        icon: "error",
        title: "Login Error",
        text: error.message,
      });
    } finally {
      setLoading(false);
    }
  };

  const isSubmitDisabled = () => {
    return username === "" || password === "" || loading;
  };

  const validatePassword = (password) => {
    const passwordRegex = /^(?=.*[A-Z])(?=.*[!@#$%^&*])(?=.*[0-9]).{6,}$/;
    return passwordRegex.test(password);
  };

  return (
    <>
      <Navbar />
      <div className="container my-5 py-5">
        <div className="row justify-content-center">
          <div className="col-md-6">
            <div className="card">
              <div className="card-body">
                <h1 className="display-6 fw-bolder text-center">Login</h1>
                <form onSubmit={handleSubmit} noValidate>
                  <div className="mb-3">
                    <label htmlFor="username" className="form-label">
                      Username
                    </label>
                    <input
                      type="text"
                      className="form-control"
                      id="username"
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="password" className="form-label">
                      Password
                    </label>
                    <input
                      type="password"
                      className="form-control"
                      id="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                    />
                  </div>
                  {error && <div className="alert alert-danger">{error}</div>}
                  <button
                    type="submit"
                    className="btn btn-outline-dark w-100 mt-3"
                    disabled={isSubmitDisabled()}
                  >
                    {loading ? "Loading..." : "Login"}
                  </button>
                </form>
                <div className="mt-3 text-center">
                  <p>Not registered yet?</p>
                  <Link to="/register" className="btn btn-outline-dark ms-2">
                    <i className="fa fa-user-plus me-1"></i>
                    Register
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Login;
