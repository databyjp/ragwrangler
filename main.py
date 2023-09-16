from typing import Union

import openai
import os
import db
from weaviate.util import generate_uuid5
import prompts
import logging


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
logger = logging.getLogger(__name__)


GPT_MODELS = ["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k"]
ALL_MODELS = GPT_MODELS

openai.api_key = os.environ["OPENAI_APIKEY"]
client = db.initialize()


class RAGTask:
    """
    A class representing a task to be handled by the RAG system.

    Attributes:
        task_prompt_template (str): The template to be used for creating the task prompt.
            It must contain the placeholder "{source_text}".
        generated_text (str): The text generated as output for the task.
    """
    def __init__(self, task_prompt_template: str):
        if "{source_text}" not in task_prompt_template:
            raise ValueError('task_prompt_template must contain "{source_text}" placeholder')
        self.task_prompt_template = task_prompt_template
        self.generated_text = None

    def get_output(self, source_text: str, model_name: str = "gpt-3.5-turbo"):
        """
        Get the output for the task, either by generating it or fetching from Weaviate.
        :param source_text: The source text based on which the task is created.
        :param model_name: The name of the model to use for generating output.
        :return: The generated output.
        """
        # Check if the output can be fetched from Weaviate using the UUID
        task_prompt = self.task_prompt_template.format(source_text=source_text)
        uuid = generate_uuid5(task_prompt)

        fetched_object = db.load_generated_text(client, uuid)
        if fetched_object is not None:
            logger.info(f"Found {uuid} in Weaviate")
            return fetched_object
        else:
            logger.warning(f"Could not find {uuid} in Weaviate")

        # Generate output using the specified model and save it to Weaviate
        logger.info(f"Generating output for {truncate_text(task_prompt)}")
        generated_text = call_llm(task_prompt, model_name=model_name)
        uuid = db.save_generated_text(client, task_prompt, generated_text, uuid)
        logger.info(f"Saved {uuid} to Weaviate")
        return generated_text


def truncate_text(text_input: str, max_length: int = 50) -> str:
    """
    Truncate a text to a specified maximum length, adding ellipsis if truncated.
    :param text_input: The input text.
    :param max_length: The maximum allowed length for the output text.
    :return:
    """
    if len(text_input) > max_length:
        return text_input[:max_length] + "..."
    else:
        return text_input


def call_llm(prompt: str, model_name: str = "gpt-3.5-turbo") -> str:
    """
    Call the language model with a specific prompt and model name.
    :param prompt: The prompt to be used.
    :param model_name: The name of the model to be used.
    :return: The output from the language model.
    """
    logger.info(f"Calling {model_name} with prompt: {truncate_text(prompt)}")
    if model_name not in ALL_MODELS:
        raise ValueError(f"Model name {model_name} not recognised")

    if "gpt" in model_name:
        return call_chatgpt(prompt, model_name)
    else:
        raise ValueError(f"No function exists to handle for model {model_name}")


def call_chatgpt(prompt: str, model_name: str = "gpt-3.5-turbo") -> str:
    """
    Call the ChatGPT model with a specific prompt.
    :param prompt: The prompt to be used.
    :param model_name: The name of the model to be used.
    :return:
    """

    completion = openai.ChatCompletion.create(
        model=model_name,
        messages=[
            prompts.system_prompt,
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message["content"]


def main():
    source_text = prompts.test_source_text
    task = RAGTask(task_prompt_template=prompts.REVISION_QUIZ)
    output = task.get_output(source_text=source_text)
    print(truncate_text(str(output)))
    print(output)


if __name__ == "__main__":
    main()
