# Directory structure:
# app/
# ├── Home.py
# ├── utils/
# │   ├── __init__.py
# │   ├── audio_pdf_genrator.py
# │   └── audio_processor.py
# │   └── text_processor.py
# │   └── rag_processor.py
# │   ├── video_processor.py
# │   ├── video_to_pdf.py
# ├── pages/
# │   ├── 1_🎥_Video_to_Audio.py
# │   ├── 2_🎥_Video_to_Text.py
# │   ├── 3_🎧_Audio_to_Text.py
# │   ├── 4_💬_Chat_with_Video.py
# │   ├── 5_💬_Chat_with_Audio.py
# │   └── 6_💬_Chat_with_Documents.py
# └── assets/
#     └── style.css
# utils/rag_processor.py

import os
from typing import List, Dict, Optional
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import tempfile

class RAGProcessor:
    def __init__(self, google_api_key: str):
        """Initialize the RAG system with necessary components."""
        self.google_api_key = google_api_key
        os.environ["GOOGLE_API_KEY"] = google_api_key
        
        self.embedding_model = HuggingFaceBgeEmbeddings(
            model_name="BAAI/bge-m3"
        )
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        
        self.conversation_memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key='answer'
        )
        
        self.vectorstore = None
        self.qa_chain = None
        self.document_summary = None

    def generate_summary(self, text: str, content_type: str = "document") -> str:
        """Generate a summary of the given text using Gemini model."""
        prompt = f"""Please provide a comprehensive summary of the following {content_type} content. 
        Focus on key topics, main arguments, and important details that would be 
        relevant for answering questions about this {content_type}: 

        Text: {{text}}
        """
        
        response = self.llm.predict(prompt.format(text=text))
        return response

    def process_pdf(self, pdf_content: bytes, content_type: str = "document") -> None:
        """Process PDF content with intelligent chunking."""
        try:
            # Save PDF content to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(pdf_content)
                tmp_path = tmp_file.name

            # Load PDF
            loader = PyPDFLoader(tmp_path)
            pages = loader.load()
            
            # Generate overall document summary
            full_text = " ".join([page.page_content for page in pages])
            self.document_summary = self.generate_summary(full_text, content_type)
            
            if len(pages) <= 1:
                documents = pages
            else:
                # Apply intelligent chunking for multi-page PDFs
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len,
                )
                
                # Split text and add summary to each chunk
                chunks = text_splitter.split_text(full_text)
                documents = []
                for chunk in chunks:
                    enhanced_chunk = f"{content_type.title()} Content Summary: {self.document_summary}\n\nContent Segment: {chunk}"
                    documents.append(Document(page_content=enhanced_chunk))
            
            # Create vector store
            self.vectorstore = FAISS.from_documents(
                documents,
                self.embedding_model
            )
            
            # Initialize QA chain
            self.qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.vectorstore.as_retriever(
                    search_kwargs={"k": 3}
                ),
                memory=self.conversation_memory,
                return_source_documents=True
            )
            
            # Clean up temporary file
            os.unlink(tmp_path)
            
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")

    def preprocess_question(self, question: str, content_type: str = "document") -> str:
        """Enhance the question using content context and chat history."""
        if not self.document_summary:
            raise Exception(f"No {content_type} content has been processed yet.")
        
        chat_history = self.conversation_memory.load_memory_variables({})
        chat_context = chat_history.get("chat_history", "")
        
        enhancement_prompt = f"""Given a {content_type} and a user's question, help enhance 
        and rephrase the question to be more specific and aligned with the {content_type}'s content.
        
        {content_type.title()} Content Summary:
        {self.document_summary}
        
        Previous Conversation Context:
        {chat_context}
        
        Original Question:
        {question}
        
        Please rephrase the question to:
        1. Include relevant context from the {content_type}
        2. Be more specific based on the {content_type}'s content
        3. Consider any relevant information from previous conversation
        4. Focus on information that's actually present in the {content_type}
        
        Enhanced Question:"""
        
        try:
            enhanced_question = self.llm.predict(enhancement_prompt)
            return enhanced_question.strip()
        except Exception as e:
            print(f"Warning: Question enhancement failed - {str(e)}")
            return question

    def get_answer(self, question: str, content_type: str = "document") -> Dict:
        """Get answer for a question using the RAG system."""
        if not self.qa_chain:
            raise Exception(f"Please process a {content_type} first before asking questions.")
        
        try:
            enhanced_question = self.preprocess_question(question, content_type)
            response = self.qa_chain({"question": enhanced_question})
            
            return {
                "original_question": question,
                "enhanced_question": enhanced_question,
                "answer": response["answer"],
                "source_documents": response["source_documents"]
            }
            
        except Exception as e:
            raise Exception(f"Error getting answer: {str(e)}")