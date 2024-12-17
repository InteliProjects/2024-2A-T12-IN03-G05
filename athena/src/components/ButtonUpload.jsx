import React from 'react';
import './ButtonUpload.css';
import uploadIcon from '../assets/images/upload_icon.svg';

const ButtonUpload = ({ label, onFileChange, fileName, inputId, uploaded }) => {
  return (
    <div className="button-container-upload">
      <input
        type="file"
        accept=".csv"
        id={inputId}
        style={{ display: 'none' }}
        onChange={onFileChange}
      />
      <label htmlFor={inputId} className={`custom-button ${uploaded ? 'uploaded' : ''}`}>
        <span className="button-text">{label}</span>
        <img src={uploadIcon} alt="Upload Icon" className="button-icon" />
      </label>
      {fileName && <p className="file-name">{fileName}</p>}
    </div>
  );
};

export default ButtonUpload;
