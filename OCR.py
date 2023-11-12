# =====================================================   /   /   Import library   /   /   ================================================= #

# [Scanning library]
import easyocr  # (Optical Character Recognition)
import numpy as np
from PIL import Image, ImageDraw
import cv2
import os
import re

# [Data frame libraries]
import pandas as pd

# [Database library]
import sqlalchemy
import mysql.connector
from sqlalchemy import create_engine, inspect

# [Dashboard library]
import streamlit as st

# ===================================================   /   /   Dash Board   /   /   ======================================================== #

# Configuring Streamlit GUI
st.set_page_config(layout='wide')

# Title
st.title('Business Card Data Extraction')

# Tabs
tab1, tab2 = st.columns(["Data Extraction zone", "Data modification zone"])

# ==========================================   /   /   Data Extraction and upload zone   /   /   ============================================== #

with tab1:
    st.subheader('Data Extraction')

    # Image file uploaded
    import_image = st.file_uploader('Select a business card (Image file)', type=['png', 'jpg', 'jpeg'],
                                    accept_multiple_files=False)

    # Note
    st.markdown('''File extension support: PNG, JPG, TIFF, File size limit: 2 Mb, Image dimension limit: 1500 pixels, Language: English.''')

    # --------------------------------      /   Extraction process   /     ---------------------------------- #

    if import_image is not None:
        try:
            # Create the reader object with desired languages
            reader = easyocr.Reader(['en'], gpu=False)

        except:
            st.info("Error: easyocr module is not installed. Please install it.")

        try:
            # Read the image file as a PIL Image object
            if isinstance(import_image, str):
                image = Image.open(import_image)
            elif isinstance(import_image, Image.Image):
                image = import_image
            else:
                image = Image.open(import_image)

            image_array = np.array(image)
            text_read = reader.readtext(image_array)

            result = []
            for text in text_read:
                result.append(text[1])

        except:
            st.info("Error: Failed to process the image. Please try again with a different image.")

    # -------------------------      /   Display the processed card with a yellow box   /     ---------------------- #

        col1, col2 = st.columns(2)

        with col1:
            # Define a function to draw the box on the image
            def draw_boxes(image, text_read, color='yellow', width=2):
                # Create a new image with bounding boxes
                image_with_boxes = image.copy()
                draw = ImageDraw.Draw(image_with_boxes)

                # Draw boundaries
                for bound in text_read:
                    p0, p1, p2, p3 = bound[0]
                    draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
                return image_with_boxes

            # Function calling
            result_image = draw_boxes(image, text_read)

            # Result image
            st.image(result_image, caption='Captured text')

    # ----------------------------    /     Data processing and converted into a data frame   /   ------------------ #

        with col2:
            # Initialize the data dictionary
            data = {
                "Company_name": [],
                "Card_holder": [],
                "Designation": [],
                "Mobile_number": [],
                "Email": [],
                "Website": [],
                "Area": [],
                "City": [],
                "State": [],
                "Pin_code": [],
            }

            # Function define
            def get_data(res):
                city = ""  # Initialize the city variable
                for ind, i in enumerate(res):
                    # To get WEBSITE_URL
                    if "www " in i.lower() or "www." in i.lower():
                        data["Website"].append(i)
                    elif "WWW" in i:
                        data["Website"].append(res[ind - 1] + "." + res[ind])

                    # To get EMAIL ID
                    elif "@" in i:
                        data["Email"].append(i)

                    # To get MOBILE NUMBER
                    elif "-" in i:
                        data["Mobile_number"].append(i)
                        if len(data["Mobile_number"]) == 2:
                            data["Mobile_number"] = " & ".join(data["Mobile_number"])

                    # To get COMPANY NAME
                    elif ind == len(res) - 1:
                        data["Company_name"].append(i)

                    # To get CARD HOLDER NAME
                    elif ind == 0:
                        data["Card_holder"].append(i)

                    # To get DESIGNATION
                    elif ind == 1:
                        data["Designation"].append(i)

                    # To get AREA
                    if re.findall("^[0-9].+, [a-zA-Z]+", i):
                        data["Area"].append(i.split(",")[0])
                    elif re.findall("[0-9] [a-zA-Z]+", i):
                        data["Area"].append(i)

                    # To get CITY NAME
                    match1 = re.findall(".+St , ([a-zA-Z]+).+", i)
                    match2 = re.findall(".+St,, ([a-zA-Z]+).+", i)
                    match3 = re.findall("^[E].*", i)
                    if match1:
                        city = match1[0]  # Assign the matched city value
                    elif match2:
                        city = match2[0]  # Assign the matched city value
                    elif match3:
                        city = match3[0]  # Assign the matched city value

                    # To get STATE
                    state_match = re.findall("[a-zA-Z]{9} +[0-9]", i)
                    if state_match:
                        data["State"].append(i[:9])
                    elif re.findall("^[0-9].+, ([a-zA-Z]+);", i):
                        data["State"].append(i.split()[-1])
                    if len(data["State"]) == 2:
                        data["State"].pop(0)

                    # To get PINCODE
                    if len(i) >= 6 and i.isdigit():
                        data["Pin_code
