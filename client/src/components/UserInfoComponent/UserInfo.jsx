// UserInfo.js
import React, { useState, useEffect } from "react";
import { Navbar } from "../Navbar";
import { useParams, useNavigate } from "react-router-dom";

// Utils
import "./UserInfo.css";
import Swal from "sweetalert2";
import "react-confirm-alert/src/react-confirm-alert.css";
import { confirmAlert } from "react-confirm-alert";
import { config, fetchData } from "../../utils";

const UserInfo = () => {
  const { username } = useParams();
  const [user, setUser] = useState(null);
  const [orders, setOrders] = useState([]);
  const [selectedOrder, setSelectedOrder] = useState({});

  const navigate = useNavigate();

  /* ********************************************************************************************* */

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const endpointUrl = config.endpoints.getUser.url;
        const method = config.endpoints.getUser.method;
        const queryParams = {
          username: username,
        };

        const getUserResponse = await fetchData(
          endpointUrl,
          method,
          queryParams,
          undefined,
          undefined
        );

        const getUserResponseData = await getUserResponse.json();

        if (!getUserResponse.ok) {
          throw new Error(
            getUserResponseData.detail ||
              "User information fetch failed. Please try again later."
          );
        }

        const userStruct = {
          username: getUserResponseData.username,
          email: getUserResponseData.email,
        };

        localStorage.setItem("user", JSON.stringify(userStruct));
        setUser(userStruct);
        
      } catch (error) {
        console.error("Error fetching user data:", error);
        Swal.fire({
          icon: "info",
          title: "Error fetching user data",
          text: error.message,
        });
      }
    };

    try {
      const cachedUser = localStorage.getItem("user");
      !cachedUser ? fetchUserData() : setUser(JSON.parse(cachedUser));

    } catch (error) {
      console.error("Error during user info load:", error);
    }
  }, [username]);

  useEffect(() => {
    const fetchUserOrders = async () => {
      try {
        const endpointUrl = config.endpoints.getUserOrders.url;
        const method = config.endpoints.getUserOrders.method;
        const queryParams = {
          username: username,
        };

        const getUserOrdersResponse = await fetchData(
          endpointUrl,
          method,
          queryParams,
          undefined,
          undefined
        );

        const getUserResponseData = await getUserOrdersResponse.json();

        if (!getUserOrdersResponse.ok) {
          throw new Error(
            getUserResponseData.detail ||
              "User orders fetch failed. Please try again later."
          );
        }

        localStorage.setItem(`${username}Orders`, JSON.stringify(getUserResponseData));
        setOrders(JSON.parse(getUserResponseData));

      } catch (error) {
        console.error("Error fetching user orders data:", error);
        Swal.fire({
          icon: "info",
          title: "Error fetching user orders data",
          text: error.message,
        });
      }
    };

    try {
      const cachedOrders = localStorage.getItem(`${username}Orders`);
      !cachedOrders ? fetchUserOrders() : setOrders(JSON.parse(cachedOrders));

    } catch (error) {
      console.error("Error during user info load:", error);
    }
  }, [user]);
  
  const handleOrderClick = (orderId) => {
    setSelectedOrder((prevSelectedOrder) => ({
      ...prevSelectedOrder,
      [orderId]: !prevSelectedOrder[orderId],
    }));
  };

  const showDeleteConfirmation = () => {
    confirmAlert({
      title: "Confirm to delete account",
      message: "Are you sure you want to delete your account?",
      buttons: [
        {
          label: "Yes",
          onClick: handleDeleteAccount,
        },
        {
          label: "No",
          onClick: () => {},
        },
      ],
    });
  };

  const handleDeleteAccount = () => {
    handleLogout();
  };

  const handleLogout = () => {
    localStorage.clear()
    navigate("/");
  };

  /* ********************************************************************************************* */

  return (
    <>
      <Navbar />
      <div className="container my-4">
        <div className="row">
          <div className="col-12 mb-4 text-center">
            <h1 className="display-6 fw-bolder">User Information</h1>
          </div>
          {user ? (
            <div className="col-12">
              <div className="user-info-card">
                <h2 className="user-info-title">Profile Details</h2>
                <p>
                  <strong>Username:</strong> {user.username}
                </p>
                <p>
                  <strong>Email:</strong> {user.email}
                </p>
                <h3 className="user-info-title">Order History</h3>
                <ul className="order-list">
                  {orders.map((order) => (
                    <li key={order.id} className="order-item">
                      <button
                        className="order-link"
                        onClick={() => handleOrderClick(order.id)}
                      >
                        Order ID: {order.id}
                      </button>
                      <span className="order-total">
                        ${order.total.toFixed(2)}
                      </span>
                      {selectedOrder[order.id] && (
                        <div className="order-details mt-2">
                          <p>
                            <strong>Date:</strong> {order.date}
                          </p>
                          <h4>Items:</h4>
                          <ul className="order-items-list">
                            {order.products.map((product) => (
                              <li key={product.id} className="order-item">
                                <img
                                  src={product.img}
                                  alt={product.title}
                                  className="order-item-image"
                                />
                                <div>
                                  <p>{product.title}</p>
                                  <p>Type: {product.product_type}</p>
                                  <p>Price: ${product.price}</p>
                                  <p>Amount: {product.amount}</p>
                                </div>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
              <div className="delete-account-button">
                <button
                  className="btn btn-danger"
                  onClick={showDeleteConfirmation}
                >
                  Delete Account
                </button>
              </div>
            </div>
          ) : (
            <div className="col-12 text-center">
              <p>Loading user data...</p>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default UserInfo;
