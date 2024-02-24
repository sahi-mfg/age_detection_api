from PIL import Image
from transformers import ViTForImageClassification, ViTImageProcessor  # type: ignore


def load_model():
    model = ViTForImageClassification.from_pretrained("nateraw/vit-age-classifier")
    return model


def load_feature_extractor():
    feature_extractor = ViTImageProcessor.from_pretrained("nateraw/vit-age-classifier")
    return feature_extractor


def prepare_image(image, feature_extractor):
    if not isinstance(image, Image.Image):
        image = Image.open(image).convert("RGB")
    inputs = feature_extractor(images=image, return_tensors="pt")
    return inputs


def predict(inputs, model):
    outputs = model(**inputs)
    # Get the class index with the highest probability
    class_index = outputs.logits.argmax(-1).item()
    # Map the class index to the corresponding age range
    age_ranges = ["0-2", "3-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"]
    predicted_age_range = age_ranges[class_index]
    return predicted_age_range
