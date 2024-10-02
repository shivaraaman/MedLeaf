function uploadImage() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('image', file);

    fetch('/process-image', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Predicted Info:', data.info);

        // Display the predicted info on the HTML page
        const infoElement = document.getElementById('info');
        infoElement.innerHTML = ''; // Clear previous content
        data.info.forEach(item => {
            const p = document.createElement('p');
            p.textContent = item;
            infoElement.appendChild(p);
        });
    })
    .catch(error => console.error('Error:', error));
}
