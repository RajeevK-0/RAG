import os
from ragModule.vector_store import FaissVectorStore
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from ragModule.config import config
class RAGSearch:

    def __init__(self, persist_dir: str = "faiss_store", embedding_model: str = "all-MiniLM-L6-v2", llm_model: str = "llama-3.1-8b-instruct"):
        self.vectorstore = FaissVectorStore(persist_dir, embedding_model)
        # Load or build vectorstore
        faiss_path = os.path.join(persist_dir, "faiss.index")
        meta_path = os.path.join(persist_dir, "metadata.pkl")
        if not (os.path.exists(faiss_path) and os.path.exists(meta_path)):
            from data_loader import load_all_documents
            docs = load_all_documents("data")
            self.vectorstore.build_from_documents(docs)
        else:
            self.vectorstore.load()
            
        self.llm = ChatGroq(groq_api_key=config.llm_api_key, model_name=llm_model)
        print(f"[INFO] Groq LLM initialized: {llm_model}")

    def get_context(self,query:str , top_k:int = 10):
        results = self.vectorstore.query(query, top_k=top_k)
        texts = [r["metadata"].get("text", "") for r in results if r["metadata"]]
        context = "\n\n".join(texts)
        return context
    
    def search_and_summarize(self, query: str, top_k: int = 10 ,history:list = None) -> str:
        context = self.get_context(query=query , top_k=top_k)
        if not context:
            return "No relevant documents found."
        prompt = ChatPromptTemplate.from_messages([('system',"you are an helpful ai research assistant.  Keep answer brief and concise, answer based on the following context: {context}"),
                                                   MessagesPlaceholder(variable_name='history'),
                                                   ("human","{query}")])
        chain = prompt | self.llm
        return chain.astream({
            "context" : context,
            "history" : history,
            "query" : query
        })
        # return {"response" : response.content}

if __name__ == "__main__":
    rag_search = RAGSearch()
    query = "What is attention mechanism?"
    summary = rag_search.search_and_summarize(query, top_k=3)
    print("Summary:", summary['response'])