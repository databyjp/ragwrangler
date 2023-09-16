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
        source_text (str): The source text based on which the task is created.
        task_prompt (str): The prompt to be used for the task.
        uuid (str): The UUID of the task.
        generated_text (str): The text generated as output for the task.
    """
    def __init__(self, source_text: str, task_prompt: str):
        self.source_text = source_text
        self.task_prompt = task_prompt
        self.uuid = generate_uuid5(task_prompt)  # Generate UUID based on the task prompt
        self.generated_text = None

    def get_output(self, model_name: str = "gpt-3.5-turbo"):
        """
        Get the output for the task, either by generating it or fetching from Weaviate.
        :param model_name: The name of the model to use for generating output.
        :return: The generated output.
        """
        # Check if the output can be fetched from Weaviate using the UUID
        if self.uuid is not None:
            fetched_object = self.load_from_weaviate()
            if fetched_object is not None:
                logger.info(f"Found {self.uuid} in Weaviate")
                return fetched_object
            else:
                logger.warning(f"Could not find {self.uuid} in Weaviate")

        # Generate output using the specified model and save it to Weaviate
        logger.info(f"Generating output for {truncate_text(self.task_prompt)}")
        generated_text = self.generate_output(model_name=model_name)
        uuid = self.save_to_weaviate(generated_text, self.uuid)
        logger.info(f"Saved {uuid} to Weaviate")
        return generated_text

    def generate_output(self, model_name: str = "gpt-3.5-turbo"):
        """
        Generate output using a specific model.
        :param model_name: The name of the model to be used. Default is "gpt-3.5-turbo".
        :return: The generated output.
        """
        return call_llm(self.task_prompt, model_name=model_name)

    def load_from_weaviate(self) -> Union[str, None]:
        """
        Load the generated output from Weaviate using the task's uuid.
        :return: The generated text retrieved from Weaviate.
        """
        weaviate_response = client.data_object.get(uuid=self.uuid, class_name=db.OUTPUT_COLLECTION)
        if weaviate_response is None:
            return None
        else:
            return weaviate_response["properties"]["generated_text"]

    def save_to_weaviate(self, generated_text, uuid) -> str:
        """
        Save the generated output to Weaviate.
        :param generated_text: The text to be saved.
        :param uuid: The unique identifier for the object being saved.
        :return: The unique identifier of the saved object.
        """
        data_object = {
            "prompt": self.task_prompt,
            "generated_text": generated_text
        }
        uuid_out = db.add_object(client, data_object, uuid)
        assert uuid_out == uuid, f"UUIDs do not match: {uuid_out} != {uuid}"
        return uuid_out


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
    task_prompt = prompts.revision_quiz_json(source_text)
    task = RAGTask(source_text, task_prompt)
    print(task.uuid)
    output = task.get_output()
    print(truncate_text(str(output)))
    print(output)


if __name__ == "__main__":
    main()
