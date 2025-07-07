# OCRitto - PDF Question Splitter with OCR

**OCRitto** is a Python-based OCR pipeline that intelligently processes exam-style PDFs to extract and separate questions and explanations. Designed for structured exam papers (e.g., tryouts, practice exams), OCRitto leverages image processing and Tesseract OCR to automate the separation of question content into organized folders.

## ✨ Features

- 🖨 Convert multi-page PDFs to clean, cropped images
- 🔎 Detects keywords like `Nomor`, `Materi`, and `Pembahasan` using Tesseract OCR
- ✂️ Automatically splits **questions** and **explanations**
- 📁 Saves output images into folder structure by subject and package name
- 🔄 Batch-processes multiple PDF files in one go

## 📁 Folder Structure

```
.
├── pdf/                    # Input PDF files
├── result/
│   └── <subject>/<package>/
│       ├── soal/           # Cropped question images
│       └── pembahasan/     # Cropped explanation images
├── main.py                 # Main script
└── README.md               # You are here
```

## ⚙️ Requirements

- Python 3.7+
- Tesseract OCR installed on your system (e.g., [Tesseract OCR](https://github.com/tesseract-ocr/tesseract))

## 📦 Dependencies

```
python
pytesseract
pyMuPDF
opencv-python
numpy
Pillow
```

Install them all using:
```bash
pip install -r requirements.txt
```

## 🔧 Configuration

Set the path to your Tesseract executable inside the script:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

## 🚀 How to Use

1. Put your exam PDFs in the `./pdf/` directory
2. Run the main script:
   ```bash
   python main.py
   ```
3. Output will be stored inside the `./result/` folder

Example output:
```
result/
└── Matematika/01/
    ├── soal/
    │   ├── soal_1_Logaritma.jpg
    │   └── soal_2_Aljabar.jpg
    └── pembahasan/
        ├── pembahasan_soal_1_Logaritma.jpg
        └── pembahasan_soal_2_Aljabar.jpg
```

## 🧠 How It Works

1. PDF is converted to high-res images (with margin cropped)
2. OCR is performed to find vertical coordinates of questions
3. Keywords detected:
   - **Nomor** → Used to split each question section
   - **Pembahasan** → Used to separate question from explanation
   - **Materi** → Extracted to name the files with relevant topic
4. Each question and explanation is saved as a separate `.jpg`

## 📝 Notes

- Assumes a consistent PDF layout (e.g., all questions labeled with "Nomor", "Pembahasan", etc.)
- You can tweak detection confidence or OCR configs via:
  ```python
  custom_config = r'-c tessedit_char_whitelist=... --psm 6'
  ```
- If OCR detection fails, the PDF is skipped and folder is auto-deleted
