import requests
import io
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

# Define your prompt, height, and width
prompt = "Astronaut riding a horse"
image_height = 1920  # Specify the desired height
image_width = 1080   # Specify the desired width

# Query the API with the input prompt and dimensions
image_bytes = query({
    "inputs": prompt,
    "parameters": {
        "height": image_height,
        "width": image_width
    }
})

# Open the generated image using PIL
image = Image.open(io.BytesIO(image_bytes))

# Display the image
image.show()

# Save the image to a file
image.save("generated_image.png")
