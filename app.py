# app.py

from flask import Flask, render_template, request, jsonify, send_file
import cv2
import numpy as np
import random
from fer import FER

app = Flask(__name__)
emotion_detector = FER()

# Map emotions to meme images and YouTube links
emotion_meme_map = {
    "happy": ["happy.jpg", "https://www.youtube.com/watch?v=happy_video"],
    "sad": ["static/sad_meme1.jpg", "https://www.youtube.com/watch?v=sad_video"],
    # Add more mappings as needed
}

def detect_emotion(image):
    """Detects the dominant emotion from the given image."""
    emotions = emotion_detector.detect_emotions(image)
    if emotions:
        # Extract most probable emotion
        emotion = max(emotions[0]["emotions"], key=emotions[0]["emotions"].get)
        return emotion
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    # Get the image from the POST request
    nparr = np.frombuffer(request.data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Detect emotion in the image
    detected_emotion = detect_emotion(image)
    
    if detected_emotion and detected_emotion in emotion_meme_map:
        meme_or_video = random.choice(emotion_meme_map[detected_emotion])
        
        # Check if it's an image or a video link
        if meme_or_video.endswith('.jpg'):
            return jsonify({'type': 'meme', 'src': meme_or_video})
        else:
            return jsonify({'type': 'video', 'src': meme_or_video})
    
    return jsonify({'error': 'No emotion detected'})

if __name__ == '__main__':
    app.run(debug=True)
