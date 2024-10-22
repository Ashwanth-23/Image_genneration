from flask import Flask, render_template, request
import requests
import io
from PIL import Image

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": "Bearer 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"}

def query_image(prompt, width, height):
    payload = {"inputs": prompt, "parameters": {"width": width, "height": height}}
    response = requests.post(API_URL, headers=headers, json=payload)

    # Check if the response is a valid image
    if response.status_code == 200:
        return response.content
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    image_url = None
    if request.method == 'POST':
        prompt = request.form['prompt']
        aspect_ratio = request.form['aspect_ratio']

        try:
            width_ratio, height_ratio = map(int, aspect_ratio.split(':'))
        except ValueError:
            return "Invalid aspect ratio format. Please use 'Width:Height'."

        base_width = 800  # Base width can be set according to your preference
        
        # Calculate height based on the aspect ratio
        height = (base_width * height_ratio) // width_ratio

        # Adjust width and height to be divisible by 8
        width = (base_width // 8) * 8
        height = (height // 8) * 8

        # Query the model
        image_bytes = query_image(prompt, width, height)

        if image_bytes:
            try:
                # Save the image to a file
                image = Image.open(io.BytesIO(image_bytes))
                image.save("static/generated_image.png")
                image_url = "static/generated_image.png"
            except Exception as e:
                print(f"Error opening or saving the image: {e}")

    return render_template('index1.html', image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)
