import torch
import open_clip
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"

model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32",
    pretrained="openai"
)
model = model.to(device)
tokenizer = open_clip.get_tokenizer("ViT-B-32")

def score_image(image_path, prompt):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    text = tokenizer([prompt]).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)

    image_features /= image_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)

    return (image_features @ text_features.T).item()
