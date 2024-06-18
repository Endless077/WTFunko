// Home App
import React from "react";
import "./Home.css";

import Slider from "./Slider.jsx";
import { Products } from "./components/ProductComponent/Products.jsx";

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
