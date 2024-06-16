import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Navbar } from "../Navbar";
import Swal from "sweetalert2";
import "./Register.css";
import { config, getApiUrl } from "../../utils";

const Register = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      if (username.length < 4 || username.length > 20) {
        throw new Error("Username must be between 4 and 20 characters.");
      }else if (!/\S+@\S+\.\S+/.test(email)) {
        throw new Error("Invalid email format.");
      }else if (!validatePassword(password)) {
        throw new Error(
          "Password must contain at least one uppercase letter, one special character, one number, and be at least 6 characters long."
        );
      }

      const newUser = { username, email, password };

      const response = await fetch(getApiUrl(config.endpoints.signup.url), {
        method: config.endpoints.signup.method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newUser),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(
          data.detail || "Registration failed. Please try again later."
        );
      }

      localStorage.setItem("user", JSON.stringify(newUser));

      Swal.fire({
        icon: "success",
        title: "Registration Successful",
        text: `Welcome ${username}`,
        timer: 3000,
        timerProgressBar: true,
        showConfirmButton: false,
        allowOutsideClick: false,
        willClose: () => {
          navigate("/");
        },
      });
    } catch (error) {
      console.error("Error during registration:", error);
      setError(error.message);

      Swal.fire({
        icon: "error",
        title: "Registration Error",
        text: error.message,
      });
    } finally {
      setLoading(false);
    }
  };

  const isSubmitDisabled = () => {
    return username === "" || email === "" || password === "" || loading;
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
                <h1 className="display-6 fw-bolder text-center">Register</h1>
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
                    <label htmlFor="email" className="form-label">
                      Email address
                    </label>
                    <input
                      type="email"
                      className="form-control"
                      id="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
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
                  {error && (
                    <div className="alert alert-danger mt-3">{error}</div>
                  )}
                  <button
                    type="submit"
                    className="btn btn-outline-dark w-100 mt-3"
                    disabled={isSubmitDisabled()}
                  >
                    {loading ? "Loading..." : "Register"}
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Register;
