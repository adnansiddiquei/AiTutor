import React from 'react';
import Plot from 'react-plotly.js';

const ScatterPlot = ({ data }) => {
  // Map your categories to colors
  const categoryToColor = {
    // 'Ethical and Professional Standards': '#FF0000',
    // 'Quantitative Methods': '#0000FF',
    // 'Economics': '#008000',
    // 'Financial Reporting and Analysis': '#800080',
    // 'Alternative Investments': '#FFA500',
    // 'Corporate Issuers': '#FFFF00',
    // 'Derivatives': '#00FFFF',
    // 'Fixed Income': '#FF00FF',
    // 'Portfolio Management and Wealth Planning': '#008080',
  };

  
  // Group data by category
  const groupedData = data.reduce((acc, point) => {
    if (!acc[point.category]) {
      acc[point.category] = {
        x: [],
        y: [],
        marker: {
          size: [],
          color: [],
        },
        type: 'scatter',
        mode: 'markers',
        name: point.category
      };
    }
    
    acc[point.category].x.push(point.x);
    acc[point.category].y.push(point.y);
    acc[point.category].marker.size.push(Math.sqrt(point.zScore) * 30); // Assuming 'size' is a property in your data
    // acc[point.category].marker.color.push(categoryToColor[point.category]);
    
    return acc;
  }, {});
  
  // Convert the grouped data into an array for Plotly
  const plotData = Object.keys(groupedData).map((category) => {
    return {
      ...groupedData[category],
      // Spreading the marker properties here
      marker: {
        ...groupedData[category].marker,
        color: categoryToColor[category], // Single color for each category
        // size and opacity arrays are already included from the reduce function above
      }
    };
  });
  
  return (
    <Plot
      data={plotData}
      layout={{
        width: 1100,
        height: 800,
        title: 'A visualisation of question similarity and difficulty',
      }}
    />
  );
};

export default ScatterPlot;