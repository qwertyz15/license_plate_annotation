from flask import Flask, send_file, request, jsonify
import os
import base64
import random
import sqlite3

app = Flask(__name__)

# Directory where license plate images are stored
IMAGE_DIR = '/home/dev/Documents/datasets/duplicates_ssim'

# List to keep track of served images
served_images = []


# Function to insert data into the SQLite database
def insert_into_database(image_path, license_plate_number):
    conn = sqlite3.connect('license_plate_database.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO license_plate_info (image_path, license_plate_number) VALUES (?, ?)", (image_path, license_plate_number))
    conn.commit()
    conn.close()

# Function to get a random image from the directory that hasn't been served yet
def get_random_image():
    conn = sqlite3.connect('license_plate_database.db')
    cur = conn.cursor()
    
    # Retrieve all image paths from the database
    cur.execute("SELECT image_path FROM license_plate_info")
    all_images = cur.fetchall()
    all_images = [img[0] for img in all_images]
    
    # Filter out served images
    available_images = list(set(os.listdir(IMAGE_DIR)) - set(all_images))
    
    if not available_images:
        # If all images have been served, reset the list
        served_images.clear()
        available_images = os.listdir(IMAGE_DIR)
    
    random_image = random.choice(available_images)
    served_images.append(random_image)
    conn.close()
    return os.path.join(IMAGE_DIR, random_image)

# Route to serve a random license plate image
@app.route('/get_license_plate_image', methods=['GET'])
def serve_license_plate_image():
    image_path = get_random_image()
    with open(image_path, "rb") as img_file:
        img_b64 = base64.b64encode(img_file.read()).decode('utf-8')

    return jsonify({'image_path': image_path, 'image_b64': img_b64})

# Route to receive annotated number from the client
@app.route('/send_annotated_number', methods=['POST'])
def receive_annotated_number():
    data = request.json
    if 'image_path' not in data or 'license_plate_number' not in data:
        return jsonify({'error': 'Image path or license plate number not found in request'}), 400
    
    image_path = data['image_path']
    license_plate_number = data['license_plate_number']
    
    # Insert data into the SQLite database
    insert_into_database(image_path, license_plate_number)
    
    print("Received license plate number:", license_plate_number)
    print("Associated image path:", image_path)
    
    return jsonify({'message': 'License plate number received successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
