import json
from llm.groq_client import ask_llm

def reflect_and_improve(request: str, content: dict[str, str], max_iterations: int = 2) -> tuple[dict[str, str], int]:
    improved = content.copy()
    reflection_count = 0

    for iteration in range(max_iterations):
        sections_text = "\n\n".join(
            f"Section: {k}\nContent: {v}" for k, v in improved.items()
        )

        score_prompt = f"""You are a quality reviewer for business documents.

Review each section below and return a JSON object where keys are section names and values are scores from 1-10.
Score based on: completeness, professionalism, and relevance to the request: "{request}"
Return ONLY valid JSON. No explanation.

{sections_text}"""

        scores_raw = ask_llm(score_prompt)

        try:
            scores = json.loads(scores_raw)
        except json.JSONDecodeError:
            break

        weak_sections = {
            k: v for k, v in scores.items()
            if k in improved and isinstance(v, (int, float)) and v < 7
        }

        if not weak_sections:
            break

        for section, score in weak_sections.items():
            retry_prompt = f"""You are a professional business document writer.

The overall request is: "{request}"
Rewrite the following section to be more complete, detailed and professional.
Section: "{section}"
Previous content was rated {score}/10. Aim for 9/10.
Write 3-5 paragraphs."""

            improved[section] = ask_llm(retry_prompt)
            reflection_count += 1

    return improved, reflection_count
