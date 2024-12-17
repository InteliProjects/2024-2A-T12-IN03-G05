import React from 'react';
import './Dropdown.css';

const Dropdown = ({ options, placeholder, label, onChange, selectedValue }) => {
  return (
    <div className="dropdown-container">
      {label && <p className="dropdown-label">{label}</p>}
      <select className="custom-dropdown" onChange={onChange} value={selectedValue}>
        <option value="" disabled>
          {placeholder}
        </option>
        {options.map((option, index) => (
          <option key={index} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {selectedValue && <p className="selected-value">Selecionado: {selectedValue}</p>}
    </div>
  );
};

export default Dropdown;