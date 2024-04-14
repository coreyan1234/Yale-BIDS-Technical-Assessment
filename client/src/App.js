import React, { useEffect, useState } from 'react';
import axios from 'axios';
import "./App.css";

function App() {
  const [ids, setIds] = useState([]);
  const [details, setDetails] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/search')
      .then(response => {
        setIds(response.data);
        response.data.forEach(id => {
          axios.post('http://localhost:5000/details', { target_id: id, fields: ['ID', 'Title', 'Authors', 'Publication Date'] })
            .then(response => {
              setDetails(prevDetails => [...prevDetails, response.data]);
            });
        });
      });
  }, []);

  return (
    <div>
      <h1>Dataset Details</h1>
      <ul>
        {details.map(detail => (
          <li key={detail.ID}>
            <strong>ID:</strong> {detail.ID}<br />
            <strong>Title:</strong> {detail.Title}<br />
            <strong>Authors:</strong> {detail.Authors.join(', ')}<br />
            <strong>Publication Date:</strong> {detail['Publication Date']}<br /><br />
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
