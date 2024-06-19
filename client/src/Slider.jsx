// Custom Slider
import React, { useEffect } from "react";
import "./Slider.css";

const Slider = () => {
  useEffect(() => {
    const images = document.querySelectorAll(".hover-gif");

    images.forEach((img) => {
      const staticSrc = img.src;
      const hoverSrc = img.getAttribute("data-hover");

      img.addEventListener("mouseenter", () => {
        img.src = hoverSrc;
      });

      img.addEventListener("mouseleave", () => {
        img.src = staticSrc;
      });
    });
  }, []);

  return (
    <div className="slider-container">
      <div id="slider">
        <figure className="f_slider">
          <img
            src="/assets/slider/Marvel_Logo.png"
            className="hover-gif"
            data-hover="/assets/slider/Marvel_Gif.gif"
          />
          <img
            src="/assets/slider/Disney_Logo.png"
            alt="Disney"
            className="hover-gif"
            data-hover="/assets/slider/Disney_Gif.gif"
          />
          <img
            src="/assets/slider/Pixar_Logo.jpg"
            alt="Pixar"
            className="hover-gif"
            data-hover="/assets/slider/Pixar_Gif.gif"
          />
          <img
            src="/assets/slider/Pokemon_Logo.png"
            alt="Pokemon"
            className="hover-gif"
            data-hover="/assets/slider/Pokemon_Gif.gif"
          />
        </figure>
      </div>
    </div>
  );
};

export default Slider;
