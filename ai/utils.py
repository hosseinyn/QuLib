import re
import unicodedata

from shekar import Normalizer, OffensiveLanguageClassifier

normalizer = Normalizer()
classifier = OffensiveLanguageClassifier()

ZERO_WIDTH = re.compile(r"[\u200B\u200C\u200D\u2060\uFEFF]")

PUNCTUATION_AND_EMOJI = re.compile(
    r"[^\w\s\u0600-\u06FF]"
)

MULTI_SPACE = re.compile(r"\s+")


def predict(text: str) -> bool:
    """
    Predict whether a given text is offensive using Classifier.

    Args:
        text (str): The normalized text.

    Returns:
        bool: True if text is offensive, False otherwise.

    document by AI
    """
    try:
        label, confidence = classifier(text)
        return label == "offensive"
    except Exception:
        return False


def is_offensive(text: str) -> bool:
    """
    Check if a text contains offensive content.

    Args:
        text (str): The raw input text.

    Returns:
        bool: True if offensive content is detected, False otherwise.

    document by AI
    """
    if not text:
        return False

    text = unicodedata.normalize("NFKC", text)

    text = normalizer(text)

    text = ZERO_WIDTH.sub("", text)

    text = PUNCTUATION_AND_EMOJI.sub(" ", text)

    text = MULTI_SPACE.sub(" ", text).strip()

    collapsed = text.replace(" ", "")

    if predict(text):
        return True

    if predict(collapsed):
        return True
    
    if predict(text.lower()):
        return True
    
    if predict(collapsed.lower()):
        return True

    return False