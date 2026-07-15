from llm.groq_client import ask_llm

DOCUMENT_TYPES = [
    "Project Plan",
    "Business Proposal",
    "Meeting Minutes",
    "Business Report",
    "Technical Design Document",
    "Standard Operating Procedure",
    "Product Specification",
]

def classify_document_type(request: str) -> str:
    types_list = "\n".join(f"- {t}" for t in DOCUMENT_TYPES)
    prompt = f"""You are a document classification expert.

Given the user request below, determine which document type best fits.
Choose ONLY from this list:
{types_list}

User request: "{request}"

Reply with ONLY the document type name. Nothing else."""

    result = ask_llm(prompt).strip()
    for doc_type in DOCUMENT_TYPES:
        if doc_type.lower() in result.lower():
            return doc_type
    return "Business Report"
