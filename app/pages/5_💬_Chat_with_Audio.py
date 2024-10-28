# pages/5_💬_Chat_with_Audio.py
# pages/5_💬_Chat_with_Audio.py
import streamlit as st
from utils.audio_processor import AudioTranscriber 
from utils.audio_pdf_generator import AudioToPDFConverter
from utils.rag_processor import RAGProcessor
import tempfile



# Configure page with custom theme and styling
st.set_page_config(
    page_title="Chat with Audio",
    page_icon="💬",
    layout="wide"
)

# Custom CSS for dark theme
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 2rem;
    }
    
    /* Header styling */
    .stTitle {
        color: #7EB6FF !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 2rem !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1E1E1E;
        padding: 2rem 1rem;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #4B4DFF;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #6E6FFF;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        transform: translateY(-1px);
    }
    
    /* File uploader styling */
    .uploadedFile {
        background-color: #2D2D2D;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #3D3D3D;
    }
    
    /* Chat message styling */
    .stChatMessage {
        background-color: #2D2D2D;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Success message styling */
    .success {
        background-color: #1E3A2F;
        color: #4CAF50;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #2E7D32;
    }
    
    /* Warning message styling */
    .warning {
        background-color: #3D2E1E;
        color: #FFA726;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #FF9800;
    }
    
    /* Input field styling */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 2px solid #3D3D3D;
        padding: 0.5rem;
        background-color: #2D2D2D;
        color: #FFFFFF;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #4B4DFF;
        box-shadow: 0 0 0 2px rgba(75,77,255,0.2);
    }

    /* Feature card styling */
    .feature-card {
        background-color: #2D2D2D;
        border: 1px solid #3D3D3D;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    /* Section header styling */
    .section-header {
        color: #7EB6FF;
        margin-bottom: 1rem;
        font-size: 1.2rem;
    }

    /* List item styling */
    .feature-list-item {
        color: #E0E0E0;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("💬 Chat with Audio")
    st.markdown("""
        <div style='background-color: #2D2D2D; padding: 1rem; border-radius: 8px; margin-bottom: 2rem; border: 1px solid #3D3D3D; color: #E0E0E0;'>
            Upload an audio file and chat with its content using AI. Our advanced system will help you analyze and interact with your audio content seamlessly.
        </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'Audio_chat_history' not in st.session_state:
        st.session_state.Audio_chat_history = []  #Audio_chat_history
    if 'Audio_rag_system' not in st.session_state:
        st.session_state.Audio_rag_system = None   #Audio_rag_system
    if 'processed_pdf' not in st.session_state:
        st.session_state.processed_pdf = None
    if 'audio_processed' not in st.session_state:
        st.session_state.audio_processed = False

    # Enhanced sidebar with dark theme
    with st.sidebar:
        st.markdown("""
            <div class='feature-card'>
                <h3 class='section-header'>🎯 Features</h3>
                <ul style='list-style-type: none; padding-left: 0;'>
                    <li class='feature-list-item'>✨ Natural conversation</li>
                    <li class='feature-list-item'>🧠 Context awareness</li>
                    <li class='feature-list-item'>📚 Multiple topics</li>
                    <li class='feature-list-item'>⏱️ Timestamp references upcomming</li>
                </ul>
            </div>
            
            <div class='feature-card'>
                <h3 class='section-header'>📝 Supported Formats</h3>
                <ul style='list-style-type: none; padding-left: 0;'>
                    <li class='feature-list-item'>🎵 WAV, MP3, M4A, FLAC</li>
                    <li class='feature-list-item'>⏰ Max duration: 1 hour</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<h3 class='section-header'>🔑 API Configuration</h3>", unsafe_allow_html=True)
        api_key = st.text_input("Enter Google API Key:", type="password")

    if api_key:
        if st.session_state.Audio_rag_system is None:  #Audio_rag_system
            st.session_state.Audio_rag_system = RAGProcessor(google_api_key=api_key) #Audio_rag_system
                # Clear history button
        if st.sidebar.button("Clear History"):
            st.session_state.Audio_chat_history = []  #Video_chat_history
            st.session_state.audio_processed = False
            st.success("Chat history cleared and ready for new input.")

        uploaded_file = st.file_uploader("Upload your audio file", type=['wav', 'mp3', 'm4a', 'flac'])

        if uploaded_file:
            st.markdown("<div class='uploadedFile'>", unsafe_allow_html=True)
            st.audio(uploaded_file)
            st.markdown("</div>", unsafe_allow_html=True)

            if not st.session_state.audio_processed:
                if st.button("🎯 Transcribe & Process", key="process_btn"):
                    with st.spinner("🔄 Processing your audio..."):
                        try:
                            transcriber = AudioTranscriber()
                            transcriber.load_model()

                            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                                tmp_file.write(uploaded_file.getvalue())
                                transcription = transcriber.transcribe_audio(tmp_file.name)

                            st.success("✅ Transcription completed!")

                            pdf_content = AudioToPDFConverter.generate_pdf(transcription)
                            st.session_state.processed_pdf = pdf_content

                            st.session_state.Audio_rag_system.process_pdf(pdf_content, content_type="audio") #Audio_rag_system
                            st.session_state.audio_processed = True
                            st.success("🎉 Audio content processed and ready for questions!")

                        except Exception as e:
                            st.error(f"❌ An error occurred: {str(e)}")
                            st.session_state.audio_processed = False
                            return

            if st.session_state.audio_processed:
                st.markdown("""
                    <h2 style='color: #7EB6FF; margin-top: 2rem; margin-bottom: 1rem;'>
                        💭 Chat with Audio Content
                    </h2>
                """, unsafe_allow_html=True)
                
                # Enhanced chat history display
                for message in st.session_state.Audio_chat_history: # Audio_chat_history
                    with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
                        st.markdown(message["content"])

                # Enhanced chat input
                if question := st.chat_input("💭 Ask a question about the audio..."):
                    with st.chat_message("user", avatar="🧑‍💻"):
                        st.markdown(question)
                    st.session_state.Audio_chat_history.append({"role": "user", "content": question}) #Audio_chat_history

                    with st.chat_message("assistant", avatar="🤖"):
                        with st.spinner("🤔 Thinking..."):
                            response = st.session_state.Audio_rag_system.get_answer(question, content_type="audio") #Audio_rag_system
                            answer = response["answer"]
                            st.markdown(answer)
                    st.session_state.Audio_chat_history.append({"role": "assistant", "content": answer}) #Audio_chat_history

                if st.button("🔄 Process Audio Again", key="reset_btn"):
                    st.session_state.audio_processed = False
                    st.experimental_rerun()
    else:
        st.warning("🔑 Please enter your Google API key in the sidebar to start.")

if __name__ == "__main__":
    main()