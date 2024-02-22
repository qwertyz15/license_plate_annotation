import requests
import json
import base64
from PIL import Image
from io import BytesIO

def receive_license_plate_image():
    url = 'http://127.0.0.1:5000/get_license_plate_image'  # Update the URL accordingly
    response = requests.get(url)

    if response.status_code == 200:
        print("Response text:", response.text)
        data = response.json()
        image_path = data['image_path']
        image_b64 = data['image_b64']
        print(image_path)
        image_bytes = base64.b64decode(image_b64)
        image = Image.open(BytesIO(image_bytes))
        image.show()
        return image_path
    else:
        print("Error:", response.text)
        return None

def send_annotated_number(image_path, license_plate_number):
    url = 'http://127.0.0.1:5000/send_annotated_number'  # Update the URL accordingly
    payload = {
        'image_path': image_path,
        'license_plate_number': license_plate_number
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        print("License plate number sent successfully.")
    else:
        print("Error:", response.json()['error'])

if __name__ == "__main__":
    received_image_path = receive_license_plate_image()
    if received_image_path:
        license_plate_number = input("Enter the annotated license plate number: ")
        send_annotated_number(received_image_path, license_plate_number)
