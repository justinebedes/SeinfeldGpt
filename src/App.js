import React, { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState('');

  useEffect(() => {
    fetch('http://backend.ebedes.com/seinfeldGPT')
      .then(response => response.text())
      .then(text => setData(text))
      .catch(error => setData('Error: ' + error.message));
  }, []);

  return <div>{data ? data : 'Loading...'}</div>;
}

export default App;