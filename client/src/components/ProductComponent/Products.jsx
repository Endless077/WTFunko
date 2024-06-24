// Products Component
import React from "react";
import { FaSearch } from "react-icons/fa";
import { useState, useEffect } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

// Utils
import "./Products.css";
import Swal from "sweetalert2";
import { Criteria } from "../enumerations";
import { config, fetchData } from "../../utils";

export const Products = () => {
  const uniqueProductsCountKey = "Products Count";

  const location = useLocation();
  const navigate = useNavigate();

  const queryParams = new URLSearchParams(location.search);

  const currentPage = parseInt(queryParams.get("page")) || 0;
  const currentCategory = queryParams.get("category") || "All";
  const currentSearchTerm = queryParams.get("searchTerm") || "";
  const currentSortingCriteria = queryParams.get("sortingCriteria") || Criteria.DEFAULT;

  const [cart, setCart] = useState([]);
  const [productsPerPage] = useState(20);
  const [searchTerm, setSearchTerm] = useState("");

  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  /* ********************************************************************************************* */

  useEffect(() => {
    const getUniqueProductsCount = async () => {
      try {
        const endpointUrl = config.endpoints.getUniqueProductsCount.url;
        const method = config.endpoints.getUniqueProductsCount.method;
        const queryParams = {
          category: currentCategory,
          searchTerm: currentSearchTerm,
        };

        const uniqueProductsCountResponse = await fetchData(
          endpointUrl,
          method,
          queryParams
        );

        const uniqueProductsCount = await uniqueProductsCountResponse.json();
        localStorage.setItem(uniqueProductsCountKey, uniqueProductsCount);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching page counter:", error);
        Swal.fire({
          icon: "error",
          title: "Error during resources loading",
          text: error.message,
        });
      }
    };

    getUniqueProductsCount();
  }, [currentCategory, currentSearchTerm]);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const endpointUrl = config.endpoints.getProducts.url;
        const method = config.endpoints.getProducts.method;
        const queryParams = {
          category: currentCategory,
          searchTerm: currentSearchTerm,
          sortingCriteria: currentSortingCriteria,
          pageIndex: currentPage,
        };
        const productsResponse = await fetchData(
          endpointUrl,
          method,
          queryParams
        );

        const products = await productsResponse.json();
        setProducts(products);
      } catch (error) {
        console.error("Error fetching page products:", error);
        Swal.fire({
          icon: "error",
          title: "Error during resources loading",
          text: error.message,
        });
      }
    };

    currentPage !== null && fetchProducts();
  }, [currentCategory, currentSearchTerm, currentSortingCriteria, currentPage]);

  useEffect(() => {
    const fetchCart = () => {
      const storedCart = JSON.parse(localStorage.getItem("cart")) || [];
      setCart(storedCart);
    };
    fetchCart();
  }, []);

  /* ********************************************************************************************* */

  const Loading = () => {
    return <>Loading...</>;
  };

  const addToCart = (product, quantity = 1) => {
    let updatedCart;
    const existingProductIndex = cart.findIndex(
      (item) => item._id === product._id
    );
    if (existingProductIndex !== -1) {
      updatedCart = [...cart];
      const newQuantity =
        updatedCart[existingProductIndex].cartQuantity + quantity;
      if (newQuantity > product.quantity) {
        Swal.fire({
          icon: "warning",
          title: "Oh no...this is too much for us",
          text: `You reached the in stock limit (${product.quantity}) for this product.`,
        });

        updatedCart[existingProductIndex].cartQuantity = product.quantity;
      } else {
        updatedCart[existingProductIndex].cartQuantity = newQuantity;
      }
    } else {
      if (quantity > product.quantity) {
        Swal.fire({
          icon: "warning",
          title: "Oh no...this is too much for us",
          text: `You reached the in stock limit (${product.quantity}) for this product.`,
        });
        updatedCart = [...cart, { ...product, cartQuantity: product.quantity }];
      } else {
        updatedCart = [...cart, { ...product, cartQuantity: quantity }];
      }
    }
    setCart(updatedCart);
    localStorage.setItem("cart", JSON.stringify(updatedCart));
  };

  const handleQuantityChange = (productId, cartQuantity, maxQuantity) => {
    if (cartQuantity > maxQuantity) {
      Swal.fire({
        icon: "warning",
        title: "Oh no...this is too much for us",
        text: `You reached the in stock limit (${maxQuantity}) for this product.`,
      });
      cartQuantity = maxQuantity;
    } else if (cartQuantity < 1) {
      cartQuantity = 1;
    }

    const updatedCart = cart.map((item) =>
      item._id === productId ? { ...item, cartQuantity } : item
    );
    setCart(updatedCart);
    localStorage.setItem("cart", JSON.stringify(updatedCart));
  };

  const handlePageChange = async (
    category = currentCategory,
    searchTerm = currentSearchTerm,
    sortingCriteria = currentSortingCriteria,
    pageIndex = currentPage
  ) => {
    if (category !== currentCategory || searchTerm !== currentSearchTerm) {
      pageIndex = 0;
    }
    navigate(
      `?category=${category}&searchTerm=${searchTerm}&sortingCriteria=${sortingCriteria}&page=${pageIndex}`
    );
  };

  /* ********************************************************************************************* */

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
                      onError={(e) =>
                        (e.target.src = "/assets/Funko_Placeholder.png")
                      }
                    />
                  </Link>
                  <div className="card-body">
                    <h5 className="card-title mb-0">{product.title}</h5>
                    <p className="card-text lead fw-bold">${product.price}</p>
                    {product.quantity > 0 ? (
                      cart.some((item) => item._id === product._id) ? (
                        <div>
                          <button
                            className="btn btn-dark btn-block mb-2"
                            onClick={() => addToCart(product, 1)}
                          >
                            In Cart
                          </button>
                          <input
                            type="number"
                            className="form-control mb-2"
                            value={
                              cart.find((item) => item._id === product._id)
                                .cartQuantity
                            }
                            min="1"
                            max={product.quantity}
                            onChange={(e) =>
                              handleQuantityChange(
                                product._id,
                                +e.target.value,
                                product.quantity
                              )
                            }
                          />
                        </div>
                      ) : (
                        <button
                          className="btn btn-outline-dark btn-block mb-2"
                          onClick={() => addToCart(product, 1)}
                        >
                          Add to Cart
                        </button>
                      )
                    ) : (
                      <p className="text-danger fw-bold mb-0">Out of Stock</p>
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
                  currentSortingCriteria,
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
                handlePageChange(
                  currentCategory,
                  currentSearchTerm,
                  currentSortingCriteria,
                  endPage
                )
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
      <div className="container my-4">
        <div className="row">
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
                  currentCategory === "Anime" ? "active" : ""
                }`}
                onClick={() => handlePageChange("Anime")}
              >
                Anime
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
                  currentCategory === "Harry Potter" ? "active" : ""
                }`}
                onClick={() => handlePageChange("Harry Potter")}
              >
                Harry Potter
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
                  currentCategory === "Music" ? "active" : ""
                }`}
                onClick={() => handlePageChange("Music")}
              >
                Music
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
                  currentCategory === "Pokémon" ? "active" : ""
                }`}
                onClick={() => handlePageChange("Pokémon")}
              >
                Pokémon
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
                  currentCategory === "Star Wars" ? "active" : ""
                }`}
                onClick={() => handlePageChange("Star Wars")}
              >
                Star Wars
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
              <select
                className="form-select"
                value={currentSortingCriteria}
                onChange={(e) =>
                  handlePageChange(
                    currentCategory,
                    currentSearchTerm,
                    e.target.value
                  )
                }
              >
                <option value={Criteria.DEFAULT}>Most Recent</option>
                <option value={Criteria.PRICE_ASCENDING}>
                  Price: Low to High &#x25B2;
                </option>
                <option value={Criteria.PRICE_DESCENDING}>
                  Price: High to Low &#x25BC;
                </option>
                <option value={Criteria.TITLE_ASCENDING}>
                  Title: A to Z &#x25B2;
                </option>
                <option value={Criteria.TITLE_DESCENDING}>
                  Title: Z to A &#x25BC;
                </option>
              </select>
            </div>
          </div>
        </div>
        {loading ? <Loading /> : <ShowProducts />}
      </div>
    </div>
  );
};
