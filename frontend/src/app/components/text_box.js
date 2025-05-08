"use client";

import React, { useEffect, useState } from 'react';

function ArticleBox() {
  const [text, setText] = useState('');
  const [data, setData] = useState('');
  const [article, setArticle] = useState('');

  const updateText = (event) => {
    setText(event.target.value)
  }

  const submitText = (event) => {
    event.preventDefault()
    sendData(text)
  }

  const sendData = (data) => {
    fetch('http://dss-political-bias-production.up.railway.app/api/article', {
      method: 'POST',
      body: JSON.stringify(data)
    })
      .then(response => response.json())
      .then(data => {
        setArticle(data.text);
        console.log("Response Data:", data);
      })
      .catch(err => console.error("Error fetching message:", err));
  }

  return (
    <form onSubmit={submitText}>
      <input 
        type="text" 
        id="user-article" 
        value={text} 
        onChange={updateText}
        placeholder='Enter URL here...'
      />
      <button type="submit">Submit</button>
      <div className='text-output'><p>{article}</p></div>
    </form>
  );
}

export default ArticleBox
