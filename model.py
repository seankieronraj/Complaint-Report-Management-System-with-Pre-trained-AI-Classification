from transformers import pipeline

# Load pre-trained model from Hugging Face
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# complaint categories mapping
CATEGORY_MAPPING = {
    "POSITIVE": "Service",
    "NEGATIVE": "Billing"
}


# categorize complaints using maped label
def classify_complaint(text):
    result = classifier(text)[0]  # Classify the text
    return CATEGORY_MAPPING.get(result["label"], "Other")
