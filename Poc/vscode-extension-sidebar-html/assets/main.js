// main.js

function submitForm() {
    const cpu = document.getElementById('cpu').value;
    const os = document.getElementById('os').value;
    const memory = document.getElementById('memory').value;
    const selectedCode = document.getElementById('selectedCode').value;
  
    if (cpu.trim() !== '' && os.trim() !== '' && memory.trim() !== '' && selectedCode.trim() !== '') {
      // Send a message to the extension
      vscode.postMessage({
        command: 'submitForm',
        cpu: cpu,
        os: os,
        memory: memory,
        selectedCode: selectedCode,
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
  