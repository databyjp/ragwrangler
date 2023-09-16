import openai
import weaviate
import os
from weaviate.util import generate_uuid5
import prompts
from typing import Literal


openai.api_key = os.environ["OPENAI_APIKEY"]


class RAGTask:
    def __init__(self, source_text: str):
        self.source_text = source_text
        self.task_prompt = None
        self.uuid = None
        self.generated_text = None

    def get_output(self, model_name: Literal["gpt-3.5-turbo", "gpt-4"] = "gpt-3.5-turbo"):
        # TODO:
        # Check if the text is already in the database
        # If it is, return the generated text
        # If it is not, generate the text and save it to the database
        return self.generate_output(model_name=model_name)

    def generate_output(self, model_name: Literal["gpt-3.5-turbo", "gpt-4"] = "gpt-3.5-turbo"):
        return call_llm(self.task_prompt, model_name=model_name)

    def load_from_weaviate(self):
        pass

    def save_to_weaviate(self):
        # Each object might generate different types of outputs
        # So, we need to save the source in one class
        # And the output in other classes as required
        pass


class RAGRevisionQuiz(RAGTask):
    def __init__(self, source_text: str):
        super().__init__(source_text)
        self.task_prompt = self.get_task_prompt()
        self.uuid = generate_uuid5(self.task_prompt)

    def get_task_prompt(self):
        task_prompt = prompts.quiz_prompt(self.source_text)
        return task_prompt


def call_llm(prompt: str, model_name: Literal["gpt-3.5-turbo", "gpt-4"] = "gpt-3.5-turbo") -> str:
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
    print(task.task_prompt)
    print(task.get_output())


if __name__ == "__main__":
    main()
