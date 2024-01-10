from transformers import M2M100Tokenizer, M2M100ForConditionalGeneration
import torch
import gradio as gr
import time


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


ckpt = './ckpts'
device = 'cpu'
engine = TopikTranslator(ckpt=ckpt, device=device)


def process(kr_input, history):
    try:
        result = engine(kr_input)
        result = result.split(' ')
        stream_result = ''
        for text in result:
            stream_result += text + ' '
            time.sleep(0.05)
            yield stream_result
    except:
        result = 'Something not valid, please check again'
    return result


if __name__ == '__main__':
    #example = '오늘은 월요일입니다. 내일은 화요일입니다.'
    block = gr.Blocks().queue()
    with block:
        slider = gr.Slider(10, 100, render=False)
        gr.ChatInterface(
            process,
            title="Ko-Vi-Translate-Machine - Author: Thanh Tung"
        )

    block.launch(server_name='localhost', share=False)
