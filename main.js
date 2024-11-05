// static/main.js

const video = document.getElementById('video');
const result = document.getElementById('result');

// Access webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(error => {
        console.error('Error accessing webcam:', error);
    });

function captureImage() {
    // Create a canvas to capture the current frame from the video
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert the canvas to a blob and send to server
    canvas.toBlob(blob => {
        fetch('/process_image', {
            method: 'POST',
            body: blob,
        })
        .then(response => response.json())
        .then(data => {
            if (data.type === 'meme') {
                result.innerHTML = `<img src="${data.src}" alt="Meme">`;
            } else if (data.type === 'video') {
                window.open(data.src, '_blank');
            } else {
                result.textContent = 'No emotion detected';
            }
        })
        .catch(error => console.error('Error processing image:', error));
    }, 'image/jpeg');
}
