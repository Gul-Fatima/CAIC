import requests
from PIL import Image
from io import BytesIO

def download_image(url, path):
    try:
        r = requests.get(url, timeout=5)
        img = Image.open(BytesIO(r.content)).convert("RGB")
        img.save(path)
        return True
    except:
        return False
