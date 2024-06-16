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

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [cart, setCart] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [productsPerPage] = useState(20);
  const [sortCriteria, setSortCriteria] = useState("default");
  const [activeCategory, setActiveCategory] = useState("All");

  // Gets the amount of unique products.
  useEffect(() => {
    const getProducts = async () => {
      try {
        setLoading(true);

        const uniqueProductsCountFetch = await fetch(
          getApiUrl(config.endpoints.getUniqueProductsCount.url),
          { method: config.endpoints.getUniqueProductsCount.method }
        );

        const uniqueProductsCountResult = await uniqueProductsCountFetch.json();
        localStorage.setItem(uniqueProductsCountKey, uniqueProductsCountResult);

        setLoading(false);
      } catch (error) {
        console.error("Error fetching page products:", error);
      }
    };

    getProducts();
  }, [currentPage]);

  // Fetch the products from the current page.
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const pageProductsFetchUrl = getApiUrl(
          config.endpoints.getProductsFromPage.url
        );
        
        const pageProductsFetch = await fetch(
          pageProductsFetchUrl.replace("{pageIndex}", currentPage),
          { method: config.endpoints.getProductsFromPage.method }
        );

        const pageProductsResult = await pageProductsFetch.json();
        setData(pageProductsResult);
      } catch (error) {
        console.error("Error fetching page products:", error);
      }
    };

    if (currentPage !== null) {
      fetchProducts();
    }
  }, [currentPage]);

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

  const filterProducts = (cat) => {
    setActiveCategory(cat);
    if (cat === "All") {
      setSearchTerm("");
    } else {
      if (searchTerm.trim() === "") {
        const updatedList = data.filter((x) => x.interest[0] === cat);
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
  };

  const handleSortChange = (e) => {
    setSortCriteria(e.target.value);
    sortProducts(e.target.value);
  };

  const handlePageChange = async (pageIndex) => {
    navigate(`?page=${pageIndex}`);
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
        {data.length === 0 ? (
          <p>No products available</p>
        ) : (
          <div className="row">
            {data.map((product) => (
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
              onClick={() => handlePageChange(startPage - 1)}
            >
              &laquo;
            </span>
          )}
          {[...Array(endPage - startPage).keys()].map((number) => (
            <button
              key={startPage + number}
              onClick={() => handlePageChange(startPage + number)}
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
              onClick={() => handlePageChange(endPage)}
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
              <button
                className={`btn btn-outline-dark me-2 ${
                  activeCategory === "All" ? "active" : ""
                }`}
                onClick={() => filterProducts("All")}
              >
                All
              </button>
              <button
                className={`btn btn-outline-dark me-2 ${
                  activeCategory === "Disney" ? "active" : ""
                }`}
                onClick={() => filterProducts("Disney")}
              >
                Disney
              </button>
              <button
                className={`btn btn-outline-dark me-2 ${
                  activeCategory === "Sports" ? "active" : ""
                }`}
                onClick={() => filterProducts("Sports")}
              >
                Sports
              </button>
              <button
                className={`btn btn-outline-dark me-2 ${
                  activeCategory === "Marvel" ? "active" : ""
                }`}
                onClick={() => filterProducts("Marvel")}
              >
                Marvel
              </button>
              <button
                className={`btn btn-outline-dark me-2 ${
                  activeCategory === "Anime" ? "active" : ""
                }`}
                onClick={() => filterProducts("Anime")}
              >
                Anime
              </button>
              <button
                className={`btn btn-outline-dark me-2 ${
                  activeCategory === "Star Wars" ? "active" : ""
                }`}
                onClick={() => filterProducts("Star Wars")}
              >
                Star Wars
              </button>
              <button
                className={`btn btn-outline-dark me-2 ${
                  activeCategory === "Pixar" ? "active" : ""
                }`}
                onClick={() => filterProducts("Pixar")}
              >
                Pixar
              </button>
              <button
                className={`btn btn-outline-dark me-2 ${
                  activeCategory === "Harry Potter" ? "active" : ""
                }`}
                onClick={() => filterProducts("Harry Potter")}
              >
                Harry Potter
              </button>
              <button
                className={`btn btn-outline-dark me-2 ${
                  activeCategory === "Pokémon" ? "active" : ""
                }`}
                onClick={() => filterProducts("Pokémon")}
              >
                Pokémon
              </button>
              <button
                className={`btn btn-outline-dark me-2 ${
                  activeCategory === "Music" ? "active" : ""
                }`}
                onClick={() => filterProducts("Music")}
              >
                Music
              </button>
              <button
                className={`btn btn-outline-dark me-2 ${
                  activeCategory === "Video Games" ? "active" : ""
                }`}
                onClick={() => filterProducts("Video Games")}
              >
                Video Games
              </button>
            </div>
            <div className="sort-options">
              <label>Sort by:</label>
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
        </div>
        {loading ? <Loading /> : <ShowProducts />}
      </div>
    </div>
  );
};
