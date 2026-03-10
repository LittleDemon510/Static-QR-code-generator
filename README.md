# QR Generator 🔲

A simple browser-based QR code generator built with Python. Run it from your terminal and it opens in your browser — no complicated setup needed.

---

## What It Does

- Takes any URL as input
- Lets you customise 4 colors: **Dots**, **Background**, **Eye Frame**, and **Eye Center**
- Generates a styled QR code instantly in your browser
- Lets you download the QR code as a PNG file

---

## Requirements

- Python 3.7 or higher
- pip (comes with Python)

---

## Installation

**1. Clone or download this project into a folder:**
```bash
mkdir QR-Generator
cd QR-Generator
```

**2. Create a virtual environment:**
```bash
python3 -m venv venv
```

**3. Activate the virtual environment:**

On Mac/Linux:
```bash
source venv/bin/activate
```

On Windows:
```bash
venv\Scripts\activate
```

You'll see `(venv)` appear in your terminal when it's active.

**4. Install the dependencies:**
```bash
pip install "qrcode[pil]" pillow
```

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| `qrcode[pil]` | latest | Generates the QR code |
| `pillow` | latest | Image processing and color customisation |

> Note: `tkinter` and `http.server` are built into Python — no installation needed.

---

## How to Run

```bash
python3 qr_generator.py
```

This will automatically open the app at **http://localhost:5555** in your browser.

**To stop the app:** Press `Control+C` in the terminal (not Command+C).

---

## How to Use

1. Type or paste your URL into the input field
2. Click the 4 color pickers to choose your colors
3. Click **Generate QR**
4. Click **Save PNG** to download your QR code

---

## Project Structure

```
QR-Generator/
├── venv/                  # Virtual environment (auto-generated)
├── qr_generator.py        # Main application file
└── README.md              # This file
```
