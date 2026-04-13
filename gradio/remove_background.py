import gradio as gd
from transformers import pipeline

pipeline_model = pipeline("image-segmentation", model="briaai/RMBG-1.4", trust_remote_code=True)

def remove_background(img):
    return pipeline_model(img)

app = gd.Interface(
    title="Remove Background na Imagem",
    description="Faça upload da imagem para remover o background",
    fn=remove_background,
    inputs=gd.components.Image(type="pil"),
    outputs=gd.components.Image(type="pil", format="png")
)

app.launch(share=True)