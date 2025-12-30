# 📇 BizCardX – Business Card OCR Application

## 📌 Overview
BizCardX is a Streamlit-based web application that extracts key information from business card images using OCR.  
Users can review, edit, store, update, and delete extracted data in a MySQL database.

---

## 🛠 Technologies Used
- Python
- Streamlit
- EasyOCR
- MySQL
- OpenCV
- Regular Expressions (Regex)

---

## 🚀 Features
- Upload business card images
- Extract company name, card holder, designation, phone, email, website, address, state, and pincode
- Edit extracted details before saving
- Store data and image in MySQL
- View, update, and delete records

---

## ⚙️ How It Works
1. Upload business card image
2. OCR extracts raw text using EasyOCR
3. Rule-based logic parses required fields
4. Data displayed in UI for review
5. Save, update, or delete data in MySQL

---

## ▶️ How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 👤 Author
Sailee Allyadwar

---
