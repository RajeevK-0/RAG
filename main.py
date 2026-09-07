from fastapi import FastAPI , HTTPException , BackgroundTasks
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import uvicorn
import traceback
import os
os.environ["LANGCHAIN_PROJECT"] = "AI_ML_RAG_EVALUATION"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
from langsmith import traceable
from langsmith.run_helpers import get_current_run_tree
from langsmith import Client
from langchain_groq import ChatGroq
import asyncio
from rag_main import RAGPipeline

app = FastAPI(title="AI/ML Research paper RAG api",
              description="Backend for query answer from rag pipline using FAISS(facebook ai similarity search) and Langchain")

from ragModule.config import config
ls_client = Client(api_key=config.langsmith_api_key)
judge_llm = ChatGroq(model='openai/gpt-oss-20b', temperature= 0,api_key=config.llm_api_key,reasoning_format='hidden')

def langsmith_eval(run_id:str , question: str , full_response:str , context:list):
    """Evaluate the live response and logs the feedback to langsmith"""

    try:
        groundedness_prompt = f"""
        Evaluate if the ANSWER is strictly supported by the CONTEXT. 
        CONTEXT: {context}
        ANSWER: {full_response}
        Output ONLY a float between 0.0 (hallucinated) and 1.0 (fully grounded).
        """
        grounded_score = float(judge_llm.invoke(groundedness_prompt).content.strip())
        
        ls_client.create_feedback(
            run_id=run_id,
            key="Groundedness",
            score=grounded_score
        )

        relevance_prompt = f"""
        Evaluate how directly the ANSWER addresses the QUESTION.
        QUESTION: {question}
        ANSWER: {full_response}
        Output ONLY a float between 0.0 (irrelevant) and 1.0 (highly relevant).
        """
        relevance_score = float(judge_llm.invoke(relevance_prompt).content.strip())
        
        ls_client.create_feedback(
            run_id=run_id,
            key="Answer Relevance",
            score=relevance_score
        )
        
        print(f"Live Evals logged for run {run_id}")
        
    except Exception as e:
        print(f"Failed to run background evals: {e}")

rag = RAGPipeline()
class queryRequest(BaseModel):
    user_query :str
    k :int = 5
    history :list = []

@traceable(name="LIVE_RAG_TRACING")
async def answer(request: queryRequest, background_task: BackgroundTasks)->any:
    run_tree = get_current_run_tree()
    current_run_id = run_tree.id if run_tree else None
    
    gen = await rag.generate(user_query=request.user_query, k = request.k , history= request.history)
    full_response = ""
    context = None
    try:
        async for chunk in gen:
            if "documents" in chunk:
                context = chunk["documents"]
            
            elif "answer" in chunk:
                text = chunk["answer"]
                full_response += text
                yield text
    
    finally:
        if current_run_id:
            background_task.add_task(langsmith_eval , 
                                     str(current_run_id) , 
                                     request.user_query,
                                     full_response ,
                                     context)

@app.get("/")
def running():
    return {'status': 'API is running'}

@app.post('/askQuery' )
async def ask_query(request: queryRequest, background_task : BackgroundTasks)->str:
    """you can give query related to ml/ai research paper, user_query should be of type str \n\n k represent the top most k similar chunks of documents we get from our db , k is of type int """
    try :
        response = answer(request,background_task)
        return StreamingResponse(response, media_type="text/event-stream") 
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500 , detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run(app)