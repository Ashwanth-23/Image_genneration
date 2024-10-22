from flask import Flask, render_template, request, send_file
import requests
import io
from PIL import Image

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": "Bearer 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"}

def query_image(prompt, height, width):
    payload = {
        "inputs": prompt,
        "parameters": {
            "height": height,
            "width": width
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        height = int(request.form['height'])
        width = int(request.form['width'])
        
        # Query the model
        image_bytes = query_image(prompt, height, width)

        # Save the image to a file
        image = Image.open(io.BytesIO(image_bytes))
        image.save("static/generated_image1.png")

        # Display the generated image
        image_url = "static/generated_image1.png"
    return render_template('index.html', image_url="static/generated_image1.png")

if __name__ == '__main__':
    app.run(debug=True)
