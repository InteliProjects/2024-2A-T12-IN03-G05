import React from 'react';
import './ButtonConfirm.css';

const ButtonConfirm = ({ label, onClick, isLoading }) => {
  return (
    <div className="button-container">
      <button className="confirm-button" onClick={onClick} disabled={isLoading}>
        {isLoading ? (
          <span className="loading-spinner"></span>
        ) : (
          <span className="button-text-confirm">{label}</span>
        )}
      </button>
    </div>
  );
};

export default ButtonConfirm;