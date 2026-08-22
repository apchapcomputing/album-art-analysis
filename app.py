import gradio as gr
import spaces

from fastai.vision.all import *
from pathlib import Path


MODEL_DIR = Path('models')
MODEL_PATHS = [('3-format', 'model_3format.pkl'), ('5-format', 'model_5format.pkl')]
FORMAT_CATEGORIES = {
    '3-format': 'digital, small physical compact, large physical vinyl',
    '5-format': 'vinyl, cassette tape, cd, digital download, streaming'
}


models = {}

def load_models():
    for name, filename in MODEL_PATHS:
        pkl = MODEL_DIR / filename
        if pkl.exists():
            models[name] = load_learner(pkl)

load_models()

@spaces.GPU(duration=120)
def predict(img, model):
    if not models:
        raise gr.Error('No models found.')
    if model not in models:
        raise gr.Error(f'{model} not found.')

    learn = models[model]
    pred, _, probs = learn.predict(img)
    return dict(zip(learn.dls.vocab, map(float, probs)))

demo = gr.Interface(
    fn=predict,
    inputs=[
        gr.Image(type='pil', label='Share Album Art'),
        gr.Radio(
            choices=list(FORMAT_CATEGORIES.keys()),
            value='3-format',
            label='Classification Model',
            info='Classify into 3 formats (digital, small physical compact, large physical vinyl) or 5 formats (vinyl, cassette tape, cd, digital download, streaming)',
        )
    ],
    outputs=gr.Label(num_top_classes=5, label='Predicted Format'),
    title='Album Art Format Classifier',
    description='Upload an album cover, then the model predicts which music format era it belongs.',
    examples=[],
    # allow_flagging='never',
)


if __name__ == '__main__':
    demo.launch()
