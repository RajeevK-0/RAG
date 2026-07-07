from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from rag_main import RAGPipeline
import uvicorn
import traceback
app = FastAPI(title="AI/ML Research paper RAG api",
              description="Backend for query answer from rag pipline using FAISS(facebook ai similarity search) and Langchain")

rag = RAGPipeline()
class queryRequest(BaseModel):
    user_query :str
    k :int = 3
    history :list = []
@app.get("/")
def running():
    return {'status': 'API is running'}

@app.post('/askQuery' )
async def ask_query(request: queryRequest)->str:
    """you can give query related to ml/ai research paper, user_query should be of type str \n\n k represent the top most k similar chunks of documents we get from our db , k is of type int """
    try :
        response = await rag.generate(user_query=request.user_query , k= request.k ,history = request.history)
        return StreamingResponse(response, media_type="text/event-stream") #
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500 , detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run(app)