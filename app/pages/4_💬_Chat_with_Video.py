# pages/4_💬_Chat_with_Video.py
import streamlit as st
from utils.video_to_pdf import VideoToPDFConverter
from utils.rag_processor import RAGProcessor
import os




import tempfile



def apply_custom_styles():
    st.markdown("""
        <style>
            .stApp {
                max-width: 1700px;
                margin: 0 auto;
                background-color: #181818; /* Dark background */
                color: #ffffff; /* Text color for better contrast */
                font-family: Arial, sans-serif;
            }
            .feature-card {
                padding: 1.5rem;
                border-radius: 0.5rem;
                background-color: rgba(34, 34, 34, 0.8); /* Semi-transparent dark background */
                margin: 1rem 0;
                transition: transform 0.3s ease;
            }
            .feature-card:hover {
                transform: translateY(-5px);
            }
            .main-title {
                font-size: 3rem;
                font-weight: bold;
                margin-bottom: 2rem;
                color: #f1f1f1;
            }
            .subtitle {
                font-size: 1.5rem;
                color: #d3d3d3;
                margin-bottom: 3rem;
            }
            .sidebar .sidebar-content {
                background-color: #222;
                color: #d3d3d3;
            }
            .sidebar .sidebar-content h2 {
                color: #f1f1f1;
            }
            .sidebar button {
                background-color: #444;
                color: #fff;
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 0.25rem;
                margin: 0.5rem 0;
            }
            .st-chat {
                background-color: #333;
                color: #fff;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Chat with Video",
        page_icon="",
        layout="wide"
    )
    apply_custom_styles()
    
    st.title(" Chat with Video")
    st.markdown("Upload a video and chat with its content using AI-powered conversation.")
    
    # Initialize session state
    if 'Video_chat_history' not in st.session_state:
        st.session_state.Video_chat_history = []   #Video_chat_history
    if 'Video_rag_system' not in st.session_state:
        st.session_state.Video_rag_system = None         #Video_rag_system
    if 'processed_pdf' not in st.session_state:
        st.session_state.processed_pdf = None
    if 'video_processed' not in st.session_state:
        st.session_state.video_processed = False

    # API key input
    api_key = st.sidebar.text_input("Enter Google API Key:", type="password")
    if api_key:
        if st.session_state.Video_rag_system is None: #Video_rag_system
            st.session_state.Video_rag_system = RAGProcessor(google_api_key=api_key) # Video_rag_system

        # Clear history button
        if st.sidebar.button("Clear History"):
            st.session_state.Video_chat_history = []  #Video_chat_history
            st.session_state.video_processed = False
            st.success("Chat history cleared and ready for new input.")

        # File uploader for videos
        uploaded_file = st.file_uploader("Upload your video file", type=['mp4', 'avi', 'mov', 'mkv'])
        if uploaded_file:
            # Display video preview
            st.video(uploaded_file)

            # Process video only if not already processed
            if not st.session_state.video_processed:
                try:
                    with st.spinner("Processing video and generating PDF..."):
                        # Initialize converter
                        converter = VideoToPDFConverter()
                        # Convert video to PDF
                        pdf_content = converter.convert_video_to_pdf(uploaded_file)
                        st.session_state.processed_pdf = pdf_content
                        
                        # Process PDF with RAG system
                        st.session_state.Video_rag_system.process_pdf(pdf_content) #Video_rag_system
                        st.session_state.video_processed = True
                        st.success("Video content processed and ready for questions!")
                except Exception as e:
                    st.error(f"An error occurred during video processing: {str(e)}")
                    st.session_state.video_processed = False
                    return

            # Only show chat interface if video is processed
            if st.session_state.video_processed:
                st.subheader("Chat with Video Content")
                
                # Display chat history
                for message in st.session_state.Video_chat_history:   #Video_chat_history

                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
                
                # Chat input
                if question := st.chat_input("Ask a question about the video:"):
                    # Display user question
                    with st.chat_message("user"):
                        st.markdown(question)
                    st.session_state.Video_chat_history.append({"role": "user", "content": question})   #Video_chat_history


                    # Get and display AI response
                    with st.chat_message("assistant"):
                        with st.spinner("Thinking..."):
                            response = st.session_state.Video_rag_system.get_answer(question,content_type="video") #Video_rag_system
                            answer = response["answer"]
                            st.markdown(answer)
                    st.session_state.Video_chat_history.append({"role": "assistant", "content": answer})    #Video_chat_history


                # Add a button to reset processing if needed
                if st.button("Process Video Again"):
                    st.session_state.video_processed = False
                    st.experimental_rerun()
    else:
        st.warning("Please enter your Google API key in the sidebar to start.")

if __name__ == "__main__":
    main()
