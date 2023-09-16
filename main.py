import openai
import os
import db
from weaviate.util import generate_uuid5
import prompts
from typing import Literal
import logging


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
logger = logging.getLogger(__name__)


openai.api_key = os.environ["OPENAI_APIKEY"]
client = db.initialize()


class RAGTask:
    def __init__(self, source_text: str):
        self.source_text = source_text
        self.task_prompt = None
        self.uuid = None
        self.generated_text = None

    def get_output(self, model_name: Literal["gpt-3.5-turbo", "gpt-4"] = "gpt-3.5-turbo"):
        if self.uuid is not None:
            fetched_object = self.load_from_weaviate()
            if fetched_object is not None:
                logger.info(f"Found {self.uuid} in Weaviate")
                return fetched_object
            else:
                logger.warning(f"Could not find {self.uuid} in Weaviate")

        logger.info(f"Generating output for {truncate_text(self.task_prompt)}")
        generated_text = self.generate_output(model_name=model_name)
        uuid = self.save_to_weaviate(generated_text, self.uuid)
        logger.info(f"Saved {uuid} to Weaviate")
        return generated_text

    def generate_output(self, model_name: Literal["gpt-3.5-turbo", "gpt-4"] = "gpt-3.5-turbo"):
        return call_llm(self.task_prompt, model_name=model_name)

    def load_from_weaviate(self):
        weaviate_response = client.data_object.get(uuid=self.uuid, class_name=db.OUTPUT_COLLECTION)
        return weaviate_response["properties"]["generated_text"]

    def save_to_weaviate(self, generated_text, uuid):
        data_object = {
            "prompt": self.task_prompt,
            "generated_text": generated_text
        }
        uuid_out = db.add_object(client, data_object, uuid)
        return uuid_out


class RAGRevisionQuiz(RAGTask):
    def __init__(self, source_text: str):
        super().__init__(source_text)
        self.task_prompt = self.get_task_prompt()
        self.uuid = generate_uuid5(self.task_prompt)

    def get_task_prompt(self):
        task_prompt = prompts.quiz_prompt(self.source_text)
        return task_prompt


def truncate_text(text_input: str, max_length: int = 50) -> str:
    if len(text_input) > max_length:
        return text_input[:max_length] + "..."
    else:
        return text_input


def call_llm(prompt: str, model_name: Literal["gpt-3.5-turbo", "gpt-4"] = "gpt-3.5-turbo") -> str:
    logger.info(f"Calling {model_name} with prompt: {truncate_text(prompt)}")
    if model_name == "gpt-3.5-turbo":
        return call_chatgpt(prompt, use_gpt_4=False)
    elif model_name == "gpt-4":
        return call_chatgpt(prompt, use_gpt_4=True)
    else:
        raise ValueError(f"Model name {model_name} not recognised")


def call_chatgpt(prompt: str, use_gpt_4: bool = False) -> str:
    if use_gpt_4 is False:
        model_name = "gpt-3.5-turbo"
    else:
        model_name = "gpt-4"

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
    task = RAGRevisionQuiz(prompts.test_source_text)
    output = task.get_output()
    print(truncate_text(str(output)))


if __name__ == "__main__":
    main()
