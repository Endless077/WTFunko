import React from "react";
import "./RemoveConfirm.css";

const RemoveConfirm = ({ show, onConfirm, onCancel, productTitle }) => {
  if (!show) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h5>Confirm Removal</h5>
        <p>Are you sure you want to remove the selected item from the cart?</p>
        <div className="modal-buttons">
          <button className="btn btn-danger" onClick={onConfirm}>
            Yes
          </button>
          <button className="btn btn-secondary" onClick={onCancel}>
            No
          </button>
        </div>
      </div>
    </div>
  );
};

export default RemoveConfirm;
