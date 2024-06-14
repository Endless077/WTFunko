import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Navbar } from "../../Navbar";
import "./ProductInfo.css";

//TODO : When switching to real backend, change product.thumbnail into product.image
const ProductInfo = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [cart, setCart] = useState([]);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await fetch(`http://localhost:8000/getProduct/${id}`);
        const data = await response.json();
        setProduct(data);
      } catch (error) {
        console.error("Error fetching product:", error);
      }
    };

    fetchProduct();
  }, [id]);

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
      (item) => item.id === product.id
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

  const handleQuantityChange = (productId, quantity) => {
    const updatedCart = cart.map((item) =>
      item.id === productId ? { ...item, quantity } : item
    );
    setCart(updatedCart);
    localStorage.setItem("cart", JSON.stringify(updatedCart));
  };

  if (!product) {
    return <div>Loading...</div>;
  }

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
                height={400}
              />
            </div>
          </div>
          <div className="col-md-6 d-flex flex-column justify-content-center">
            {/*TODO : AGGIUNGERE L' h2 CON L'INTEREST DEL PRODOTTO (LISTA)*/}
            {/*TODO : AGGIUNGERE L' h3 CON IL PRODUCT TYPE DEL PRODOTTO (LISTA)*/}
            <h1 className="display-5">{product.title}</h1>
            <p className="lead">{product.description}</p>
            <h3 className="my-4">${product.price}</h3>
            {cart.some((item) => item.id === product.id) ? (
              <div>
                <button
                  className="btn btn-dark btn-block mb-2"
                  onClick={() => addToCart(product, 1)}
                >
                  In Cart
                </button>
                <select
                  className="form-select mb-2"
                  value={cart.find((item) => item.id === product.id).quantity}
                  onChange={(e) =>
                    handleQuantityChange(product.id, +e.target.value)
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
        {/*TODO : AGGIUNGERE LA PARTE IN CUI FA VEDERE LE IMMAGINI DEI FUNKO RELATED (ID)*/}
      </div>
    </>
  );
};

export default ProductInfo;
