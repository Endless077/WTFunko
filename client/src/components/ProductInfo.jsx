// components/ProductInfo.jsx
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Navbar } from "./Navbar";
import "./ProductInfo.css";

const ProductInfo = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await fetch(`https://fakestoreapi.com/products/${id}`);
        const data = await response.json();
        setProduct(data);
      } catch (error) {
        console.error("Error fetching product:", error);
      }
    };

    fetchProduct();
  }, [id]);

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
                src={product.image}
                className="card-img-top"
                alt={product.title}
                height={400}
              />
            </div>
          </div>
          <div className="col-md-6 d-flex flex-column justify-content-center">
            <h1 className="display-5">{product.title}</h1>
            <p className="lead">{product.description}</p>
            <h3 className="my-4">${product.price}</h3>
            <button className="btn btn-outline-dark">Add to Cart</button>
          </div>
        </div>
      </div>
    </>
  );
};

export default ProductInfo;
