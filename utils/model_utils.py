from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from config import MODELS, API_KEY
import torch
import time

# Dictionary to cache loaded models and tokenizers
model_pipes = {}


def get_model_and_tokenizer(model_name):
    if model_name not in model_pipes:
        model_info = MODELS[model_name]
        tokenizer = AutoTokenizer.from_pretrained(
            model_info['path'], token=API_KEY, legacy=False)

        # Enable 8-bit quantization
        quant_config = BitsAndBytesConfig(load_in_8bit=True)

        # Load model with reduced precision
        model = AutoModelForCausalLM.from_pretrained(
            model_info['path'],
            token=API_KEY,
            quantization_config=quant_config,
            torch_dtype=torch.float16
        )

        # Enable gradient checkpointing
        model.gradient_checkpointing_enable()

        # Store model and tokenizer
        model_pipes[model_name] = (model, tokenizer)
    return model_pipes[model_name]


def generate_response(prompt, model_name, max_length=50, delay=0.1):
    model, tokenizer = get_model_and_tokenizer(model_name)

    # Tokenize prompt
    input_ids = tokenizer.encode(prompt, return_tensors='pt')

    # Prepare for step-by-step generation
    generated_ids = input_ids
    response = tokenizer.decode(
        input_ids[0], skip_special_tokens=True)  # Initialize with prompt
    response_prefix_length = len(response)

    # Generate text step by step
    for _ in range(max_length):
        with torch.no_grad():
            # Get model output
            outputs = model(generated_ids)
            next_token_logits = outputs.logits[:, -1, :]

            # Get the most likely next token
            next_token_id = torch.argmax(
                next_token_logits, dim=-1).unsqueeze(-1)

            # Append the token to the generated sequence
            generated_ids = torch.cat((generated_ids, next_token_id), dim=1)

            # Decode the generated sequence
            current_text = tokenizer.decode(
                generated_ids[0], skip_special_tokens=True)

            # Update response with new tokens
            if len(current_text) > response_prefix_length:
                response = current_text
                yield response

            # Simulate delay for real-time display
            time.sleep(delay)

    return response


# from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
#
# # Dictionary to cache loaded pipelines
# model_pipes = {}
#
# def get_pipeline(model_name):
#     if model_name not in model_pipes:
#         model_info = MODELS[model_name]
#         tokenizer = AutoTokenizer.from_pretrained(model_info['path'], token=API_KEY, legacy=False)
#
#         # Enable 8-bit quantization
#         quant_config = BitsAndBytesConfig(load_in_8bit=True)
#
#         model = AutoModelForCausalLM.from_pretrained(model_info['path'], token=API_KEY, quantization_config=quant_config)
#
#         # Enable gradient checkpointing
#         model.gradient_checkpointing_enable()
#
#         # Adjust max_length to reduce memory usage
#         pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0 if torch.cuda.is_available() else -1, max_length=500)
#         model_pipes[model_name] = pipe
#     return model_pipes[model_name]
#
# def generate_response(prompt, model_name):
#     # Use the pipeline for text generation
#     pipe = get_pipeline(model_name)
#     response = pipe(prompt)[0]['generated_text']
#     return response
