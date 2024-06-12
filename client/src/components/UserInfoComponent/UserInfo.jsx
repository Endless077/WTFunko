import React, { useState, useEffect } from "react";
import "./UserInfo.css";
import { Navbar } from "../Navbar";
import { Link, useNavigate } from "react-router-dom";
import { confirmAlert } from "react-confirm-alert"; // Importa il pacchetto
import "react-confirm-alert/src/react-confirm-alert.css"; // Importa lo stile CSS

// Dati fasulli per esempio
const fakeUserData = {
  username: "JohnDoe",
  email: "johndoe@example.com",
  orderIds: [101, 102, 103, 104],
};

const fakeOrdersData = {
  101: {
    id: 101,
    date: "2024-01-15",
    total: 150.0,
    items: ["Item A", "Item B"],
  },
  102: {
    id: 102,
    date: "2024-02-20",
    total: 200.0,
    items: ["Item C", "Item D"],
  },
  103: {
    id: 103,
    date: "2024-03-10",
    total: 50.0,
    items: ["Item E", "Item F"],
  },
  104: {
    id: 104,
    date: "2024-04-05",
    total: 300.0,
    items: ["Item G", "Item H"],
  },
};

const UserInfo = () => {
  const [userData, setUserData] = useState(null);
  const [selectedOrder, setSelectedOrder] = useState({});
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState("");
  const navigate = useNavigate();

  const user = JSON.parse(localStorage.getItem("user"));

  useEffect(() => {
    // Simula il recupero dei dati dell'utente
    setUserData(fakeUserData);
  }, []);

  const handleOrderClick = (orderId) => {
    setSelectedOrder((prevSelectedOrder) => ({
      ...prevSelectedOrder,
      [orderId]: !prevSelectedOrder[orderId],
    }));
  };

  const handleLogout = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("cart");
    setIsLoggedIn(false);
    setUsername("");
    navigate("/");
  };

  const handleDeleteAccount = () => {
    //TODO : FARE LA CHIAMATA PER CANCELLARE L'UTENTE CON USERNAME username
    handleLogout();
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

  return (
    <>
      <Navbar />
      <div className="container my-5 py-5">
        <div className="row">
          <div className="col-12 mb-4 text-center">
            <h1 className="display-6 fw-bolder">User Information</h1>
          </div>
          {userData ? (
            <div className="col-12">
              <div className="user-info-card">
                <h2 className="user-info-title">Profile Details</h2>
                <p>
                  <strong>Username:</strong> {userData.username}
                </p>
                <p>
                  <strong>Email:</strong> {userData.email}
                </p>
                <h3 className="user-info-title">Order History</h3>
                <ul className="order-list">
                  {userData.orderIds.map((orderId) => (
                    <li key={orderId} className="order-item">
                      <button
                        className="order-link"
                        onClick={() => handleOrderClick(orderId)}
                      >
                        Order ID: {orderId}
                      </button>
                      <span className="order-total">
                        ${fakeOrdersData[orderId].total.toFixed(2)}
                      </span>
                      {selectedOrder[orderId] && (
                        <div className="order-details mt-2">
                          <p>
                            <strong>Date:</strong>{" "}
                            {fakeOrdersData[orderId].date}
                          </p>
                          <h4>Items:</h4>
                          <ul className="order-items-list">
                            {fakeOrdersData[orderId].items.map(
                              (item, index) => (
                                <li key={index} className="order-item">
                                  {item}
                                </li>
                              )
                            )}
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
