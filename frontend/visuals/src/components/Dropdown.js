import React, { useState } from 'react';

const Dropdown = ({lessonId, setLessonId}) => {
  const handleChange = (event) => {
    setLessonId(event.target.value);
  };
  
  return (
    <select value={lessonId} onChange={handleChange}>
      <option value="0">0</option>
      <option value="1">1</option>
    </select>
  );
};

export default Dropdown;