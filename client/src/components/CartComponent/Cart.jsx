import { Navbar } from "../Navbar";
import { Link, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import RemoveConfirm from "./RemoveConfirmComponent/RemoveConfirm";
import Swal from "sweetalert2";
import "./Cart.css";

const CartPage = () => {
  const VAT_RATE = 0.22;
  const SHIPPING_COST = 5.0;
  const [cart, setCart] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [productToRemove, setProductToRemove] = useState(null);

  const navigate = useNavigate()

  useEffect(() => {
    const storedCart = JSON.parse(localStorage.getItem("cart")) || [];
    setCart(storedCart);
  }, []);

  const updateQuantity = (productId, newQuantity) => {
    if (newQuantity === 0) {
      handleShowModal(productId);
      return;
    }

    newQuantity = Math.max(newQuantity, 1);

    const updatedCart = cart.map((item) => {
      if (item._id === productId) {
        return { ...item, quantity: newQuantity };
      }
      return item;
    });

    setCart(updatedCart);
    localStorage.setItem("cart", JSON.stringify(updatedCart));
  };

  const removeFromCart = (productId) => {
    const updatedCart = cart.filter((item) => item._id !== productId);

    setCart(updatedCart);
    localStorage.setItem("cart", JSON.stringify(updatedCart));
    handleCloseModal();
  };

  const handleConfirmRemoval = () => {
    if (productToRemove !== null) {
      removeFromCart(productToRemove);
    }
  };

  const handleShowModal = (productId) => {
    setProductToRemove(productId);
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setProductToRemove(null);
  };

  const calculateSubtotal = () => {
    return cart.reduce((total, item) => total + item.price * item.quantity, 0);
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

  const handlePayment = () => {
    if(localStorage.getItem("user") == null) {
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
        }
      });
    } else {
      //TODO: avviare ordine, inserire nuovo ordine, aggiornare la quantità.
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
    }
  };

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
                  <th>Quantity</th>
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
                            updateQuantity(item._id, item.quantity - 1)
                          }
                        >
                          -
                        </button>
                        <span>{item.quantity}</span>
                        <button
                          className="btn btn-sm btn-primary ms-2"
                          onClick={() =>
                            updateQuantity(item._id, item.quantity + 1)
                          }
                        >
                          +
                        </button>
                      </div>
                    </td>
                    <td>${(item.price * item.quantity).toFixed(2)}</td>
                    <td>
                      <button
                        className="btn btn-danger"
                        onClick={() => handleShowModal(item._id)}
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
                      {/* Adjust colspan to 4 */}
                      Subtotal:
                    </td>
                    <td>${calculateSubtotal().toFixed(2)}</td>
                    <td></td>
                  </tr>
                  <tr>
                    <td colSpan="4" className="text-end">
                      {" "}
                      {/* Adjust colspan to 4 */}
                      VAT (22%):
                    </td>
                    <td>${calculateVat().toFixed(2)}</td>
                    <td></td>
                  </tr>
                  <tr>
                    <td colSpan="4" className="text-end">
                      {" "}
                      {/* Adjust colspan to 4 */}
                      Shipping Cost:
                    </td>
                    <td>${SHIPPING_COST.toFixed(2)}</td>
                    <td></td>
                  </tr>
                  <tr>
                    <td colSpan="4" className="text-end">
                      {" "}
                      {/* Adjust colspan to 4 */}
                      Total:
                    </td>
                    <td>${calculateTotal()}</td>
                    <td></td>
                  </tr>
                  <tr>
                    <td colSpan="4" className="text-end">
                      {" "}
                      {/* Adjust colspan to 4 */}
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
      <RemoveConfirm
        show={showModal}
        onConfirm={handleConfirmRemoval}
        onCancel={handleCloseModal}
      />
    </>
  );
};

export default CartPage;
