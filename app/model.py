from transformers import ViTFeatureExtractor, ViTForImageClassification
from PIL import Image

model = ViTForImageClassification.from_pretrained("nateraw/vit-age-classifier")
feature_extractor = ViTFeatureExtractor.from_pretrained("nateraw/vit-age-classifier")


def load_model():
    model.eval()
    return model


def prepare_image(image_path):
    image = Image.open(image_path)
    inputs = feature_extractor(images=image, return_tensors="pt")
    return inputs


def predict(inputs):
    outputs = model(**inputs)
    preds = outputs.logits.argmax(-1)
    return preds.item()
