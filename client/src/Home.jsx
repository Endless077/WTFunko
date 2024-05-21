import React from "react";
import { Products } from "./components/ProductComponent/Products.jsx";
import "./Home.css";
import Slider from "./Slider.jsx";

export const Home = () => {
  return (
    <div className="container">
      <div className="hero">
        <Slider />
        <Products />
      </div>
    </div>
  );
};
