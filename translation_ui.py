import gradio as gr
import time
from src.translator import TopikTranslator
from utils.utils import split_into_sentences


ckpt = './ckpts'
device = 'cuda'
engine = TopikTranslator(ckpt=ckpt, device=device)


def process(kr_input, history):
    try:
        sentences = split_into_sentences(kr_input)
        stream_result = ''
        for l, sen in enumerate(sentences):
            result = engine(sen)
            result = result.split(' ')
            for r, text in enumerate(result):
                if r != len(result):
                    stream_result += text + ' '
                else:
                    stream_result += '. '
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
