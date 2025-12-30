import easyocr
import numpy as np

# Initialize reader once
reader = easyocr.Reader(['en'], gpu=False)

def extract_text(image):
    """
    image: numpy array (RGB)
    returns: list of text strings
    """
    if image.dtype != np.uint8:
        image = image.astype(np.uint8)

    results = reader.readtext(image, detail=0)
    return [text.strip() for text in results if text.strip()]
