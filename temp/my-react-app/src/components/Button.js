import React from 'react';

const handleClick = () => {
    fetch('/run-python-script', {
        method: 'POST'
    })
    .then(response => response.text())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
};

const Button = () => {
    return (
        <div className="button">
            <button onClick={handleClick}>Click Me</button>
        </div>
    );
};

export default Button;
