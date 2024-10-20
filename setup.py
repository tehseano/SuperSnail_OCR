from setuptools import setup, find_packages

setup(
    name="ocr_scan",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "pillow",
        "pytesseract",
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "ocr_scan=scan:main",
        ],
    },
)