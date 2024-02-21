// main.js

function submitForm() {
  const cpu = document.getElementById('cpu').value;
  const os = document.getElementById('os').value;
  const memory = document.getElementById('memory').value;
  const selectedCode = document.getElementById('selectedCode').value;

  if (cpu.trim() !== '' && os.trim() !== '' && memory.trim() !== '' && selectedCode.trim() !== '') {
      // Construct the API URL with the form data
      const apiUrl = 'http://localhost:3000/posts';
      // const formData = {
      //     cpu: cpu,
      //     os: os,
      //     memory: memory,
      //     selectedCode: selectedCode,
      // };

      // Make the API call using fetch
      fetch(apiUrl, {
          method: 'GET', // or 'GET' depending on your API
          headers: {
              'Content-Type': 'application/json',
          },
          //body: JSON.stringify(formData),
      })
      .then(response => {
          if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
      })
      .then(data => {
          // Handle the API response as needed
          console.log('API response:', data);
          vscode.postMessage({
            command: 'showInformationMessage',
            text: `API response: ${JSON.stringify(data)}`,
          });
        })
      .catch(error => {
          console.error('Error:', error);
          // Handle errors, and maybe inform the user
          vscode.postMessage({
              command: 'showError',
              text: 'Error occurred while making the API call.',
          });
      });

  } else {
      // Send an error message to the extension
      vscode.postMessage({
          command: 'showError',
          text: 'Please fill in all fields.',
      });
  }
}

document.addEventListener('DOMContentLoaded', function () {
  const submitButton = document.getElementById('submitBtn');

  if (submitButton) {
      submitButton.addEventListener('click', submitForm);
  }
});
