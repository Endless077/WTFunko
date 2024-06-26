// Login Component
import React, { useState } from "react";
import { Navbar } from "../Navbar";
import { Link, useNavigate } from "react-router-dom";

// Utils
import "./Login.css";
import Swal from "sweetalert2";
import { config, fetchData } from "../../utils";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  /* ********************************************************************************************* */

  const handleSubmit = async (e) => {
    const loginRequest = async () => {
      try {
        const endpointUrl = config.endpoints.login.url;
        const method = config.endpoints.login.method;
        const payload = { username, email: username, password };

        const loginResponse = await fetchData(
          endpointUrl,
          undefined,
          method,
          undefined,
          undefined,
          payload
        );

        const loginResponseData = await loginResponse.json();
        if (!loginResponse.ok) {
          throw new Error(
            loginResponseData.detail || "Login failed. Please try again later."
          );
        }

        Swal.fire({
          icon: "success",
          title: "Login Successful",
          text: `Welcome back\uD83D\uDC4B, ${username}!`,
          timer: 3000,
          timerProgressBar: true,
          showConfirmButton: false,
          allowOutsideClick: false,
          willClose: () => {
            localStorage.setItem("user", JSON.stringify(loginResponseData));
            localStorage.setItem(
              "token",
              JSON.stringify(loginResponseData.token)
            );
            navigate("/");
          },
        });

        return loginResponseData;
      } catch (error) {
        console.error("Error signup attempt:", error);
        Swal.fire({
          icon: "error",
          title: "Error during login attempt",
          text: error.message,
        });
      }
    };

    try {
      e.preventDefault();
      setLoading(true);
      setError("");

      if (username.length < 4 || username.length > 20) {
        throw new Error("Username must be between 4 and 20 characters.");
      } else if (!validatePassword(password)) {
        throw new Error(
          "Password must contain at least one uppercase letter, one special character, one number, and be at least 6 characters long."
        );
      }

      await loginRequest();
    } catch (error) {
      console.error("Error during registration:", error);
      setError(error.message);

      Swal.fire({
        icon: "error",
        title: "Error during login attempt",
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

  /* ********************************************************************************************* */

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
