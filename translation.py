import pandas as pd
from transformers import M2M100Tokenizer, M2M100ForConditionalGeneration
import torch

# Khởi tạo tokenizer
tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M", use_fast=False, src_lang="ko", tgt_lang="vi")

# Tải mô hình từ checkpoint
model_path = "float_16model"
model = M2M100ForConditionalGeneration.from_pretrained(model_path)

if torch.cuda.is_available():
    model = model.cuda()

def translate_korean_to_vietnamese(text):
    # Encode the Korean text
    encoded_korean = tokenizer(text, return_tensors="pt")

    # Move to GPU
    if torch.cuda.is_available():
        encoded_korean = {k: v.cuda() for k, v in encoded_korean.items()}

    # Perform translation
    with torch.no_grad():
        translated = model.generate(**encoded_korean)

    # Decode the Vietnamese text
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    return translated_text
