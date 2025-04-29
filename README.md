# PDF Table Extraction with OCR & Tabula

This repository contains two scripts for extracting tables from PDFs, either defined or as screenshots, and saving them in various formats (CSV, Excel, JSON).

## Scripts

### 1. **Tabula-based Extraction**  
Uses `tabula-py` to extract tables directly from PDFs with defined tables.  
Supports extracting tables from PDF URLs, then saves them to CSV, Excel, and JSON formats.

### 2. **OCR-based Screenshot Extraction**  
Uses `pdfplumber` to convert PDFs to images and `pytesseract` for Optical Character Recognition (OCR).  
Detects table structures from images (screenshots of tables) using `OpenCV`, and then performs OCR to extract data.  
Saves extracted tables as JSON files.

## Key Features
- **Tabula-based Extraction**: Efficiently extracts tables from PDFs with pre-defined table structures.
- **OCR-based Extraction**: Handles PDFs with screenshots of tables, using OCR to extract data.
- Supports saving output in CSV, Excel, and JSON formats for further processing.

## Installation

Install dependencies with:

```bash
pip install -r requirements.txt
