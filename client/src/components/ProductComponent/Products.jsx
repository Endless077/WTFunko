import { useState, useEffect } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { FaSearch } from "react-icons/fa";
import React from "react";

import "./Products.css";
import { config, getApiUrl } from "../../utils";

export const Products = () => {
  const uniqueProductsCountKey = "Unique Products Count Result";

  const location = useLocation();
  const navigate = useNavigate();

  const queryParams = new URLSearchParams(location.search);
  const currentPage = parseInt(queryParams.get("page")) || 0;
  const currentCategory = queryParams.get("category") || "All";
  const currentSearchTerm = queryParams.get("searchTerm") || "";

  const [products, setProducts] = useState([]);

  const [loading, setLoading] = useState(true);
  const [cart, setCart] = useState([]);

  const [productsPerPage] = useState(20);
  const [sortCriteria, setSortCriteria] = useState("default");
  const [searchTerm, setSearchTerm] = useState("");

  // Gets the amount of unique products.
  useEffect(() => {
    const getProducts = async () => {
      try {
        const uniqueProductsCountFetchUrl = getApiUrl(
          config.endpoints.getUniqueProductsCount.url
        );

        const queryAppend = `?category=${currentCategory}&searchTerm=${currentSearchTerm}`;

        const uniqueProductsCountFetch = await fetch(
          uniqueProductsCountFetchUrl + queryAppend,
          { method: config.endpoints.getUniqueProductsCount.method }
        );

        const uniqueProductsCountResult = await uniqueProductsCountFetch.json();
        localStorage.setItem(uniqueProductsCountKey, uniqueProductsCountResult);
        // TODO: This can trigger an error if it ends before the counting of the products (for the rendering).
        setLoading(false);
      } catch (error) {
        console.error("Error fetching page products:", error);
      }
    };

    getProducts();
  }, [currentCategory, currentSearchTerm]);

  // Fetch the products from the current page.
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const pageProductsFetchUrl = getApiUrl(
          config.endpoints.getProductsFromPage.url
        );

        const queryAppend = `?category=${currentCategory}&searchTerm=${currentSearchTerm}&pageIndex=${currentPage}`;

        const pageProductsFetch = await fetch(
          pageProductsFetchUrl + queryAppend,
          { method: config.endpoints.getProductsFromPage.method }
        );

        const pageProductsResult = await pageProductsFetch.json();
        setProducts(pageProductsResult);
      } catch (error) {
        console.error("Error fetching page products:", error);
      }
    };

    if (currentPage !== null) {
      fetchProducts();
    }
  }, [currentCategory, currentSearchTerm, currentPage]);

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
      (item) => item._id === product._id
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
        sortedProducts = products;
        break;
    }
  };

  const handlePageChange = async (
    category = currentCategory,
    searchTerm = currentSearchTerm,
    pageIndex = currentPage
  ) => {
    if (category !== currentCategory || searchTerm !== currentSearchTerm) {
      // Reset the page index when we change category.
      pageIndex = 0;
    }
    navigate(
      `?category=${category}&searchTerm=${searchTerm}&page=${pageIndex}`
    );
  };

  const Loading = () => {
    return <>Loading...</>;
  };

  const handleQuantityChange = (productId, quantity) => {
    const updatedCart = cart.map((item) =>
      item._id === productId ? { ...item, quantity } : item
    );
    setCart(updatedCart);
    localStorage.setItem("cart", JSON.stringify(updatedCart));
  };

  const ShowProducts = () => {
    const uniqueProductsCountResult = localStorage.getItem(
      uniqueProductsCountKey
    );
    const totalPages = Math.ceil(uniqueProductsCountResult / productsPerPage);
    const maxPageDisplay = 10;
    const startPage = Math.floor(currentPage / maxPageDisplay) * maxPageDisplay;
    const endPage = Math.min(startPage + maxPageDisplay, totalPages);

    return (
      <>
        {products.length === 0 ? (
          <p>No products available</p>
        ) : (
          <div className="row">
            {products.map((product) => (
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
                    <h5 className="card-title mb-0">{product.title}</h5>
                    <p className="card-text lead fw-bold">${product.price}</p>
                    {cart.some((item) => item._id === product._id) ? (
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
                            cart.find((item) => item._id === product._id)
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
          {startPage > 0 && (
            <span
              className="page-arrow"
              onClick={() =>
                handlePageChange(
                  currentCategory,
                  currentSearchTerm,
                  startPage - 1
                )
              }
            >
              &laquo;
            </span>
          )}
          {[...Array(endPage - startPage).keys()].map((number) => (
            <button
              key={startPage + number}
              onClick={() =>
                handlePageChange(
                  currentCategory,
                  currentSearchTerm,
                  startPage + number
                )
              }
              className={`page-item ${
                currentPage === startPage + number ? "active" : ""
              }`}
            >
              {startPage + number + 1}
            </button>
          ))}
          {endPage < totalPages && (
            <span
              className="page-arrow"
              onClick={() =>
                handlePageChange(currentCategory, currentSearchTerm, endPage)
              }
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
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      handlePageChange(currentCategory, searchTerm);
                    }
                  }}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
                <button
                  className="custom-search-button"
                  type="button"
                  onClick={() => handlePageChange(currentCategory, searchTerm)}
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
              <button
                className={`btn btn-outline-dark me-2 ${
                  currentCategory === "All" ? "active" : ""
                }`}
                onClick={() => handlePageChange("All")}
              >
                All
              </button>
              <button
                className={`btn btn-outline-dark me-2 ${
                  currentCategory === "Disney" ? "active" : ""
                }`}
                onClick={() => handlePageChange("Disney")}
              >
                Disney
              </button>
              <button
                className={`btn btn-outline-dark me-2 ${
                  currentCategory === "Sports" ? "active" : ""
                }`}
                onClick={() => handlePageChange("Sports")}
              >
                Sports
              </button>
              <button
                className={`btn btn-outline-dark me-2 ${
                  currentCategory === "Marvel" ? "active" : ""
                }`}
                onClick={() => handlePageChange("Marvel")}
              >
                Marvel
              </button>
              <button
                className={`btn btn-outline-dark me-2 ${
                  currentCategory === "Anime" ? "active" : ""
                }`}
                onClick={() => handlePageChange("Anime")}
              >
                Anime
              </button>
              <button
                className={`btn btn-outline-dark me-2 ${
                  currentCategory === "Star Wars" ? "active" : ""
                }`}
                onClick={() => handlePageChange("Star Wars")}
              >
                Star Wars
              </button>
              <button
                className={`btn btn-outline-dark me-2 ${
                  currentCategory === "Pixar" ? "active" : ""
                }`}
                onClick={() => handlePageChange("Pixar")}
              >
                Pixar
              </button>
              <button
                className={`btn btn-outline-dark me-2 ${
                  currentCategory === "Harry Potter" ? "active" : ""
                }`}
                onClick={() => handlePageChange("Harry Potter")}
              >
                Harry Potter
              </button>
              <button
                className={`btn btn-outline-dark me-2 ${
                  currentCategory === "Pokémon" ? "active" : ""
                }`}
                onClick={() => handlePageChange("Pokémon")}
              >
                Pokémon
              </button>
              <button
                className={`btn btn-outline-dark me-2 ${
                  currentCategory === "Music" ? "active" : ""
                }`}
                onClick={() => handlePageChange("Music")}
              >
                Music
              </button>
              <button
                className={`btn btn-outline-dark me-2 ${
                  currentCategory === "Video Games" ? "active" : ""
                }`}
                onClick={() => handlePageChange("Video Games")}
              >
                Video Games
              </button>
            </div>
            <div className="sort-options">
              <label>Sort by:</label>
              <select
                className="form-select"
                value={sortCriteria}
                onChange={handlePageChange}
              >
                <option value="default">Default</option>
                <option value="price-asc">Price: Low to High</option>
                <option value="price-desc">Price: High to Low</option>
                <option value="name-asc">Name: A to Z</option>
                <option value="name-desc">Name: Z to A</option>
              </select>
            </div>
          </div>
        </div>
        {loading ? <Loading /> : <ShowProducts />}
      </div>
    </div>
  );
};
