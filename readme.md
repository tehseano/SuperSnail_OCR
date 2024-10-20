# OCR Scan Script

This script uses OCR to extract data from images of player profiles.

## Setup

1. Ensure you have Python 3.8 or newer installed.
2. Install Tesseract OCR:
   - Windows: https://github.com/UB-Mannheim/tesseract/wiki
   - macOS: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`
3. Clone this repository or download the files.
4. Navigate to the project directory in your terminal.
5. Create a virtual environment:
   ```
   python -m venv venv
   ```
6. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
7. Install the required packages:
   ```
   pip install -e .
   ```

## Usage

1. Place your images in the 'screenshots' folder.
2. Run the script:
   ```
   ocr_scan
   ```
3. The extracted data will be saved in 'output.csv', and images with bounding boxes will be saved in the 'output' folder.

## Troubleshooting

If you encounter any issues, ensure that Tesseract is properly installed and its path is correctly set in your system's PATH environment variable.
