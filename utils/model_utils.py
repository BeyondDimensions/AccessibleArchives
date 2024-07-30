from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from config import MODELS

# Dictionary to cache loaded pipelines
model_pipes = {}


def get_pipeline(model_name):
    if model_name not in model_pipes:
        tokenizer = AutoTokenizer.from_pretrained(
            MODELS[model_name], legacy=False)
        model = AutoModelForSeq2SeqLM.from_pretrained(MODELS[model_name])
        model_pipes[model_name] = pipeline(
            "text2text-generation", model=model, tokenizer=tokenizer, device=-1, max_length=1000)
    return model_pipes[model_name]


def generate_response(prompt, model_name):
    # Use the pipeline for text generation
    pipe = get_pipeline(model_name)
    response = pipe(prompt)[0]['generated_text']
    return response
