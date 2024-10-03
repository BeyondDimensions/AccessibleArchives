from utils import logger
from langchain_community.llms.ollama import Ollama
from config import TEMP_MODELS
from openai import OpenAI

client = OpenAI()


def prompt_llm(prompt: str, model_name: str) -> str:
    """Prompt the specified LLM model and return the response.

    Args:
        prompt (str): The user input or question.
        model_name (str): The name of the model to use (e.g., 'Llama3', 'ChatGPT').

    Returns:
        str: The generated response from the LLM.
    """
    try:
        # TODO Initialize memory

        # Based on the selected model, prompt the LLM
        match model_name:
            case 'Llama3':
                # Logic for using the Ollama Llama3 model
                logger.info("Using Llama3 model")
                response = Ollama(model=TEMP_MODELS.get(model_name)).invoke(
                    prompt)  # Pass prompt as a list
            case 'ChatGPT':
                # Logic for using the ChatGPT model
                logger.info("Using ChatGPT model")
                completion = client.chat.completions.create(
                    model=TEMP_MODELS.get(model_name),
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                  "type": "text",
                                  "text": prompt
                                }
                            ]
                        }
                    ]
                )
                response = completion.choices[0].message.content
            case None:
                raise ValueError("Model name must not be None.")
            case _:
                raise ValueError(f"Unsupported model: {model_name}")

        # TODO Add LLM response to memory

        # Since we pass a list of prompts, return the first response
        return response

    except Exception as e:
        logger.error(f"Failed to generate response: {e}")
        raise e
