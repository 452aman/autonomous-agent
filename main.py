import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from models.schemas import AgentRequest, AgentResponse, HistoryEntry
from agent.classifier import classify_document_type
from agent.planner import create_plan
from agent.executor import execute_tasks
from agent.reflection import reflect_and_improve
from document.word_builder import build_word_document

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Autonomous Agent API",
    description="An autonomous AI agent that plans, executes, reflects, and generates professional Word documents from natural language requests.",
    version="1.0.0",
)

history: list[HistoryEntry] = []


@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/history")
def get_history():
    return {"total": len(history), "requests": history}


@app.post("/agent")
async def run_agent(body: AgentRequest):
    request = body.request
    logger.info(f"New request received: {request[:80]}...")

    try:
        logger.info("Step 1/4 — Classifying document type")
        document_type = classify_document_type(request)
        logger.info(f"Document type: {document_type}")

        logger.info("Step 2/4 — Planning tasks")
        tasks = create_plan(request)
        logger.info(f"Generated {len(tasks)} tasks: {tasks}")

        logger.info("Step 3/4 — Executing tasks")
        content = execute_tasks(request, tasks)

        logger.info("Step 4/4 — Running reflection")
        improved_content, reflection_count = reflect_and_improve(request, content)
        logger.info(f"Reflection complete — {reflection_count} sections improved")

        title = f"{document_type} — {request[:60]}"
        file_path = build_word_document(title, improved_content)
        logger.info(f"Document saved: {file_path}")

        entry = HistoryEntry(
            id=len(history) + 1,
            request=request,
            document_type=document_type,
            tasks_completed=tasks,
            reflection_iterations=reflection_count,
            file_path=file_path,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        history.append(entry)

        return FileResponse(
            path=file_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename="agent_output.docx",
            headers={
                "X-Document-Type": document_type,
                "X-Tasks-Completed": str(len(tasks)),
                "X-Reflection-Iterations": str(reflection_count),
            },
        )

    except Exception as e:
        logger.error(f"Agent failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
