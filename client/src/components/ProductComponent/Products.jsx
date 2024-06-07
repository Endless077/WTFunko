import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { FaSearch } from "react-icons/fa";
import React from "react";
import "./Products.css";

export const Products = () => {
  const [data, setData] = useState([]);
  const [filter, setFilter] = useState([]);
  const [loading, setLoading] = useState(false);
  const [cart, setCart] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [productsPerPage] = useState(20);
  const [sortCriteria, setSortCriteria] = useState("default");

  useEffect(() => {
    const getProducts = async () => {
      setLoading(true);
      const response = await fetch("http://localhost:8000/getAllProducts");
      const result = await response.json();
      setData(result);
      setFilter(result);
      setLoading(false);
    };

    getProducts();
  }, []);

  useEffect(() => {
    const fetchCart = () => {
      const storedCart = JSON.parse(localStorage.getItem("cart")) || [];
      setCart(storedCart);
    };
    fetchCart();
  }, []);

  const addToCart = (product) => {
    let updatedCart;
    const existingProductIndex = cart.findIndex(
      (item) => item.id === product._id
    );
    if (existingProductIndex !== -1) {
      updatedCart = [...cart];
      updatedCart[existingProductIndex].quantity += 1;
    } else {
      updatedCart = [...cart, { ...product, quantity: 1 }];
    }
    setCart(updatedCart);
    localStorage.setItem("cart", JSON.stringify(updatedCart));
  };

  const filterProducts = (cat) => {
    if (cat === "All") {
      setSearchTerm("");
      setFilter(data);
    } else {
      if (searchTerm.trim() === "") {
        const updatedList = data.filter((x) => x.category === cat);
        setFilter(updatedList);
      } else {
        filterProductsByName(searchTerm);
      }
    }
  };

  const handleSearch = () => {
    if (searchTerm.trim() === "") {
      filterProducts("All");
    } else {
      filterProducts("All");
      filterProductsByName(searchTerm);
    }
  };

  const filterProductsByName = (searchTerm) => {
    const filteredProducts = data.filter((product) =>
      product.title.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilter(filteredProducts);
  };

  const sortProducts = (criteria) => {
    let sortedProducts = [...filter];
    switch (criteria) {
      case "price-asc":
        sortedProducts.sort((a, b) => a.price - b.price);
        break;
      case "price-desc":
        sortedProducts.sort((a, b) => b.price - a.price);
        break;
      case "name-asc":
        sortedProducts.sort((a, b) => a.title.localeCompare(b.title));
        break;
      case "name-desc":
        sortedProducts.sort((a, b) => b.title.localeCompare(a.title));
        break;
      default:
        sortedProducts = data;
        break;
    }
    setFilter(sortedProducts);
  };

  const handleSortChange = (e) => {
    setSortCriteria(e.target.value);
    sortProducts(e.target.value);
  };

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const paginate = (products, pageNumber, productsPerPage) => {
    const startIndex = (pageNumber - 1) * productsPerPage;
    const endIndex = startIndex + productsPerPage;
    return products.slice(startIndex, endIndex);
  };

  const Loading = () => {
    return <>Loading...</>;
  };

  const ShowProducts = () => {
    const paginatedProducts = paginate(filter, currentPage, productsPerPage);
    return (
      <>
        {paginatedProducts.length === 0 ? (
          <p>No products available</p>
        ) : (
          <div className="row">
            {paginatedProducts.map((product) => (
              <div key={product._id} className="col-md-3 mb-4">
                <div
                  className="card h-100 text-center p-4"
                  style={{ width: "18rem" }}
                >
                  <Link to={`/productInfo/${product._id}`}>
                    <img
                      src={product.img}
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
                    {cart.some((item) => item.id === product._id) ? (
                      <div>
                        <button
                          className="btn btn-dark btn-block mb-2"
                          onClick={() => addToCart(product, 1)}
                        >
                          In Cart
                        </button>
                        <select
                          className="form-select mb-2"
                          value={
                            cart.find((item) => item.id === product._id)
                              .quantity
                          }
                          onChange={(e) =>
                            handleQuantityChange(product._id, +e.target.value)
                          }
                        >
                          {[...Array(10).keys()].map((number) => (
                            <option key={number + 1} value={number + 1}>
                              {number + 1}
                            </option>
                          ))}
                        </select>
                      </div>
                    ) : (
                      <button
                        className="btn btn-outline-dark btn-block mb-2"
                        onClick={() => addToCart(product, 1)}
                      >
                        Add to Cart
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
        <div className="pagination">
          {currentPage > 1 && (
            <span
              className="page-arrow"
              onClick={() => handlePageChange(currentPage - 1)}
            >
              &laquo;
            </span>
          )}
          {[...Array(Math.ceil(filter.length / productsPerPage)).keys()].map(
            (number) => (
              <button
                key={number + 1}
                onClick={() => handlePageChange(number + 1)}
                className={`page-item ${
                  currentPage === number + 1 ? "active" : ""
                }`}
              >
                {number + 1}
              </button>
            )
          )}
          {currentPage < Math.ceil(filter.length / productsPerPage) && (
            <span
              className="page-arrow"
              onClick={() => handlePageChange(currentPage + 1)}
            >
              &raquo;
            </span>
          )}
        </div>
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
              <div className="custom-search-bar">
                <input
                  type="text"
                  className="custom-search-input"
                  placeholder="Search a Product..."
                  aria-label="Search"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
                <button
                  className="custom-search-button"
                  type="button"
                  onClick={handleSearch}
                >
                  <FaSearch />
                </button>
              </div>
            </div>
          </div>
        </div>
        <div className="row justify-content-center mb-4">
          <div className="category-bar">
            <label>Categories</label>
            <div className="category-buttons">
              {/*TODO : METTERE I FILTRI PER : Disney, Sports, Marvel, Anime, Star Wars, Music, Video Games, Pixar, Harry Potter, Pokémon */}
              <button
                className="btn btn-outline-dark me-2"
                onClick={() => filterProducts("All")}
              >
                All
              </button>
              <button
                className="btn btn-outline-dark me-2"
                onClick={() => filterProducts("smartphones")}
              >
                Disney
              </button>
              <button
                className="btn btn-outline-dark me-2"
                onClick={() => filterProducts("Sports")}
              >
                Sports
              </button>
              <button
                className="btn btn-outline-dark me-2"
                onClick={() => filterProducts("Marvel")}
              >
                Marvel
              </button>
              <button
                className="btn btn-outline-dark me-2"
                onClick={() => filterProducts("Anime")}
              >
                Anime
              </button>
              <button
                className="btn btn-outline-dark me-2"
                onClick={() => filterProducts("Star Wars")}
              >
                Star Wars
              </button>
              <button
                className="btn btn-outline-dark me-2"
                onClick={() => filterProducts("Music")}
              >
                Music
              </button>
              <button
                className="btn btn-outline-dark me-2"
                onClick={() => filterProducts("Video Games")}
              >
                Video Games
              </button>
              <button
                className="btn btn-outline-dark me-2"
                onClick={() => filterProducts("Pixar")}
              >
                Pixar
              </button>
              <button
                className="btn btn-outline-dark me-2"
                onClick={() => filterProducts("Harry Potter")}
              >
                Harry Potter
              </button>
              <button
                className="btn btn-outline-dark me-2"
                onClick={() => filterProducts("Pokémon")}
              >
                Pokémon
              </button>
            </div>
          </div>
          <div className="sort-bar">
            <label>Sort By</label>
            <select
              className="form-select"
              value={sortCriteria}
              onChange={handleSortChange}
            >
              <option value="default">Default</option>
              <option value="price-asc">Price: Low to High</option>
              <option value="price-desc">Price: High to Low</option>
              <option value="name-asc">Name: A to Z</option>
              <option value="name-desc">Name: Z to A</option>
            </select>
          </div>
        </div>
        <div className="row justify-content-center">
          {loading ? <Loading /> : <ShowProducts />}
        </div>
      </div>
    </div>
  );
};

export default Products;
