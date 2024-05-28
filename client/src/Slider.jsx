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
      <div className="col-12 mb-4 text-center">
        <h1 className="display-6 fw-bolder">
          Discover your favourite category!
        </h1>
      </div>
      <div id="slider">
        <figure className="f_slider">
          <a href="ProdottoList?franchise=Marvel">
            <img
              src="/assets/slider/Marvel_Logo.png"
              className="hover-gif"
              data-hover="/assets/slider/Marvel_Gif.gif"
            />
          </a>
          <a href="ProdottoList?franchise=Disney">
            <img
              src="/assets/slider/Disney_Logo.png"
              alt="Disney"
              className="hover-gif"
              data-hover="/assets/slider/Disney_Gif.gif"
            />
          </a>
          <a href="ProdottoList?franchise=Pixar">
            <img
              src="/assets/slider/Pixar_Logo.jpg"
              alt="Pixar"
              className="hover-gif"
              data-hover="/assets/slider/Pixar_Gif.gif"
            />
          </a>
          <a href="ProdottoList?franchise=Pokemon">
            <img
              src="/assets/slider/Pokemon_Logo.png"
              alt="Pokemon"
              className="hover-gif"
              data-hover="/assets/slider/Pokemon_Gif.gif"
            />
          </a>
        </figure>
      </div>
    </div>
  );
};

export default Slider;
