import re

# ------------------ CONSTANTS ------------------

DESIGNATION_KEYWORDS = [
    "manager", "executive", "officer", "director",
    "founder", "ceo", "cto", "lead"
]

INDIAN_STATES = [
    "andhra pradesh", "arunachal pradesh", "assam", "bihar",
    "chhattisgarh", "goa", "gujarat", "haryana",
    "himachal pradesh", "jharkhand", "karnataka", "kerala",
    "madhya pradesh", "maharashtra", "manipur", "meghalaya",
    "mizoram", "nagaland", "odisha", "punjab", "rajasthan",
    "sikkim", "tamilnadu", "tamil nadu", "telangana",
    "tripura", "uttar pradesh", "uttarakhand", "west bengal",
    "delhi", "jammu and kashmir", "ladakh", "puducherry",
    "chandigarh", "andaman and nicobar", "lakshadweep",
    "dadra and nagar haveli", "daman and diu"
]

# ------------------ HELPERS ------------------

def normalize_website(text):
    text = text.lower().replace(" ", "")
    if text.startswith("www") and not text.startswith("www."):
        text = "www." + text[3:]
    return text

def looks_like_name(text):
    return (
        (text.isupper() or text.istitle())
        and len(text.split()) <= 3
        and not any(ch.isdigit() for ch in text)
    )

def looks_like_company(text):
    if any(ch.isdigit() for ch in text):
        return False
    if "@" in text or "www" in text.lower():
        return False
    return len(text.split()) >= 2

# ------------------ MAIN FUNCTION ------------------

def extract_fields(ocr_texts):
    """
    ocr_texts: list[str] from easyocr (detail=0)
    """

    data = {
        "company_name": "",
        "card_holder": "",
        "designation": "",
        "phone": "",
        "email": "",
        "website": "",
        "area": "",
        "city": "",
        "state": "",
        "pincode": ""
    }

    phones = []
    address_lines = []

    # -------- PASS 1: BASIC FIELD EXTRACTION --------
    for i, text in enumerate(ocr_texts):
        t = text.strip()
        tl = t.lower()

        # EMAIL
        if "@" in t and not data["email"]:
            data["email"] = t.lower()

        # WEBSITE
        elif "www" in tl and not data["website"]:
            data["website"] = normalize_website(t)

        # PHONE
        elif re.search(r"\+?\d[\d\s\-()]{8,}", t):
            num = re.sub(r"[^\d+]", "", t)
            if len(num) >= 10:
                phones.append(num)

        # PINCODE
        elif re.search(r"\b\d{6}\b", t):
            data["pincode"] = re.search(r"\b\d{6}\b", t).group()
            address_lines.append(t)

        # DESIGNATION
        elif any(word in tl for word in DESIGNATION_KEYWORDS):
            data["designation"] = t

            # Name is directly ABOVE designation
            if i > 0 and looks_like_name(ocr_texts[i - 1]):
                data["card_holder"] = ocr_texts[i - 1]

        else:
            address_lines.append(t)

    # -------- PHONE JOIN --------
    data["phone"] = ", ".join(dict.fromkeys(phones))

    # -------- STATE DETECTION --------
    full_text = " ".join(ocr_texts).lower()
    for state in INDIAN_STATES:
        if state in full_text:
            data["state"] = state.title()
            break

    # -------- COMPANY NAME --------
    for t in ocr_texts:
        if (
            t != data["card_holder"]
            and t != data["designation"]
            and looks_like_company(t)
        ):
            data["company_name"] = t
            break

    # -------- AREA + CITY LOGIC --------
    area = " ".join(address_lines)

    # Remove known fields from area
    for remove in [
        data["company_name"],
        data["card_holder"],
        data["designation"],
        data["state"],
        data["pincode"]
    ]:
        if remove:
            area = area.replace(remove, "")

    area = re.sub(r"\s+", " ", area).strip()

    # City from comma rule
    if "," in area:
        left, right = area.split(",", 1)
        data["area"] = left.strip()
        data["city"] = right.split(";")[0].strip()
    else:
        data["area"] = area

    return data
