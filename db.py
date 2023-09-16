import weaviate
import os
import logging

logger = logging.getLogger(__name__)

VECTORIZER = "text2vec-openai"
OUTPUT_COLLECTION = "RAGOutput"


def initialize() -> weaviate.Client:
    client = connect_to_wcs()
    configure_database(client)
    return client


def connect_to_wcs() -> weaviate.Client:
    client = weaviate.Client(
        url=os.environ['JP_WCS_URL'],
        auth_client_secret=weaviate.AuthApiKey(os.environ['JP_WCS_ADMIN_KEY']),
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


# client.query.get("RAGOutput", ["prompt", "generated_text"]).do()