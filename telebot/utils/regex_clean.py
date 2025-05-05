import re

def clean_text(text: str) -> str:
    return re.sub(r'[^\w\s:]', '', text.lower().strip())