from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
from config import MODELS, API_KEY

# Dictionary to cache loaded pipelines
model_pipes = {}


def get_pipeline(model_name):
    if model_name not in model_pipes:
        model_info = MODELS[model_name]
        tokenizer = AutoTokenizer.from_pretrained(
            model_info['path'], token=API_KEY, legacy=False)

        if model_info['type'] == 'seq2seq':
            model = AutoModelForSeq2SeqLM.from_pretrained(
                model_info['path'], token=API_KEY)
            pipe = pipeline("text2text-generation", model=model,
                            tokenizer=tokenizer, device=-1, max_length=1000)
        elif model_info['type'] == 'causal':
            model = AutoModelForCausalLM.from_pretrained(
                model_info['path'], token=API_KEY)
            pipe = pipeline("text-generation", model=model,
                            tokenizer=tokenizer, device=-1, max_length=1000)
        else:
            raise ValueError(f"Unsupported model type: {model_info['type']}")

        model_pipes[model_name] = pipe
    return model_pipes[model_name]


def generate_response(prompt, model_name):
    # Use the pipeline for text generation
    pipe = get_pipeline(model_name)
    if 'text2text-generation' in pipe.task:
        response = pipe(prompt)[0]['generated_text']
    elif 'text-generation' in pipe.task:
        response = pipe(prompt)[0]['generated_text']
    else:
        raise ValueError(f"Unsupported pipeline task: {pipe.task}")
    return response
