// ProductInfo Component
import React, { useEffect, useState } from "react";
import { Navbar } from "../../Navbar";
import { useParams } from "react-router-dom";

// Utils
import "./ProductInfo.css";
import Swal from "sweetalert2";
import { config, fetchData } from "../../../utils";

const ProductInfo = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [cart, setCart] = useState([]);

  /* ********************************************************************************************* */

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const endpointUrl = config.endpoints.getByID.url;
        const method = config.endpoints.getByID.method;
        const pathParams = {
          product_id: id,
        };

        const getProductResponse = await fetchData(
          endpointUrl,
          method,
          undefined,
          pathParams
        );

        if (!getProductResponse.ok) {
          throw new Error(
            getProductResponse.detail ||
              "Product loading failed. Please try again later."
          );
        }

        const getProductData = await getProductResponse.json();
        setProduct(getProductData);
      } catch (error) {
        console.error("Error product fetch:", error);
        Swal.fire({
          icon: "error",
          title: "Error during product loading",
          text: error.message,
        });
      }
    };

    try {
      fetchProduct();
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
      <div className="container my-5 py-5">
        <div className="row">
          <div className="col-md-6">
            <div className="card h-100 text-center p-4">
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
            {/*TODO : AGGIUNGERE L' h2 CON L'INTEREST DEL PRODOTTO (LISTA)*/}
            {/*TODO : AGGIUNGERE L' h3 CON IL PRODUCT TYPE DEL PRODOTTO (LISTA)*/}
            <h1 className="display-5">{product.title}</h1>
            <p className="lead">{product.description}</p>
            <h3 className="my-4">${product.price}</h3>
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
          </div>
        </div>
        {/*TODO : AGGIUNGERE LA PARTE IN CUI FA VEDERE LE IMMAGINI DEI FUNKO RELATED (ID)*/}
      </div>
    </>
  );
};

export default ProductInfo;
