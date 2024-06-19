// Cart Component
import React, { useState, useEffect } from "react";
import { Navbar } from "../Navbar";
import { Link, useNavigate } from "react-router-dom";

// Utils
import "./Cart.css";
import Swal from "sweetalert2";
import { config, fetchData } from "../../utils";

const CartPage = () => {
  const VAT_RATE = 0.22;
  const SHIPPING_COST = 6.99;
  const FREE_SHIPPING_THRESHOLD = 100;

  const [cart, setCart] = useState([]);
  const navigate = useNavigate();

  /* ********************************************************************************************* */

  useEffect(() => {
    const storedCart = JSON.parse(localStorage.getItem("cart")) || [];
    setCart(storedCart);
  }, []);

  const updateQuantity = (productId, newQuantity) => {
    const updatedCart = cart.map((item) => {
      if (item._id === productId) {
        const maxQuantity = item.quantity;
        if (newQuantity > maxQuantity) {
          Swal.fire({
            icon: "warning",
            title: "Oh no...this is too much for us",
            text: `You reached the in stock limit (${maxQuantity}) for this product.`,
          });
          newQuantity = maxQuantity;
        } else if (newQuantity < 1) {
          newQuantity = 1;
        }
        return { ...item, cartQuantity: newQuantity };
      }
      return item;
    });

    setCart(updatedCart);
    localStorage.setItem("cart", JSON.stringify(updatedCart));
  };

  const clearCart = () => {
    Swal.fire({
      title: "Clear Cart",
      text: "Are you sure you want to remove all items from your cart?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, clear it!",
    }).then((result) => {
      if (result.isConfirmed) {
        setCart([]);
        localStorage.removeItem("cart");
        Swal.fire("Cleared!", "Your cart has been cleared.", "success");
      }
    });
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

    const total = parseFloat((subtotal + vat + SHIPPING_COST).toFixed(2));
    return total;
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

    const total = calculateTotal();

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
        const payload = newOrder;

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
            navigate("/login");
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
        <h6>(for orders over $100 free shipping)</h6>
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
                      <div className="cart-quantity-control">
                        <button
                          className="btn btn-sm btn-primary"
                          onClick={() =>
                            updateQuantity(item._id, item.cartQuantity - 1)
                          }
                        >
                          -
                        </button>
                        <span className="cart-quantity">
                          {item.cartQuantity}
                        </span>
                        <button
                          className="btn btn-sm btn-primary"
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
            <button className="btn btn-danger mt-3" onClick={clearCart}>
              Clear Cart
            </button>
            <div className="cart-container mt-5">
              <table className="cart-table">
                <tfoot>
                  <tr>
                    <td colSpan="4" className="text-end fw-bold">
                      Subtotal:
                    </td>
                    <td>${calculateSubtotal().toFixed(2)}</td>
                    <td></td>
                  </tr>
                  <tr>
                    <td colSpan="4" className="text-end fw-bold">
                      VAT (22%):
                    </td>
                    <td>${calculateVat().toFixed(2)}</td>
                    <td></td>
                  </tr>
                  <tr>
                    <td colSpan="4" className="text-end fw-bold">
                      Shipping Cost:
                    </td>
                    <td>
                      {calculateSubtotal() > FREE_SHIPPING_THRESHOLD ? (
                        <span
                          className="text-success"
                          style={{ whiteSpace: "nowrap" }}
                        >
                          Free Shipping
                        </span>
                      ) : (
                        `$${SHIPPING_COST.toFixed(2)}`
                      )}
                    </td>
                    <td></td>
                  </tr>
                  <tr>
                    <td colSpan="4" className="text-end fw-bold">
                      Total:
                    </td>
                    <td>${calculateTotal()}</td>
                    <td></td>
                  </tr>
                  <tr>
                    <td colSpan="6" className="text-end">
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
