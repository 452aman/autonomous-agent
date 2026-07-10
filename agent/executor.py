from llm.groq_client import ask_llm

def execute_tasks(request: str, tasks: list[str]) -> dict[str, str]:
    content = {}
    for task in tasks:
        prompt = f""" You are a professional business document writer.
        The overall user request is: "{request}"
        Your current task is: "{task}"
        Write detailed, professional content for this section only.
        Be specific, use mock data where needed, and write 2-4 paragraphs."""

        content[task] = ask_llm(prompt)
    return content
