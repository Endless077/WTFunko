import { Products } from "./components/Products.jsx";
import "./Home.css";
import { Link } from "react-router-dom";

export const Home = () => {
  return (
    <div className="container">
      <div className="hero">
        <Link href="#" className="card-link">
          <div className="card text-bg-dark border-0">
            <img
              src="/assets/questionMark.png"
              className="card-img"
              alt="background"
              height="500"
            />
            <div className="card-img-overlay d-flex flex-column justify-content-center">
              <div className="container">
                <h5 className="card-title text-white display-3 fw-bolder mb-0">
                  DISCOVER YOUR RANDOM FUNKO
                </h5>
                <p className="card-text text-black lead fs-2">
                  ROLL THE DICE OF DESTINY
                </p>
              </div>
            </div>
          </div>
        </Link>
        <Products />
      </div>
    </div>
  );
};
