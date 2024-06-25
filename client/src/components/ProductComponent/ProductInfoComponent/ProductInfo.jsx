// ProductInfo Component
import React, { useEffect, useState } from "react";
import { Navbar } from "../../Navbar";
import { Link, useParams, useNavigate } from "react-router-dom";

// Utils
import "./ProductInfo.css";
import Swal from "sweetalert2";
import { config, fetchData } from "../../../utils";

const ProductInfo = () => {
  const { id } = useParams();
  const [cart, setCart] = useState([]);
  const [product, setProduct] = useState(null);
  const [relatedProducts, setRelatedProducts] = useState([]);

  const navigate = useNavigate();

  /* ********************************************************************************************* */

  useEffect(() => {
    const fetchProducts = async () => {
      const mainProduct = await fetchProduct(id);
      const relProducts = await fetchRelatedProducts(mainProduct);
      setProduct(mainProduct);
      setRelatedProducts(relProducts);
    };

    try {
      fetchProducts();
    } catch (error) {
      console.error("Error fetching product:", error);
    }
  }, [id]);

  useEffect(() => {
    const fetchCart = () => {
      const storedCart = JSON.parse(localStorage.getItem("cart")) || [];
      setCart(storedCart);
    };
    fetchCart();
  }, []);

  const fetchProduct = async (productId) => {
    try {
      const endpointUrl = config.endpoints.getByID.url;
      const method = config.endpoints.getByID.method;
      const pathParams = {
        product_id: productId,
      };

      const getProductResponse = await fetchData(
        endpointUrl,
        method,
        undefined,
        pathParams
      );

      const getProductResponseData = await getProductResponse.json();

      if (!getProductResponse.ok) {
        throw new Error(
          getProductResponseData.detail ||
            "Product loading failed. Please try again later."
        );
      }
      return getProductResponseData;
    } catch (error) {
      console.error("Error product fetch:", error);
      Swal.fire({
        icon: "error",
        title: "Error during product loading",
        text: error.message,
      });
    }
  };

  const fetchRelatedProducts = async (mainProduct) => {
    const relatedProductsIds = mainProduct.related.slice(0, 3);
    const relProducts = [];
    for (let i = 0; i < relatedProductsIds.length; i++) {
      const relatedProduct = await fetchProduct(relatedProductsIds[i]);
      relProducts[i] = relatedProduct;
    }
    return relProducts;
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
          title: "Maximum Reached",
          text: `You can add up to a maximum of ${product.quantity} units.`,
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
          text: `You reached the in stock limit (${maxQuantity}) for this product.`,
        });
        updatedCart = [...cart, { ...product, cartQuantity: product.quantity }];
      } else {
        updatedCart = [...cart, { ...product, cartQuantity: quantity }];
      }
    }
    setCart(updatedCart);
    localStorage.setItem("cart", JSON.stringify(updatedCart));
  };

  const handleCategoryClick = (category) => {
    navigate(
      `/?category=${category}&searchTerm=&sortingCriteria=Default&page=0`
    );
  };

  const handleProductTypeClick = (product_type) => {
    navigate(
      `/?category=&searchTerm=${product_type}&sortingCriteria=Default&page=0`
    );
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

  if (!product) {
    return <div>Loading...</div>;
  }

  /* ********************************************************************************************* */

  return (
    <>
      <Navbar />
      <div className="container my-3 py-3">
        <div className="row">
          <div className="col-md-6">
            <div className="card h-100 text-center p-4 border-3">
              <img
                src={product.img}
                className="card-img-top"
                alt={product.title}
                onError={(e) =>
                  (e.target.src = "/assets/Funko_Placeholder.png")
                }
              />
            </div>
          </div>
          <div className="col-md-6 d-flex flex-column justify-content-center">
            <h1 className="fixed-height-text">{product.title}</h1>
            <div>
              <button
                onClick={() => handleCategoryClick(product.interest[0])}
                className="btn btn-link p-0"
              >
                <h5>{product.interest[0]}</h5>
              </button>
            </div>
            <div>
              <button
                onClick={() => handleProductTypeClick(product.product_type)}
                className="btn btn-link p-0"
              >
                <h5>{product.product_type}</h5>
              </button>
            </div>
            <div className="fixed-height-description">
              <p className="lead">{product.description}</p>
            </div>
            <h3 className="my-2">${product.price}</h3>
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
                      cart.find((item) => item._id === product._id).cartQuantity
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
            <div className="row mt-3">
              <h3>Related Products</h3>
              {relatedProducts.length > 0 ? (
                relatedProducts.map((relatedProduct) => (
                  <div key={relatedProduct._id} className="col-md-4">
                    <div className="card h-100 text-center p-4">
                      <Link to={`/productInfo/${relatedProduct._id}`}>
                        <img
                          src={relatedProduct.img}
                          className="card-img-top"
                          alt={relatedProduct.title}
                          style={{ cursor: "pointer" }}
                          onError={(e) =>
                            (e.target.src = "/assets/Funko_Placeholder.png")
                          }
                        />
                      </Link>
                    </div>
                  </div>
                ))
              ) : (
                <p className="no-related">No Funko Pop related</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ProductInfo;
