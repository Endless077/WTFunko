import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { FaSearch } from "react-icons/fa";
import "./Products.css";

export const Products = () => {
  const [data, setData] = useState([]);
  const [filter, setFilter] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const getProducts = async () => {
      setLoading(true);
      const response = await fetch("https://dummyjson.com/products");
      const result = await response.json();
      setData(result.products);
      setFilter(result.products);
      setLoading(false);
    };

    getProducts();
  }, []);

  const filterProducts = (cat) => {
    const updatedList = data.filter((x) => x.category === cat);
    setFilter(updatedList);
  };

  const Loading = () => {
    return <>Loading...</>;
  };

  const ShowProducts = () => {
    return (
      <>
        <div className="buttons d-flex justify-content-center mb-5 pb-5">
          <button
            className="btn btn-outline-dark me-2"
            onClick={() => setFilter(data)}
          >
            All
          </button>
          <button
            className="btn btn-outline-dark me-2"
            onClick={() => filterProducts("smartphones")}
          >
            Smartphones
          </button>
          <button
            className="btn btn-outline-dark me-2"
            onClick={() => filterProducts("laptops")}
          >
            Laptops
          </button>
          <button
            className="btn btn-outline-dark me-2"
            onClick={() => filterProducts("fragrances")}
          >
            Fragrances
          </button>
          <button
            className="btn btn-outline-dark me-2"
            onClick={() => filterProducts("skincare")}
          >
            Skincare
          </button>
        </div>

        {filter.map((product) => (
          <div key={product.id} className="col-md-3 mb-4">
            <div
              className="card h-100 text-center p-4"
              style={{ width: "18rem" }}
            >
              <Link to={`/productInfo/${product.id}`}>
                <img
                  src={product.thumbnail}
                  className="card-img-top"
                  alt={product.title}
                  height="250"
                />
              </Link>
              <div className="card-body">
                <h5 className="card-title mb-0">
                  {product.title.substring(0, 12)}
                </h5>
                <p className="card-text lead fw-bold">${product.price}</p>
                <button className="btn btn-outline-dark">Buy now</button>
              </div>
            </div>
          </div>
        ))}
      </>
    );
  };

  return (
    <div>
      <div className="container my-5 py-5">
        <div className="row">
          <div className="col-12 mb-4 text-center">
            <h1 className="display-6 fw-bolder">Our selection of Products</h1>
          </div>
          <div className="col-12 mb-4 d-flex justify-content-center">
            <div className="search-bar">
              <div className="input-group">
                <input
                  type="text"
                  className="form-control"
                  placeholder="Search a Product..."
                  aria-label="Search"
                  aria-describedby="search-icon"
                />
                <button
                  className="btn btn-outline-dark"
                  type="button"
                  id="search-icon"
                >
                  <FaSearch />
                </button>
              </div>
            </div>
          </div>
        </div>
        <div className="row justify-content-center">
          {loading ? <Loading /> : <ShowProducts />}
        </div>
      </div>
    </div>
  );
};
