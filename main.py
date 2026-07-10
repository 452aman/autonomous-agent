from fastapi import FastAPI                                     
from fastapi.responses import FileResponse                                                                            
from models.schemas import AgentRequest                         
from agent.planner import create_plan
from agent.executor import execute_tasks                                                                              
from agent.reflection import reflect_and_improve
from document.word_builder import build_word_document                                                                 
                                                                                                                    
app = FastAPI(title="Autonomous Agent API")
                                                                                                                    
@app.post("/agent")                                             
def run_agent(body: AgentRequest):
    request = body.request                  
                                        
    tasks = create_plan(request)
    content = execute_tasks(request, tasks)                                                                           
    improved_content, reflection_count = reflect_and_improve(request, content)
                                                                                                                    
    title = f"Business Document — {request[:60]}"               
    file_path = build_word_document(title, improved_content)                                                          
                                                                                                                    
    return FileResponse(                                                                                              
        path=file_path,                                                                                               
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",                         
        filename="agent_output.docx",       
        headers={                                                                                                     
            "X-Tasks-Completed": str(len(tasks)),               
            "X-Reflection-Iterations": str(reflection_count),                                                         
        }                               
    )                                                                                                                 
                                            