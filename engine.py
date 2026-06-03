import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# --- THE UNIVERSAL SOUL ---
UNIVERSAL_SYSTEM_PROMPT = """
You are {persona_name}, a historical figure from the era of {era}.

CORE DIRECTIVES:
1. ADAPT YOUR VOICE: Use the tone described as: {tone_description}. 
   Use these words naturally: {vocabulary}.
2. KNOWLEDGE BOUNDARY: Your awareness ends in the year {cutoff_year}. 
   Do not acknowledge inventions or events after this date.
3. GROUNDING: Use the provided context to answer. If not found, stay in character.

CONTEXT:
{context}

CHAT HISTORY:
{chat_history}

USER QUESTION: {question}
{persona_name}: """


# --- SIMPLE MEMORY (No broken LangChain dependency!) ---
class SimpleWindowMemory:
    """Remembers the last k conversation turns. Pure Python, zero dependencies."""
    def __init__(self, k=5):
        self.k = k
        self.history = []  # List of (user_msg, ai_msg) tuples

    def add(self, user_msg, ai_msg):
        self.history.append((user_msg, ai_msg))
        # Keep only last k turns
        if len(self.history) > self.k:
            self.history = self.history[-self.k:]

    def get_history_string(self, persona_name="AI"):
        result = ""
        for user_msg, ai_msg in self.history:
            result += f"User: {user_msg}\n{persona_name}: {ai_msg}\n"
        return result


class HistoricalEngine:
    def __init__(self, persona_id=None):
        self.llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.persona_id = persona_id
        
        # Initialize Vectorstore only if persona_id is provided
        if persona_id:
            faiss_path = f"./faiss_db/{persona_id}"
            if os.path.exists(faiss_path):
                self.vectorstore = FAISS.load_local(faiss_path, self.embeddings, allow_dangerous_deserialization=True)
            else:
                self.vectorstore = None
        
        # Simple memory - no langchain dependency!
        self.memory = SimpleWindowMemory(k=5)

    def ingest_new_persona(self, persona_id):
        """Turns raw .txt files into a searchable brain."""
        data_path = f"./source_data/{persona_id}"
        files = [f for f in os.listdir(data_path) if f.endswith('.txt')]
        
        all_docs = []
        for file in files:
            loader = TextLoader(os.path.join(data_path, file))
            all_docs.extend(loader.load())
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(all_docs)
        
        self.vectorstore = FAISS.from_documents(
            documents=chunks, 
            embedding=self.embeddings
        )
        # Save the FAISS index to disk
        faiss_path = f"./faiss_db/{persona_id}"
        self.vectorstore.save_local(faiss_path)
        return all_docs[0].page_content[:2000]  # Return sample for profiling

    def auto_profile(self, sample_text):
        """The AI reads the data and decides who it is."""
        extraction_prompt = f"""
        Analyze this text and return ONLY a JSON object:
        TEXT: {sample_text}
        KEYS: name, era, cutoff_year, tone_description, vocabulary (list of 5 words)
        """
        response = self.llm.invoke(extraction_prompt)
        # Clean the response to ensure it's valid JSON
        clean_content = response.content.strip().replace("```json", "").replace("```", "")
        return json.loads(clean_content)

    def ask(self, question, persona_details):
        context = self.get_context(question)
        
        # Get chat history string from our simple memory
        chat_history_str = self.memory.get_history_string(persona_details['name'])

        final_prompt = UNIVERSAL_SYSTEM_PROMPT.format(
            persona_name=persona_details['name'],
            era=persona_details.get('era', 'their time'),
            tone_description=persona_details['tone_description'],
            vocabulary=persona_details.get('vocabulary', ''),
            cutoff_year=persona_details['cutoff_year'],
            context=context,
            chat_history=chat_history_str,
            question=question
        )
        
        response = self.llm.invoke(final_prompt)
        
        # Save to our simple memory
        self.memory.add(question, response.content)
        
        return response.content

    def get_context(self, question):
        try:
            docs = self.vectorstore.similarity_search(question, k=3)
            return "\n".join([d.page_content for d in docs])
        except Exception as e:
            return "No context available yet."