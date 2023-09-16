import main
import prompts


class RAGRevisionQuiz(main.RAGTask):
    """
    Represents a RAG revision quiz task, extending RAGTask with specific prompt generation and uuid assignment.

    Attributes:
        source_text (str): The source text for the task.
    """
    def __init__(self, source_text: str):
        super().__init__(source_text)

    def get_task_prompt(self):
        """
        Generate the task prompt using predefined quiz prompts.
        :return: The generated task prompt.
        """
        task_prompt = prompts.revision_quiz_json(self.source_text)
        return task_prompt