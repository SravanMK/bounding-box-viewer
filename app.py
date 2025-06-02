from flask import Flask, request, render_template
import cv2
import numpy as np
import requests
from io import BytesIO
import os  # ✅ Import os to create static folder

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    image_path = None

    if request.method == 'POST':
        raw_input = request.form['input_data']
        try:
            parts = raw_input.strip().split('\t')
            url, top, bottom, right, left = parts[0], int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4])

            # Download and decode image
            resp = requests.get(url, stream=True).raw
            img_array = np.asarray(bytearray(resp.read()), dtype=np.uint8)
            image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            # Draw rectangle
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

            # Encode image to bytes
            _, img_encoded = cv2.imencode('.jpg', image)
            img_bytes = BytesIO(img_encoded.tobytes())

            # ✅ Ensure static folder exists
            os.makedirs("static", exist_ok=True)

            # Save the image
            with open("static/output.jpg", "wb") as f:
                f.write(img_bytes.getbuffer())

            image_path = "static/output.jpg"

        except Exception as e:
            return f"Error: {e}"

    return render_template('index.html', image_path=image_path)

if __name__ == '__main__':
    app.run(debug=True)
