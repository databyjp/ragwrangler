# RAGWrangler - A simple RAG (Retrieval-Augumented Generation) Task Manager

RAGWrangler is a Python project designed to streamline the management of RAG tasks using generative language models and the Weaviate database.

With this tool, you can automatically create, retrieve, and store the outputs of RAG tasks in a structured manner in Weaviate, allowing for easy management and tracking of outputs, ultimately saving time and resources.

## Features

- **Automated Task Handling**: Simplify the creation and management of tasks with a straightforward Python class interface.
- **Weaviate Integration**: Seamlessly store and retrieve task outputs using Weaviate database integration.
- **Support for Multiple Language Models**: You can easily swap out language models as desired.
- **Logging**: Utilize integrated logging for effortless debugging and tracking of task statuses.

## Installation

The tool should be compatible with Python 3.8 and higher, although development primarily utilized Python 3.9.

To get started, install the necessary Python packages using the command below:

```sh
pip install openai weaviate-client
```

Next, set your OpenAI API key as an environment variable:

```sh
export OPENAI_APIKEY='your_openai_api_key_here'
```

Finally, clone the repository and navigate to the project directory:

## Quickstart

See `example_usage.py` to see a brief example of how to use the tool.

## Usage

While the project is configured to use a WCS instance by default, you can easily adjust the configuration to your own Weaviate instance in the `db.py` file (see the `initialize()` function for details).

Refer to the [Weaviate documentation](https://weaviate.io/developers/weaviate/installation) for more information on how to set up & connect to a Weaviate instance.

The primary class you will interact with is `RAGTask`.

## RAGTask

The `RAGTask` class represents a general task to be handled by the system. 
Instantiate a `RAGTask` with a task prompt builder function to initiate a task, which can then generate an output based on the source text.

Extend `RAGTask` by defining custom task prompt builder functions that dictate how to generate prompts from the source text, which are then used to derive outputs.

## Working with Tasks

To create a new task, instantiate an object of `RAGTask` (or its extension) with a source text:

```python
from prompts import revision_quiz_json_builder

task = RAGTask(task_prompt_builder=revision_quiz_json_builder)
```

To obtain the task output, utilize the `get_output` method, specifying a model name if desired:

```python
output = task.get_output(source_text="Your source text here", model_name="gpt-3.5-turbo")
```

## License
This project is licensed under the MIT License.

## Copyright
© 2023 JP Hwang
