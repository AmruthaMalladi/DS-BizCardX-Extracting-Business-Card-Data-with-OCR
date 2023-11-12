# Business Card Data Extraction and Management

## Overview

This Python script provides a comprehensive solution for extracting information from business cards and managing the data efficiently. The script utilizes optical character recognition (OCR) to extract text from images, processes the data, and allows users to modify and delete entries. Additionally, it incorporates a dashboard for visualizing the extracted data and uploading it to a MySQL database.

## Requirements

Ensure you have the required libraries installed before running the script. Install the necessary dependencies using:

```bash
pip install easyocr numpy pillow opencv-python pandas sqlalchemy mysql-connector-python streamlit
```

## Libraries Used

- **Scanning library**
  - `easyocr`: Optical Character Recognition library
  - `numpy`: Numerical operations on arrays
  - `PIL`: Python Imaging Library for image processing
  - `cv2`: OpenCV for computer vision tasks
  - `os`: Operating system interactions
  - `re`: Regular expression operations for text processing

- **Data frame libraries**
  - `pandas`: Data manipulation and analysis library

- **Database library**
  - `sqlalchemy`: SQL toolkit and Object-Relational Mapping (ORM)
  - `mysql.connector`: MySQL connector for Python

- **Dashboard library**
  - `streamlit`: Web application framework for creating interactive dashboards
  

## Dashboard Usage

1. **Data Extraction Zone:**
    - Upload a business card image (PNG, JPG, or JPEG).
    - The OCR library extracts text from the image.
    - The extracted text is displayed on the dashboard with a yellow box around it.
    - The processed data is converted into a Pandas DataFrame and displayed.

2. **Data Modification Zone:**
    - Two tabs are provided: "Edit option" and "Delete option."
    - **Edit Option:**
        - Select a cardholder's name from the dropdown list.
        - Modify the details as needed and click the "Update" button.
    - **Delete Option:**
        - Select a cardholder's name from the dropdown list.
        - Click the "Delete" button to remove the selected cardholder's details from the database.

3. **Data Upload to MySQL:**
    - After data extraction, click the "Upload to MySQL DB" button to store the data in a MySQL database.
    - Database connection details (host, user, password) can be configured in the script.

## How to Run

Run the script using the following command:

```bash
streamlit run script_name.py
```

Access the dashboard through the provided URL in your web browser.

## Note

- Ensure the required MySQL server is running and accessible.
- The script uses the `easyocr` library for OCR. If not installed, follow the provided instructions.

## Contributors

- Add your name here if you contribute to this project.

Feel free to contribute, report issues, or suggest improvements to make this business card data extraction and management tool more robust and user-friendly.
