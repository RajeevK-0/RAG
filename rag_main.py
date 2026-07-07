from ragModule.search import RAGSearch
from langchain_core.messages import HumanMessage , AIMessage
class RAGPipeline :
    async def generate(self , user_query:str , k:int = 3 , history:list = None):
        if history is None:
            history = []
        langchain_history = []
        for msg in history:
            if msg['role'] == 'user':
                langchain_history.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                langchain_history.append(AIMessage(content=msg['content']))
        rgSearch = RAGSearch()
        stream = rgSearch.search_and_summarize(query=user_query,top_k=k,history = langchain_history)
        async def IntercptNprint():
            async for chunk in stream:
                text = chunk.content if hasattr(chunk , "content") else str(chunk)
                print(text , end = '' , flush= True)
                yield text
        return IntercptNprint()
if __name__ == "__main__":
    import asyncio
    async def run():
        print('testing astream ...')
        rp = RAGPipeline()
        user_query = "what is q,v,r in attention mechanism?"
        resp = await rp.generate(user_query=user_query , k=3 , chat_history=None)
        async for _ in resp:
            pass
    asyncio.run(run())
    # print(f"answer for user query {user_query} : {response["response"]}")