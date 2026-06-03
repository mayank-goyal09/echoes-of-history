"""
Migration script: Rebuild all persona vector stores using FAISS.
Run this once locally to generate the faiss_db/ indexes that get committed to the repo.
"""
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def migrate_all():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    source_dir = "./source_data"
    
    personas = [f for f in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, f))]
    
    for persona_id in personas:
        print(f"\n{'='*50}")
        print(f"Processing: {persona_id}")
        
        data_path = os.path.join(source_dir, persona_id)
        files = [f for f in os.listdir(data_path) if f.endswith('.txt')]
        
        if not files:
            print(f"  No .txt files found, skipping.")
            continue
        
        all_docs = []
        for file in files:
            loader = TextLoader(os.path.join(data_path, file))
            all_docs.extend(loader.load())
            print(f"  Loaded: {file} ({len(all_docs)} docs so far)")
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(all_docs)
        print(f"  Split into {len(chunks)} chunks")
        
        vectorstore = FAISS.from_documents(documents=chunks, embedding=embeddings)
        
        faiss_path = f"./faiss_db/{persona_id}"
        vectorstore.save_local(faiss_path)
        print(f"  Saved FAISS index to: {faiss_path}")
    
    print(f"\n{'='*50}")
    print("Migration complete! All FAISS indexes created.")
    print("You can now commit faiss_db/ to your repository.")

if __name__ == "__main__":
    migrate_all()
