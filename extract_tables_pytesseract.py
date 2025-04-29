import pdfplumber
import pytesseract
import cv2
import numpy as np
import json
from PIL import Image

def detect_table_cells(img_cv):
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Detect horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    detect_horizontal = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

    # Detect vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    detect_vertical = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel, iterations=2)

    # Combine detected lines
    table_mask = cv2.add(detect_horizontal, detect_vertical)

    # Find contours (cells)
    contours, _ = cv2.findContours(table_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cells = [cv2.boundingRect(c) for c in contours]

    return sorted(cells, key=lambda b: (b[1], b[0]))  # Sort by top first, then left

def group_cells_into_rows(cells, y_threshold=10):
    """
    Group detected cell bounding boxes into rows based on their Y position.
    """
    rows = []
    current_row = []
    previous_y = None

    for cell in cells:
        x, y, w, h = cell
        if previous_y is None:
            current_row.append(cell)
            previous_y = y
        else:
            if abs(y - previous_y) > y_threshold:
                # New row
                rows.append(sorted(current_row, key=lambda b: b[0]))  # Sort current row left-to-right
                current_row = [cell]
            else:
                current_row.append(cell)
            previous_y = y
    if current_row:
        rows.append(sorted(current_row, key=lambda b: b[0]))

    return rows

def extract_tables_from_screenshot_pdf(pdf_path):
    all_tables_json = {}

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            # Convert page to image
            img = page.to_image(resolution=300).original
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

            # Detect table cells
            cells = detect_table_cells(img_cv)
            rows = group_cells_into_rows(cells)

            page_data = []
            for row_cells in rows:
                row_data = []
                for (x, y, w, h) in row_cells:
                    # Crop and OCR each cell
                    cell_img = img.crop((x, y, x + w, y + h))
                    text = pytesseract.image_to_string(cell_img, config="--psm 6").strip()
                    row_data.append(text)
                page_data.append(row_data)

            all_tables_json[f"page_{page_num + 1}"] = page_data

    return all_tables_json

tables_json = extract_tables_from_screenshot_pdf("sample-tables.pdf")

print(json.dumps(tables_json, indent=2, ensure_ascii=False))

with open("./json_files/extracted_tables_pytesseract.json", "w", encoding="utf-8") as f:
    json.dump(tables_json, f, indent=2, ensure_ascii=False)
print("Tables extracted and saved to '/json_files/extracted_tables_pytesseract.json'")