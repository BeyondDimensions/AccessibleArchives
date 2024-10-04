from _load_src import SRC_PATH
import pytest
from llm import prompt_llm
from utils import logger
from config import TEMP_MODELS

# To see logging run: pytest -s tests/test_llm/test_prompting.py


@pytest.mark.parametrize("model_name", list(TEMP_MODELS.keys()))
def test_prompt_llm(model_name):
    # Test with a valid prompt and valid model
    prompt = "What is the capital of France? Give one word answer."

    response = prompt_llm(prompt, model_name)

    # Log the response for debugging
    logger.info(f"Model: {model_name}, Response: {response}")

    # Add assertion for the expected response
    assert response.strip().rstrip(".").lower(
    ) == "paris", f"Expected 'Paris', but got: {response}"


def test_prompt_llm_invalid_model():
    # Test with an invalid model name
    prompt = "Tell me something"
    model_name = "UnknownModel"

    # Check if ValueError is raised for an unsupported model
    with pytest.raises(ValueError, match=f"Unsupported model: {model_name}"):
        prompt_llm(prompt, model_name)


def test_prompt_llm_none_model():
    # Test with None as the model name
    prompt = "Tell me something"
    model_name = None

    # Check if ValueError is raised for None model
    with pytest.raises(ValueError, match="Model name must not be None."):
        prompt_llm(prompt, model_name)


def test_prompt_llm_empty_prompt():
    # Test with an empty prompt
    prompt = ""
    model_name = "Llama3"

    # Pass an empty prompt and check if the function handles it correctly
    response = prompt_llm(prompt, model_name)

    # Log the response for debugging
    logger.info(f"Model: {model_name}, Response: {response}")

    # Add assertion for handling an empty prompt (depends on your logic for handling empty inputs)
    assert response == "", f"Expected empty response, but got: {response}"
