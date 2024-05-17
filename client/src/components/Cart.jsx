import { useState } from "react";
import { Navbar } from "./Navbar";
import "./Cart.css";

const CartPage = () => {
  // Costante per l'IVA al 22%
  const VAT_RATE = 0.22;

  // Costo fisso per le spese di spedizione
  const SHIPPING_COST = 5.0;

  //Costo del sottototale
  let subtotal = 0;
  // Esempio di stato del carrello con alcuni prodotti
  const [cart, setCart] = useState([
    {
      id: 1,
      name: "Funko Pop Figure",
      price: 10.99,
      quantity: 2,
      image: "/assets/zoro.png",
    },
    {
      id: 2,
      name: "Funko Mystery Box",
      price: 24.99,
      quantity: 1,
      image: "/assets/zoro.png",
    },
  ]);

  const removeFromCart = (productId) => {
    setCart(cart.filter((item) => item.id !== productId));
  };

  const updateQuantity = (productId, newQuantity) => {
    newQuantity = Math.max(newQuantity, 1);
    setCart(
      cart.map((item) =>
        item.id === productId ? { ...item, quantity: newQuantity } : item
      )
    );
  };

  const calculateSubtotal = () => {
    subtotal = cart.reduce(
      (total, item) => total + item.price * item.quantity,
      0
    );
    return subtotal;
  };

  const calculateVat = () => {
    return subtotal * VAT_RATE;
  };

  const calculateTotal = () => {
    const subtotal = cart.reduce(
      (total, item) => total + item.price * item.quantity,
      0
    );
    const vat = subtotal * VAT_RATE;
    const total = subtotal + vat + SHIPPING_COST;
    return total.toFixed(2);
  };

  const handlePayment = () => {
    alert("Payment successful!");
  };

  return (
    <>
      <Navbar />
      <div className="container mt-5">
        <h2>Shopping Cart</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Product</th>
              <th>Price</th>
              <th>Quantity</th>
              <th>Total</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {cart.map((item) => (
              <tr key={item.id}>
                <td>
                  <div className="d-flex align-items-center">
                    <img
                      src={item.image}
                      alt={item.name}
                      style={{ marginRight: "10px", width: "50px" }}
                    />
                    <span>{item.name}</span>
                  </div>
                </td>
                <td>${item.price.toFixed(2)}</td>
                <td>
                  <div className="d-flex align-items-center">
                    <button
                      className="btn btn-sm btn-primary me-2"
                      onClick={() => updateQuantity(item.id, item.quantity - 1)}
                    >
                      -
                    </button>
                    <span>{item.quantity}</span>
                    <button
                      className="btn btn-sm btn-primary ms-2"
                      onClick={() => updateQuantity(item.id, item.quantity + 1)}
                    >
                      +
                    </button>
                  </div>
                </td>
                <td>${(item.price * item.quantity).toFixed(2)}</td>
                <td>
                  <button
                    className="btn btn-danger"
                    onClick={() => removeFromCart(item.id)}
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
                <td colSpan="3" className="text-end">
                  Subtotal:
                </td>
                <td>${calculateSubtotal().toFixed(2)}</td>
                <td></td>
              </tr>
              <tr>
                <td colSpan="3" className="text-end">
                  VAT (22%):
                </td>
                <td>${calculateVat().toFixed(2)}</td>
                <td></td>
              </tr>
              <tr>
                <td colSpan="3" className="text-end">
                  Shipping Cost:
                </td>
                <td>${SHIPPING_COST.toFixed(2)}</td>
                <td></td>
              </tr>
              <tr>
                <td colSpan="3" className="text-end">
                  Total:
                </td>
                <td>${calculateTotal()}</td>
                <td></td>
              </tr>
              <tr>
                <td colSpan="3" className="text-end">
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
      </div>
    </>
  );
};

export default CartPage;
