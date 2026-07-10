from llm.groq_client import ask_llm
def create_plan(request:str) -> list[str]:
    prompt = f"""You are a planning agent. A user has made the following request:
    "{request}"
    Your job is to break this into a numbered list of
     specific tasks needed to produce a professional bussiness document.
     Return ONLY the numbered list. No introduction, no explanation, no extra text.
    Example Format:
    1. Define project overview
    2. List scope and features
    3. Create timeline"""

    response = ask_llm(prompt)
    tasks = []
    for line in response.strip().split("\n"):
        line = line.strip()
        if line and line[0].isdigit():
            task = line.split(".", 1)[-1].strip()
            tasks.append(task)
    return tasks

