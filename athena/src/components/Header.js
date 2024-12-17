// src/components/Header.js
import React from 'react';
import './Header.css';
import logo from '../assets/images/logo_data027.svg';

const Header = () => {
    return (
      <header className="header">
        <img src={logo} alt="Logo" className="logo" />
      </header>
    );
  }

export default Header;
