// Cart Component
import React, { useState, useEffect } from "react";
import { Navbar } from "../Navbar";
import Swal from "sweetalert2";
import { Link, useNavigate } from "react-router-dom";

// Utils
import { config, getApiUrl } from "../../utils";
import "./Cart.css";

const CartPage = () => {
  const VAT_RATE = 0.22;
  const SHIPPING_COST = 5.0;
  const [cart, setCart] = useState([]);

  const navigate = useNavigate();

  /* ********************************************************************************************* */

  useEffect(() => {
    const storedCart = JSON.parse(localStorage.getItem("cart")) || [];
    setCart(storedCart);
  }, []);

  const updateQuantity = (productId, newQuantity) => {
    newQuantity = Math.max(newQuantity, 1);

    const updatedCart = cart.map((item) => {
      if (item._id === productId) {
        return { ...item, cartQuantity: newQuantity };
      }
      return item;
    });

    setCart(updatedCart);
    localStorage.setItem("cart", JSON.stringify(updatedCart));
  };

  const removeFromCart = (productId) => {
    Swal.fire({
      title: "Are you sure?",
      text: "You won't be able to revert this!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, remove it!",
    }).then((result) => {
      if (result.isConfirmed) {
        const updatedCart = cart.filter((item) => item._id !== productId);
        setCart(updatedCart);
        localStorage.setItem("cart", JSON.stringify(updatedCart));
        Swal.fire("Removed!", "Your item has been removed.", "success");
      }
    });
  };

  const calculateSubtotal = () => {
    return cart.reduce(
      (total, item) => total + item.price * item.cartQuantity,
      0
    );
  };

  const calculateVat = () => {
    return calculateSubtotal() * VAT_RATE;
  };

  const calculateTotal = () => {
    const subtotal = calculateSubtotal();
    const vat = calculateVat();
    const total = subtotal + vat + SHIPPING_COST;
    return total.toFixed(2);
  };

  const makeOrder = (user, products) => {
    const currentDate = new Date().toISOString();

    const orderProducts = products.map((product) => ({
      product: {
        id: product._id,
        title: product.title,
        product_type: product.product_type,
        price: product.price,
        amount: product.cartQuantity,
        description: product.description,
        img: product.img,
      },
    }));

    const total = products.reduce(
      (sum, product) => sum + product.price * product.cartQuantity,
      0
    );

    const newOrder = {
      user: {
        id: user._id,
        username: user.username,
        email: user.email,
      },
      products: orderProducts,
      total: total,
      date: currentDate,
      status: "Evaso",
    };

    return newOrder;
  };

  const handlePayment = () => {
    const sendOrder = async (newOrder) => {
      try {
        const endpointUrl = config.endpoints.insertOrder.url;
        const method = config.endpoints.insertOrder.method;
        const payload = newOrder

        const insertOrderResponse = await fetchData(
          endpointUrl,
          method,
          null,
          payload
        );

        if (!insertOrderResponse.ok) {
          throw new Error(
            insertOrderResponse.detail ||
              "Order failed. Please try again later."
          );
        }

        Swal.fire({
          icon: "success",
          title: "Payment Done",
          text: `Thank you for your order!`,
          timer: 3000,
          timerProgressBar: true,
          showConfirmButton: false,
          allowOutsideClick: false,
          willClose: () => {
            navigate("/profile");
          },
        });
      } catch (error) {
        console.error("Error creating current order:", error);
        Swal.fire({
          icon: "error",
          title: "Order Error",
          text: error.detail,
        });
      }
    };

    try {
      const currentUser = localStorage.getItem("user");
      if (currentUser == null) {
        Swal.fire({
          icon: "error",
          title: "Account Needed",
          text: "You need an account to buy something.",
          timer: 3000,
          timerProgressBar: true,
          showConfirmButton: false,
          allowOutsideClick: false,
          willClose: () => {
            navigate("/");
          },
        });
      } else {
        const newOrder = makeOrder(currentUser, cart);
        sendOrder(newOrder);
      }
    } catch (error) {
      console.error("Error during login:", error);
    }
  };

  /* ********************************************************************************************* */

  return (
    <>
      <Navbar />
      <div className="container mt-5">
        <h2>Shopping Cart</h2>
        {cart.length === 0 ? (
          <p>Your cart is empty.</p>
        ) : (
          <>
            <table className="table">
              <thead>
                <tr>
                  <th>Product Image</th>
                  <th>Product Name</th>
                  <th>Price</th>
                  <th>Amount</th>
                  <th>Total</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {cart.map((item) => (
                  <tr key={item._id}>
                    <td>
                      <div className="d-flex align-items-center">
                        <Link to={`/productInfo/${item._id}`}>
                          <img
                            src={item.img}
                            alt={item.name}
                            style={{ marginRight: "10px", width: "50px" }}
                          />
                        </Link>
                      </div>
                    </td>
                    <td>{item.title}</td>
                    <td>${item.price.toFixed(2)}</td>
                    <td>
                      <div className="d-flex align-items-center">
                        <button
                          className="btn btn-sm btn-primary me-2"
                          onClick={() =>
                            updateQuantity(item._id, item.cartQuantity - 1)
                          }
                        >
                          -
                        </button>
                        <span>{item.cartQuantity}</span>
                        <button
                          className="btn btn-sm btn-primary ms-2"
                          onClick={() =>
                            updateQuantity(item._id, item.cartQuantity + 1)
                          }
                        >
                          +
                        </button>
                      </div>
                    </td>
                    <td>${(item.price * item.cartQuantity).toFixed(2)}</td>
                    <td>
                      <button
                        className="btn btn-danger"
                        onClick={() => removeFromCart(item._id)}
                      >
                        Remove
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div className="cart-container mt-5">
              <table className="cart-table">
                <tfoot>
                  <tr>
                    <td colSpan="4" className="text-end">
                      {" "}
                      Subtotal:
                    </td>
                    <td>${calculateSubtotal().toFixed(2)}</td>
                    <td></td>
                  </tr>
                  <tr>
                    <td colSpan="4" className="text-end">
                      {" "}
                      VAT (22%):
                    </td>
                    <td>${calculateVat().toFixed(2)}</td>
                    <td></td>
                  </tr>
                  <tr>
                    <td colSpan="4" className="text-end">
                      {" "}
                      Shipping Cost:
                    </td>
                    <td>${SHIPPING_COST.toFixed(2)}</td>
                    <td></td>
                  </tr>
                  <tr>
                    <td colSpan="4" className="text-end">
                      {" "}
                      Total:
                    </td>
                    <td>${calculateTotal()}</td>
                    <td></td>
                  </tr>
                  <tr>
                    <td colSpan="4" className="text-end">
                      {" "}
                      <button
                        className="btn btn-success cart-button"
                        onClick={handlePayment}
                      >
                        Buy Now
                      </button>
                    </td>
                  </tr>
                </tfoot>
              </table>
            </div>
          </>
        )}
      </div>
    </>
  );
};

export default CartPage;
