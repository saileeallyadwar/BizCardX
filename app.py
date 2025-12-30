import streamlit as st
import numpy as np
from PIL import Image

from ocr_engine import extract_text
from data_extraction import extract_fields
from database import insert_data, fetch_all, update_data, delete_data

st.set_page_config(page_title="BizCardX", layout="wide")
st.title("📇 BizCardX – Business Card OCR")

tab1, tab2 = st.tabs(["📤 Upload & Extract", "📂 Manage Database"])

# ---------- TAB 1 ----------
with tab1:
    uploaded_file = st.file_uploader(
        "Upload Business Card Image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, width=350)

        img_array = np.array(image)
        ocr_text = extract_text(img_array)
        extracted_data = extract_fields(ocr_text)

        st.subheader("📌 Extracted Information")
        st.json(extracted_data)

        if st.button("💾 Save to Database"):
            insert_data(extracted_data, uploaded_file.read())
            st.success("Data saved successfully!")

# ---------- TAB 2 ----------
with tab2:
    st.subheader("📂 Stored Business Cards")
    records = fetch_all()

    if records:
        for record in records:
            with st.expander(f"🆔 ID {record['id']} - {record['card_holder']}"):
                updated_data = {
                    "company_name": st.text_input("Company Name", record["company_name"], key=f"c{record['id']}"),
                    "card_holder": st.text_input("Card Holder", record["card_holder"], key=f"h{record['id']}"),
                    "designation": st.text_input("Designation", record["designation"], key=f"d{record['id']}"),
                    "phone": st.text_input("Phone", record["phone"], key=f"p{record['id']}"),
                    "email": st.text_input("Email", record["email"], key=f"e{record['id']}"),
                    "website": st.text_input("Website", record["website"], key=f"w{record['id']}"),
                    "area": st.text_input("Area", record["area"], key=f"a{record['id']}"),
                    "city": st.text_input("City", record["city"], key=f"ci{record['id']}"),
                    "state": st.text_input("State", record["state"], key=f"s{record['id']}"),
                    "pincode": st.text_input("Pincode", record["pincode"], key=f"pi{record['id']}")
                }

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✏️ Update", key=f"u{record['id']}"):
                        update_data(record["id"], updated_data)
                        st.success("Updated successfully!")
                with col2:
                    if st.button("🗑️ Delete", key=f"x{record['id']}"):
                        delete_data(record["id"])
                        st.warning("Deleted successfully!")
    else:
        st.info("No records found.")
