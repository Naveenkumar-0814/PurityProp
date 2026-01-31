import React, { useEffect, useRef } from 'react';
import logoImage from '../assets/logo.png';
import '../styles/animated-logo.css';

const AnimatedLogo = ({ size = 48 }) => {
    const spokesRef = useRef(null);

    const restartAnimation = () => {
        if (spokesRef.current) {
            spokesRef.current.style.animation = 'none';
            spokesRef.current.offsetHeight; /* trigger reflow */
            spokesRef.current.style.animation = 'rotate-in 1s ease-out forwards, spin 10s linear infinite 1s';
        }
    };

    return (
        <div
            className="animated-logo-container"
            style={{ width: size, height: size }}
            onClick={restartAnimation}
            title="Click to replay animation"
        >
            <div className="logo-layer inner-hub" style={{ backgroundImage: `url(${logoImage})` }}></div>
            <div
                className="logo-layer middle-spokes"
                ref={spokesRef}
                style={{ backgroundImage: `url(${logoImage})` }}
            ></div>
            <div className="logo-layer outer-ring" style={{ backgroundImage: `url(${logoImage})` }}></div>
        </div>
    );
};

export default AnimatedLogo;
