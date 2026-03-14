import os
import csv
from tqdm import tqdm

from search import search_images
from filter import score_image
from utils import download_image

PROMPT = "construction workers wearing PPE"
NUM_IMAGES = 200

os.makedirs("dataset/accepted", exist_ok=True)
os.makedirs("dataset/rejected", exist_ok=True)

urls = search_images(PROMPT, NUM_IMAGES)

rows = []

for idx, url in enumerate(tqdm(urls)):
    img_path = f"temp_{idx}.jpg"
    if not download_image(url, img_path):
        continue

    score = score_image(img_path, PROMPT)

    if score > 0.28:
        final_path = f"dataset/accepted/img_{idx}.jpg"
        kept = True
    else:
        final_path = f"dataset/rejected/img_{idx}.jpg"
        kept = False

    os.rename(img_path, final_path)

    rows.append([final_path, score, kept])

with open("dataset/report.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["image_path", "score", "kept"])
    writer.writerows(rows)
