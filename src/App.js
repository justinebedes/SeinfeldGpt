import React, { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState('');

  useEffect(() => {
    console.log('Fetching from seinfeldGPT2');
    fetch('https://backend.ebedes.com/seinfeldGPT2')
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

  return (
    <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
      {data ? data : 'Loading...'}
    </pre>
  );
}

export default App;