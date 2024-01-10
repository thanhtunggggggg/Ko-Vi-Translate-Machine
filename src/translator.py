from transformers import M2M100Tokenizer, M2M100ForConditionalGeneration
import torch


class TopikTranslator(object):
    def __init__(self, ckpt, device='cuda'):
        self.ckpt = ckpt
        self.tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M", use_fast=False, src_lang="ko",
                                                         tgt_lang="vi")
        self.model = M2M100ForConditionalGeneration.from_pretrained(ckpt)
        self.model = self.model.to(device)
        self.model.eval()
        self.device = device

    def __call__(self, kr_text):
        kr_text_enc = self.tokenizer(kr_text, return_tensors="pt")
        kr_text_enc.to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(**kr_text_enc)

        # Decode the Vietnamese text
        vn_text_dec = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
        return vn_text_dec[0]
