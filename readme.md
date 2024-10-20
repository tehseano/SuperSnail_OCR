# Automated OCR Scan Script

This script automates the process of setting up the environment and running OCR to extract data from images of player profiles.

## Prerequisites

1. Ensure you have Python 3.8 or newer installed.
2. Install Tesseract OCR:
   - Windows: https://github.com/UB-Mannheim/tesseract/wiki
   - macOS: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`

## Setup and Usage

1. Clone this repository or download the files.
2. Place your images in the 'screenshots' folder.
3. Open a command prompt or terminal in the project directory.
4. Run the following command:

   ```
   python run_ocr.py
   ```

   This script will:
   - Create a virtual environment if it doesn't exist
   - Install all required dependencies
   - Run the OCR script on your images

5. The extracted data will be saved in 'output.csv', and images with bounding boxes will be saved in the 'output' folder.

## Troubleshooting

If you encounter any issues, ensure that:
- Tesseract is properly installed and its path is correctly set in your system's PATH environment variable.
- You have internet access for the script to download required packages.
- You have sufficient permissions to create directories and install packages in the project folder.

For any persistent issues, please check the error messages in the console output.

## Manual Setup (if needed)

If you prefer to set up the environment manually:

1. Create a virtual environment:
   ```
   python -m venv venv
   ```
2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
3. Install the required packages:
   ```
   pip install -e .
   ```
4. Run the script:
   ```
   python scan.py
   ```