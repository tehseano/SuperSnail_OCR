import os
import sys
import subprocess
import pytesseract
from PIL import Image
import cv2
import numpy as np
import csv
import re

def check_tesseract():
    try:
        subprocess.run(["tesseract", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("Tesseract is not installed. Please install Tesseract OCR.")
        print("Visit https://github.com/UB-Mannheim/tesseract/wiki for Windows installation.")
        print("For macOS, use: brew install tesseract")
        print("For Linux, use: sudo apt-get install tesseract-ocr")
        sys.exit(1)
        
# Adjustable settings for each region
SETTINGS = {
    'Name': {
        'THRESH_BLOCK_SIZE': 13,
        'THRESH_C': 5,
        'INVERT': False,
        'SCALE': 1,
        'PSM': 13
    },
    'Power': {
        'THRESH_BLOCK_SIZE': 15,
        'THRESH_C': 5,
        'INVERT': False,
        'SCALE': 1,
        'PSM': 13
    },
    'Weekly_Club_Exp': {
        'THRESH_BLOCK_SIZE': 11,
        'THRESH_C': 5,
        'INVERT': False,
        'SCALE': 2,
        'PSM': 7
    },
    'Total_Club_Exp': {
        'THRESH_BLOCK_SIZE': 13,
        'THRESH_C': 5,
        'INVERT': False,
        'SCALE': 1,
        'PSM': 6
    },
    'DNA_Strength': {
        'THRESH_BLOCK_SIZE': 19,
        'THRESH_C': 2,
        'INVERT': False,
        'SCALE': 2,
        'PSM': 6
    },
    'Leadership': {
        'THRESH_BLOCK_SIZE': 19,
        'THRESH_C': 2,
        'INVERT': True,
        'SCALE': 2,
        'PSM': 7
    }
}

def preprocess_region(roi, settings):
    # Convert to grayscale
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, settings['THRESH_BLOCK_SIZE'], settings['THRESH_C'])
    
    # Invert the image if needed
    if settings['INVERT']:
        thresh = cv2.bitwise_not(thresh)
    
    # Scale the image
    thresh = cv2.resize(thresh, None, fx=settings['SCALE'], fy=settings['SCALE'], interpolation=cv2.INTER_CUBIC)
    
    return thresh

def extract_text_from_region(image, region, field):
    x, y, w, h = region
    roi = image[y:y+h, x:x+w]
    
    settings = SETTINGS[field]
    roi = preprocess_region(roi, settings)
    
    # Use Pillow for OCR
    pil_img = Image.fromarray(roi)
    
    # Define character whitelists for each field
    whitelists = {
        'Name': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789. ',
        'Power': '0123456789.M',
        'Weekly_Club_Exp': '0123456789',
        'Total_Club_Exp': '0123456789',
        'DNA_Strength': '0123456789K',
        'Leadership': '0123456789'
    }
    
    config = f'--psm {settings["PSM"]} -c tessedit_char_whitelist={whitelists[field]}'
    
    text = pytesseract.image_to_string(pil_img, config=config).strip()
    return text

def process_image(image_path):
    image = cv2.imread(image_path)
    
    # Define precise regions for each field (adjust these based on your image layout)
    regions = {
        'Name': (250, 660, 800, 125),  # (x, y, width, height)
        'Power': (585, 800, 250, 80),
        'Weekly_Club_Exp': (600, 1080, 75, 50),
        'Total_Club_Exp': (585, 1150, 90, 50),
        'DNA_Strength': (945, 1580, 130, 55),
        'Leadership': (960, 1725, 115, 65),
    }
    
    # Create a copy of the image to draw boxes on
    image_with_boxes = image.copy()
    
    data = {}
    for field, region in regions.items():
        x, y, w, h = region
        # Draw red box on the copied image
        cv2.rectangle(image_with_boxes, (x, y), (x+w, y+h), (0, 0, 255), 2)
        
        text = extract_text_from_region(image, region, field)
        print(f"{field}: {text}")
        
        if field == 'Power':
            match = re.search(r'(\d+\.?\d*M?)', text)
            data[field] = match.group(1) if match else ''
        elif field in ['Weekly_Club_Exp', 'Total_Club_Exp', 'Leadership']:
            match = re.search(r'(\d+)', text)
            data[field] = match.group(1) if match else ''
        elif field in ['DNA_Strength']:
            match = re.search(r'(\d+\.?\d*[KM]?)', text)
            data[field] = match.group(1) if match else ''
        else:
            data[field] = text
    
    # Extract the name (assuming it's already in the data dictionary)
    name = data.get('Name', 'Unknown')
    
    # Clean the name to make it suitable for a filename
    clean_name = re.sub(r'[^\w\-_\. ]', '_', name)
    
    # Save the image with boxes, using the name as prefix
    output_image_path = os.path.join('output', f'{clean_name}_{os.path.basename(image_path)}')
    cv2.imwrite(output_image_path, image_with_boxes)
    
    # print(f"Extracted data:")
    # print(data)
    # print(f"Image with boxes saved as: {output_image_path}")
    print("-" * 50)
    return data
    
def main():
    # print("Files in the screenshots folder:")
    # for filename in os.listdir('screenshots'):
        # print(filename)
    
    # Create output folder if it doesn't exist
    if not os.path.exists('output'):
        os.makedirs('output')
    
    data = []
    for filename in os.listdir('screenshots'):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join('screenshots', filename)
            try:
                extracted_data = process_image(image_path)
                if extracted_data:
                    data.append(extracted_data)
                else:
                    print(f"Warning: No data extracted from {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
    
    if data:
        with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'Power', 'Weekly_Club_Exp', 'Total_Club_Exp', 'DNA_Strength', 'Leadership']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        print(f"Data saved to output.csv")
    else:
        print("No data was extracted from the images.")

if __name__ == '__main__':
    main()