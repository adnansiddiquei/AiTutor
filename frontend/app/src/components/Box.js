import React from 'react';

const Box = ({ width, height }) => {
  const boxStyle = {
    width: `${width}`,
    height: `${height}px`,
    background: '#f0f0f0', // Example background color
    margin: '0 auto', // Centers the box horizontally
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)' // Centers the box vertically and horizontally
  };
  
  return (
    <div style={boxStyle}>
      {/* Content of the box goes here */}
    </div>
  );
};

export default Box;