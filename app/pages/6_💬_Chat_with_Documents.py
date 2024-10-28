

# pages/6_💬_Chat_with_Documents.py
import streamlit as st

import streamlit as st
from utils.rag_processor import RAGProcessor
import os
from typing import List
import streamlit as st

def apply_custom_css():
    """Apply custom CSS styling to the Streamlit app"""
    st.markdown("""
        <style>
        /* Main container styling */
        .main {
            background-color: var(--background-color);
            color: var(--text-color);
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: rgba(251, 251, 251, 0.05);
            border-right: 1px solid rgba(251, 251, 251, 0.1);
        }
        
        /* Chat message containers */
        .stChatMessage {
            background-color: rgba(251, 251, 251, 0.05);
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            border: 1px solid rgba(251, 251, 251, 0.1);
            transition: all 0.2s ease;
        }
        
        .stChatMessage:hover {
            background-color: rgba(251, 251, 251, 0.08);
        }
        
        /* User message styling */
        .stChatMessage [data-testid="StyChatMessageUser"] {
            background-color: rgba(28, 131, 225, 0.1);
            border: 1px solid rgba(28, 131, 225, 0.2);
        }
        
        /* Assistant message styling */
        .stChatMessage [data-testid="StyChatMessageAssistant"] {
            background-color: rgba(87, 96, 106, 0.1);
            border: 1px solid rgba(87, 96, 106, 0.2);
        }
        
        /* Document management section */
        .document-section {
            background-color: rgba(251, 251, 251, 0.03);
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid rgba(251, 251, 251, 0.1);
        }
        
        /* File upload area */
        .uploadedFile {
            background-color: rgba(251, 251, 251, 0.05);
            border-radius: 8px;
            padding: 0.75rem;
            margin: 0.5rem 0;
            border: 1px solid rgba(251, 251, 251, 0.1);
        }
        
        /* Source document expander */
        .streamlit-expanderHeader {
            background-color: rgba(251, 251, 251, 0.05);
            border-radius: 8px;
            border: 1px solid rgba(251, 251, 251, 0.1);
        }
        
        /* Code blocks in source documents */
        .streamlit-expanderContent pre {
            background-color: rgba(251, 251, 251, 0.03);
            border-radius: 6px;
            padding: 0.75rem;
            border: 1px solid rgba(251, 251, 251, 0.1);
        }
        
        /* Buttons */
        .stButton button {
            background-color: rgba(28, 131, 225, 0.1);
            color: rgb(28, 131, 225);
            border: 1px solid rgba(28, 131, 225, 0.2);
            border-radius: 6px;
            transition: all 0.2s ease;
        }
        
        .stButton button:hover {
            background-color: rgba(28, 131, 225, 0.2);
            border-color: rgba(28, 131, 225, 0.3);
        }
        
        /* Input fields */
        .stTextInput input {
            background-color: rgba(251, 251, 251, 0.05);
            border: 1px solid rgba(251, 251, 251, 0.1);
            border-radius: 6px;
            color: var(--text-color);
        }
        
        .stTextInput input:focus {
            border-color: rgb(28, 131, 225);
            box-shadow: 0 0 0 1px rgb(28, 131, 225);
        }
        
        /* Headers */
        h1, h2, h3 {
            color: rgb(255, 255, 255);
            font-weight: 600;
        }
        
        /* Alerts and notifications */
        .stAlert {
            background-color: rgba(251, 251, 251, 0.05);
            border: 1px solid rgba(251, 251, 251, 0.1);
            border-radius: 8px;
        }
        
        /* Success message */
        .success {
            background-color: rgba(45, 201, 55, 0.1);
            border-color: rgba(45, 201, 55, 0.2);
        }
        
        /* Error message */
        .error {
            background-color: rgba(255, 76, 76, 0.1);
            border-color: rgba(255, 76, 76, 0.2);
        }
        
        /* Spinner */
        .stSpinner {
            border-color: rgb(28, 131, 225);
        }
        </style>
    """, unsafe_allow_html=True)


    
    # Rest of your existing main() function code...
def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "rag_processor" not in st.session_state:
        st.session_state.rag_processor = None
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []
    if "current_doc" not in st.session_state:
        st.session_state.current_doc = None

def display_chat_messages():
    """Display chat messages with enhanced styling"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant" and "is_summary" in message:
                # Display document summary in a special way
                st.markdown(f"📄 **Document Analysis**")
                st.markdown(message["content"])
            else:
                st.markdown(message["content"])
            
            # Display sources if available
            if "source_docs" in message:
                with st.expander("📚 View Sources", expanded=False):
                    for idx, doc in enumerate(message["source_docs"], 1):
                        st.markdown(f"**Source {idx}:**")
                        st.markdown(f"```\n{doc.page_content}\n```")

def process_document(file, rag_processor: RAGProcessor):
    """Process a single document using RAG processor"""
    try:
        with st.spinner(f"📄 Processing {file.name}..."):
            if file.type == "application/pdf":
                pdf_bytes = file.read()
                rag_processor.process_pdf(pdf_bytes)
                
                # Add document summary to chat
                if rag_processor.document_summary:
                    summary_message = {
                        "role": "assistant",
                        "content": rag_processor.document_summary,
                        "is_summary": True
                    }
                    st.session_state.messages.append(summary_message)
                return True
            else:
                st.warning(f"⚠️ Unsupported file type: {file.type}")
                return False
    except Exception as e:
        st.error(f"❌ Error processing {file.name}: {str(e)}")
        return False

def create_sidebar():
    """Create sidebar with settings and info"""
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        api_key = st.text_input("Enter Google API Key:", type="password", key="api_key")
        
        if api_key:
            if st.session_state.rag_processor is None:
                st.session_state.rag_processor = RAGProcessor(google_api_key=api_key)
                st.success("✅ System initialized!")
        
        st.markdown("---")
        
        with st.expander("📖 How to Use"):
            st.markdown("""
            1. Enter your API key
            2. Upload PDF document(s)
            3. Process the documents
            4. Start chatting!
            
            **Tips:**
            - Upload related documents together
            - Use clear, readable PDFs
            - Ask specific questions
            - Reference document sections
            """)
            
        with st.expander("🎯 Features"):
            st.markdown("""
            - Multi-document support
            - Smart context understanding
            - Source citations
            - Document summaries
            - Natural conversation
            """)
            
        st.markdown("---")
        
        # Clear chat button
        if st.button("🧹 Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

def main():
    st.set_page_config(
        page_title="Chat with Documents",
        page_icon="💬",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    
    # Apply custom styling
    apply_custom_css()    

    # Initialize session state
    initialize_session_state()
    
    # Create sidebar
    create_sidebar()

    # Main content area
    st.title("💬 Chat with Documents")
    st.markdown("Engage with your documents through AI-powered conversation")

    # Create two columns for document management and chat
    doc_col, chat_col = st.columns([1, 2])

    with doc_col:
        st.markdown("### 📚 Document Management")
        
        # File uploader with drag-and-drop
        uploaded_files = st.file_uploader(
            "Drop your PDFs here",
            type=['pdf'],
            accept_multiple_files=True,
            help="Drag and drop your PDF files here"
        )

        if uploaded_files:
            st.markdown("#### 📑 Uploaded Documents")
            for file in uploaded_files:
                file_col, btn_col = st.columns([2, 1])
                with file_col:
                    st.markdown(f"**{file.name}**")
                    st.caption(f"Size: {file.size / 1024:.1f} KB")
                
                with btn_col:
                    if st.button("Process 🔄", key=f"process_{file.name}"):
                        if not st.session_state.rag_processor:
                            st.error("⚠️ Please enter API key first!")
                        else:
                            success = process_document(file, st.session_state.rag_processor)
                            if success:
                                st.success(f"✅ Processed {file.name}")
                st.markdown("---")

    with chat_col:
        st.markdown("### 💭 Chat Interface")
        
        # Chat container with custom styling
        chat_container = st.container()
        
        with chat_container:
            # Display chat messages
            display_chat_messages()
            
            # Chat input
            if prompt := st.chat_input("Ask about your documents..."):
                if not st.session_state.rag_processor:
                    st.error("⚠️ Please enter API key and process documents first!")
                else:
                    # Add user message
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    
                    # Get AI response
                    try:
                        with st.spinner("🤔 Thinking..."):
                            response = st.session_state.rag_processor.get_answer(prompt)
                            
                            # Add assistant response
                            assistant_message = {
                                "role": "assistant",
                                "content": response["answer"],
                                "source_docs": response["source_documents"]
                            }
                            st.session_state.messages.append(assistant_message)
                            
                            # Rerun to update chat display
                            st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

        # Add some spacing at the bottom
        st.markdown("<br>" * 2, unsafe_allow_html=True)

if __name__ == "__main__":
    main()