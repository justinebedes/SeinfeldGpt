import React, { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState('');

  useEffect(() => {
    console.log('Fetching /api/seinfeldGPT2');
    fetch('/api/seinfeldGPT2')
      .then(response => {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let result = '';

        function read() {
          return reader.read().then(({ done, value }) => {
            if (done) {
              return;
            }
            result += decoder.decode(value, { stream: true });
            setData(result);
            return read();
          });
        }

        return read();
      })
      .catch(error => setData('Error: ' + error.message));
  }, []);

  return <div>{data ? data : 'Loading...'}</div>;
}

export default App;