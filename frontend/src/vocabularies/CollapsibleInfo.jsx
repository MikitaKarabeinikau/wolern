import React, { useState, useRef, useEffect } from 'react';
import '../../styles/Collapsible.css';

function CollapsibleInfo({ title, children }) {
  const [isOpen, setIsOpen] = useState(false);
  const contentRef = useRef(null);

  useEffect(() => {
    // Function to adjust scroll position
    const adjustScroll = () => {
      if (contentRef.current) {
        const contentTop = contentRef.current.getBoundingClientRect().top;
        const windowTop = window.scrollY || document.documentElement.scrollTop;
        const offset = contentTop + windowTop - 20; // Adjust 20 to your needs

        window.scrollTo({
          top: offset,
          behavior: 'smooth', // Optional: for smooth scrolling
        });
      }
    };

    // Call adjustScroll when isOpen changes to false (collapsing)
    if (!isOpen) {
      adjustScroll();
    }
  }, [isOpen]);

  return (
    <div className="collapsible">
      <button className="collapsible-header" onClick={() => setIsOpen(!isOpen)}>
        {title}
      </button>
      <div
        className={`collapsible-content ${isOpen ? 'open' : ''}`}
        ref={contentRef}
      >
        {children}
      </div>
    </div>
  );
}

export default CollapsibleInfo;