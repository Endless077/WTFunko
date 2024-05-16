import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import { Link } from "react-router-dom";

const CarouselSection = () => {
  const CustomPrevArrow = () => {
    return <button className="slick-arrow slick-prev">Previous</button>;
  };

  const CustomNextArrow = () => {
    return <button className="slick-arrow slick-next">Next</button>;
  };

  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    prevArrow: <CustomPrevArrow />,
    nextArrow: <CustomNextArrow />,
  };

  return (
    <section className="carousel-section">
      <h2 className="section-title">Featured Products</h2>
      <Slider {...settings}>
        <div>
          <Link to="/product1">
            <img
              src="https://via.placeholder.com/500x300?text=Funko+Pop+1"
              alt="Funko Pop 1"
            />
          </Link>
        </div>
        <div>
          <Link to="/product2">
            <img
              src="https://via.placeholder.com/500x300?text=Funko+Pop+2"
              alt="Funko Pop 2"
            />
          </Link>
        </div>
        <div>
          <Link to="/product3">
            <img
              src="https://via.placeholder.com/500x300?text=Funko+Pop+3"
              alt="Funko Pop 3"
            />
          </Link>
        </div>
        <div>
          <Link to="/product4">
            <img
              src="https://via.placeholder.com/500x300?text=Funko+Pop+4"
              alt="Funko Pop 4"
            />
          </Link>
        </div>
      </Slider>
    </section>
  );
};

export default CarouselSection;
