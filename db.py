from typing import Union

import weaviate
import os
import logging

logger = logging.getLogger(__name__)

VECTORIZER = "text2vec-openai"
OUTPUT_COLLECTION = "RAGOutput"


def initialize() -> weaviate.Client:
    client = connect_to_db()
    configure_database(client)
    return client


def connect_to_db() -> weaviate.Client:
    client = weaviate.Client(
        url=os.environ['WCS_URL'],
        auth_client_secret=weaviate.AuthApiKey(os.environ['WCS_ADMIN_KEY']),
    )
    return client


def configure_database(client: weaviate.Client) -> None:
    collection_definition = {
        "class": OUTPUT_COLLECTION,
        "description": "RAG output",
        "properties": [
            {
                "name": "prompt",
                "description": "Prompt used to generate the output",
                "dataType": ["text"],
            },
            {
                "name": "generated_text",
                "description": "Generated text",
                "dataType": ["text"],
                "moduleConfig": {
                    VECTORIZER: {
                        "skip": True
                    }
                }
            },
        ]
    }

    if not client.schema.exists(OUTPUT_COLLECTION):
        client.schema.create_class(collection_definition)
    return None


def add_object(client: weaviate.Client, data_object: dict, uuid=None) -> str:
    uuid_out = client.data_object.create(
        data_object=data_object,
        class_name=OUTPUT_COLLECTION,
        uuid=uuid
    )
    return uuid_out


def load_generated_text(client: weaviate.Client, uuid: str) -> Union[str, None]:
    """
    Load the generated output from Weaviate using the task's uuid.
    :param client: The Weaviate client.
    :param uuid: The unique identifier for the object being retrieved.
    :return: The generated text retrieved from Weaviate.
    """
    weaviate_response = client.data_object.get(uuid=uuid, class_name=OUTPUT_COLLECTION)
    if weaviate_response is None:
        return None
    else:
        return weaviate_response["properties"]["generated_text"]


def save_generated_text(client: weaviate.Client, prompt: str, generated_text: str, uuid: str) -> str:
    """
    Save the generated output to Weaviate.
    :param client: The Weaviate client.
    :param prompt: The prompt used to generate the text.
    :param generated_text: The text to be saved.
    :param uuid: The unique identifier for the object being saved.
    :return: The unique identifier of the saved object.
    """
    data_object = {
        "prompt": prompt,
        "generated_text": generated_text
    }
    uuid_out = add_object(client, data_object, uuid)
    assert uuid_out == uuid, f"UUIDs do not match: {uuid_out} != {uuid}"
    return uuid_out
