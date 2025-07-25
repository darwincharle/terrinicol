import wikipedia
import requests
from PIL import Image
from io import BytesIO
import os

wikipedia.set_lang("es")

def get_wiki_content(element_name):
    try:
        return wikipedia.summary(f"{element_name} (elemento)")
    except:
        return f"No se pudo cargar información sobre {element_name} desde Wikipedia."

def get_wiki_image(element_name):
    try:
        page = wikipedia.page(f"{element_name} (elemento)")
        img_url = next(img for img in page.images if img.lower().endswith(('.jpg', '.png')))
        response = requests.get(img_url, timeout=10)
        return Image.open(BytesIO(response.content))
    except:
        # Fallback a imagen local
        return "assets/images/default_element.png"