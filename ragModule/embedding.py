from typing import List, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
from ragModule.data_loader import load_document

class EmbeddingPipeline:
    def __init__(self,model:str = "all-MiniLM-L6-v2" , chunk_size: int = 1000 ,chunk_overlap: int = 200):
        self.model = SentenceTransformer(model)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        print(f"model loaded: {model}")
    
    def chunk_document(self,documents:List[Any]):
        splitter = RecursiveCharacterTextSplitter(separators=["\n\n","\n"," ",""],chunk_size = self.chunk_size , chunk_overlap = self.chunk_overlap)
        chunk = splitter.split_documents(documents)
        print(f"split {len(documents)} documents into {len(chunk)} chunks")
        return chunk
    
    def embed_chunks(self,chunks:List[Any])->np.ndarray:
        text = [chunk.page_content for chunk in chunks]
        print(f"gen embedding for {len(text) } chunks..")
        embeddings = self.model.encode(text,show_progress_bar = True)
        print(f"shape of embeddings: {embeddings.shape}")
        return embeddings

if __name__ == "__main__":
    docs = load_document("data")
    emb_pipeline= EmbeddingPipeline()
    chunks = emb_pipeline.chunk_document(documents=docs)
    embedding = emb_pipeline.embed_chunks(chunks=chunks)
    print(f"example embedding: {embedding[0] if len(embedding)>0 else None}")