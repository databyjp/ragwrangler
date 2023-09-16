test_source_text = """

Unfortunately, the BGP protocol in practice can suffer from two significant limitations: misconfigurations and faults. A possible misconfiguration or an error can result in an excessively large number of updates, resulting in route instability, router processor and memory overloading, outages, and router failures. One way that ASes can help reduce the risk that these events will happen is by limiting the routing table size and limiting the number of route changes. 

An AS can limit the routing table size using filtering. For example, long, specific prefixes can be filtered to encourage route aggregation. In addition, routers can limit the number of prefixes advertised from a single source on a per-session basis. Some small ASes also have the option to configure default routes into their forwarding tables. ASes can likewise protect other ASes by using route aggregation and exporting less specific prefixes where possible. 

Also, an AS can limit the number of routing changes, explicitly limiting the propagation of unstable routes by using a mechanism known as flap damping. To apply this technique, an AS will track the number of updates to a specific prefix over a certain amount of time. If the tracked value reaches a configurable value, the AS can suppress that route until a later time. Because this can affect reachability, an AS can be strategic about how it uses this technique for certain prefixes. For example, more specific prefixes could be more aggressively suppressed (lower thresholds), while routes to known destinations that require high availability could be allowed higher thresholds.

"""


system_prompt = {
    "role": "system",
    "content": """
    You are a helpful, intelligent, thoughtful assistant who is a great communicator.
    
    You can communicate complex ideas and concepts in clear, concise language 
    without resorting to domain-specific jargon unless it is entirely necessary.
    
    When you do are not sure of what the answer should be, or whether it is grounded in fact,
    you communicate this to the user to help them make informed decisions
    about how much to trust your outputs. 
    """
}


def quiz_prompt(source_text: str) -> str:
    prompt = """
        Write a set of multiple-choice quiz questions with three to four options each 
        to review and internalise the following information.

        The quiz should be returned in a JSON format so that it can be displayed and undertaken by the user.
        The answer should be a list of integers corresponding to the indices of the correct answers.
        If there is only one correct answer, the answer should be a list of one integer.
        Also return an explanation for each answer, and a quote from the source text to support the answer.

        The goal of the quiz is to provide a revision exercise, 
        so that the user can internalise the information presented in this passage.
        The quiz questions should only cover information explicitly presented in this passage. 
        The number of questions can be anything from one to 10, depending on the volume of information presented.     

        Sample quiz question:

        {
            "question": "What is the capital of France?",
            "options": ["Paris", "London", "Berlin", "Madrid"],
            "answer": [0],
            "explanation": "Paris is the capital of France",
            "source passage": "SOME PASSAGE EXTRACTED FROM THE INPUT TEXT"
        }

        Sample quiz set:

        [
            {
                "question": "What is the capital of France?",
                "options": ["Paris", "London", "Berlin", "Madrid"],
                "answer": [0],
                "explanation": "Paris is the capital of France",
                "source passage": "SOME PASSAGE EXTRACTED FROM THE INPUT TEXT"
            },
            {
                "question": "What is the capital of Spain?",
                "options": ["Paris", "London", "Berlin", "Madrid"],
                "answer": [3],
                "explanation": "Madrid is the capital of Spain",
                "source passage": "SOME PASSAGE EXTRACTED FROM THE INPUT TEXT"
            }
        ]

        ======= Source Text =======

        """ + source_text + """

        ======= Questions =======
    """
    return prompt
