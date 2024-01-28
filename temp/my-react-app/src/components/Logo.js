import React from 'react';
import './Logo.css'; // Import Logo.css
import logoImage from '../assets/logo.png'; // Assuming your logo file is named logo.png and located in the assets folder

const Logo = () => {
    return (
        <div className="logo">
            <img src={logoImage} alt="Logo" />
        </div>
    );
};

export default Logo;
