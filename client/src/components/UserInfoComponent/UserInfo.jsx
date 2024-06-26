// UserInfo.js
import React, { useState, useEffect } from "react";
import { Navbar } from "../Navbar";
import { Link, useParams, useNavigate } from "react-router-dom";

// Utils
import "./UserInfo.css";
import Swal from "sweetalert2";
import { format } from "date-fns";
import { Status } from "../enumerations";
import "react-confirm-alert/src/react-confirm-alert.css";
import { config, fetchData, retrieveToken } from "../../utils";

const UserInfo = () => {
  const [user, setUser] = useState(null);
  const [orders, setOrders] = useState([]);
  const [selectedOrder, setSelectedOrder] = useState({});

  const { username } = useParams();

  const navigate = useNavigate();

  /* ********************************************************************************************* */

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const endpointUrl = config.endpoints.getUser.url;
        const headers = {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        };
        const method = config.endpoints.getUser.method;
        const queryParams = {
          username: username,
        };

        const getUserResponse = await fetchData(
          endpointUrl,
          headers,
          method,
          queryParams,
          undefined,
          undefined
        );

        const getUserResponseData = await getUserResponse.json();

        if (!getUserResponse.ok) {
          if (getUserResponse.status == 401) {
            console.error(
              "Error fetching user data:",
              getUserResponseData.detail
            );
            Swal.fire({
              icon: "error",
              title: "Unauthorized User",
              text: "If you think it is an error, please try again.",
            });
            newToken = await retrieveToken();
            localStorage.setItem("token", newToken);
          }
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
          icon: "error",
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
        const headers = {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        };
        const method = config.endpoints.getUserOrders.method;
        const queryParams = {
          username: username,
        };

        const getUserOrdersResponse = await fetchData(
          endpointUrl,
          headers,
          method,
          queryParams,
          undefined,
          undefined
        );

        const getOrdersResponseData = await getUserOrdersResponse.json();

        if (!getUserOrdersResponse.ok) {
          if (getUserOrdersResponse.status == 401) {
            console.error(
              "Error fetching user data:",
              getOrdersResponseData.detail
            );
            const newToken = await retrieveToken();
            localStorage.setItem("token", newToken);
          }
          throw new Error(
            getOrdersResponseData.detail ||
              "User orders fetch failed. Please try again later."
          );
        }

        localStorage.setItem(
          `${username}Orders`,
          JSON.stringify(getOrdersResponseData)
        );
        setOrders(getOrdersResponseData);
      } catch (error) {
        console.error("Error fetching user orders data:", error);
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
    Swal.fire({
      title: "Confirm to delete account",
      text: "Are you sure you want to delete your account?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#dc3545",
      cancelButtonColor: "#6c757d",
      confirmButtonText: "Yes",
      cancelButtonText: "No",
    }).then((result) => {
      if (result.isConfirmed) {
        handleDeleteAccount();
      }
    });
  };

  const getOrderButtonColor = (status) => {
    switch (status) {
      case Status.FULLFILLED:
        return "#28a745";
      case Status.ON_HOLD:
        return "#ffc107";
      case Status.SCHEDULED:
        return "#dc3545";
      default:
        return "#000000";
    }
  };

  const handleDeleteAccount = () => {
    const fetchDeleteUser = async () => {
      try {
        const endpointUrl = config.endpoints.deleteAccount.url;
        const headers = {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        };
        const method = config.endpoints.deleteAccount.method;
        const pathParams = {
          username: username,
        };
        const deleteUserResponse = await fetchData(
          endpointUrl,
          headers,
          method,
          undefined,
          pathParams,
          undefined
        );

        const deleteUserResponseData = await deleteUserResponse.json();

        if (!deleteUserResponse.ok) {
          throw new Error(
            deleteUserResponseData.detail ||
              "User account deletion fetch failed. Please try again later."
          );
        }

        Swal.fire({
          icon: "success",
          title: "User Account Deleted",
          text: `Thank you ${username} for being our customer \u2764\uFE0F.`,
          timer: 3000,
          timerProgressBar: true,
          showConfirmButton: false,
          allowOutsideClick: false,
          willClose: () => {
            localStorage.clear();
            navigate("/");
          },
        });
      } catch (error) {
        console.error("Error fetching deletion user account:", error);
        Swal.fire({
          icon: "error",
          title: "Error during account deletion",
          text: error.message,
        });
      }
    };

    try {
      fetchDeleteUser();
    } catch (error) {
      console.error("Error durin user account deletion:", error);
    }
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
              </div>
              <div className="order-history-section">
                <h3 className="user-info-title">Order History</h3>
                {orders.length === 0 ? (
                  <p className="text-center">No orders found.</p>
                ) : (
                  <ul className="order-list">
                    {orders.map((order) => (
                      <li key={order._id} className="order-item">
                        <button
                          className="order-link"
                          style={{
                            backgroundColor: getOrderButtonColor(order.status),
                          }}
                          onClick={() => handleOrderClick(order._id)}
                        >
                          Order ID: {order._id}
                        </button>
                        <div className="order-item-details">
                          <div>
                            Date: {format(new Date(order.date), "dd/MM/yyyy")}
                          </div>
                          <div>Status: {order.status}</div>
                          <div>Total: ${order.total.toFixed(2)}</div>
                        </div>
                        {selectedOrder[order._id] && (
                          <div className="order-details mt-2">
                            <h3>Order Items:</h3>
                            <ul className="order-items-list">
                              {order.products.map((product) => (
                                <li key={product._id} className="order-item">
                                  <Link to={`/productInfo/${product._id}`}>
                                    <img
                                      src={product.img}
                                      className="card-img-top product-image"
                                      alt={product.title}
                                      height="100"
                                      width="100"
                                      onError={(e) =>
                                        (e.target.src =
                                          "/assets/Funko_Placeholder.png")
                                      }
                                    />
                                  </Link>
                                  <div>
                                    <Link to={`/productInfo/${product._id}`}>
                                      <h5 className="card-title mb-0">
                                        {product.title}
                                      </h5>
                                    </Link>
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
                )}
              </div>
              <div className="delete-account-button text-center mt-4">
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
