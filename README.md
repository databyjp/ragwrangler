# Weaviate RAG (Retrieval-Augmented Generation) Task Manager

Weaviate RAG Task Manager is a Python project designed to streamline the management of RAG tasks using the Weaviate database. 

With this, you can automatically create, retrieve, and store the outputs of RAG tasks in a structured manner in Weaviate. This will allow you to easily manage and track the outputs of RAG tasks to save money and time.

## Features

- **Automated Task Handling**: Easily create tasks and handle them through a streamlined Python class interface.
- **Weaviate Integration**: Store and retrieve task outputs seamlessly with Weaviate database integration.
- **Support for Multiple GPT Models**: The system supports various GPT models including gpt-3.5-turbo and upcoming versions like gpt-4.
- **Logging**: Integrated logging allows for easy debugging and tracking of task statuses.

## Installation

It should work with Python 3.8 and higher, but the development environment used Python 3.9.

You will also need to install the necessary Python packages using the following command:

```sh
pip install openai weaviate-client
```

Next, set your OpenAI API key as an environment variable:

```sh
export OPENAI_APIKEY='your_openai_api_key_here'
```

Finally, clone the repository and navigate to the project directory:

## Usage
The proejct is set up to use a WCS instance by default, but you can change configuration to your own Weaviate instance in `db` (see `connect_to_db()`).

Refer to the [Weaviate documentation](https://weaviate.io/developers/weaviate/installation) for more information on how to set up & connect to a Weaviate instance.

The main class you'll be interacting with is `RAGTask`.

## RAGTask
This class represents a general task to be handled by the system. You instantiate a `RAGTask` with a source text, and it can generate an output based on a task prompt, which can be generated or set manually.

### Example extension of RAGTask

##### RAGRevisionQuiz
This class extends `RAGTask`, automatically generating a task prompt for a revision quiz based on the source text.

## Working with Tasks
To create a new task, instantiate an object of `RAGTask` (or its extension) with a source text:

```python
task = RAGRevisionQuiz("Your source text here")
```

To get the output for a task, use the `get_output` method, optionally specifying a model name:

```python
output = task.get_output(model_name="gpt-3.5-turbo")
```

## License
This project is licensed under the MIT License.
