
# pages/3_🎧_Audio_to_Text.py
import streamlit as st
from utils.audio_processor import AudioTranscriber
import tempfile

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfWriter, PdfReader

st.set_page_config(
    page_title="Audio to Text Conversion",
    page_icon="🎧",
    layout="wide"
)



# Apply custom styling
def apply_custom_css():
    st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 2rem;
    }
    
    /* Header styling */
    .stTitle {
        color: #E0E0E0 !important;
        font-weight: 600 !important;
        margin-bottom: 2rem !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: rgba(51, 51, 51, 0.6);
        padding: 2rem 1rem;
        border-radius: 10px;
    }
    
    .sidebar .sidebar-content {
        background-color: rgba(51, 51, 51, 0.6);
    }
    
    /* Sidebar headers */
    .sidebar h3 {
        color: #00ADB5 !important;
        font-size: 1.2rem !important;
        margin-top: 2rem !important;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #00ADB5;
    }
    
    /* File uploader styling */
    .uploadedFile {
        background-color: rgba(0, 173, 181, 0.1) !important;
        border: 1px solid #00ADB5 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #00ADB5 !important;
        color: white !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        background-color: #008B8B !important;
        box-shadow: 0 4px 12px rgba(0, 173, 181, 0.2) !important;
    }
    
    /* Select box styling */
    .stSelectbox {
        background-color: rgba(51, 51, 51, 0.6) !important;
        border-radius: 8px !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #CCC !important;
        background-color: transparent !important;
        border-radius: 4px 4px 0 0 !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #00ADB5 !important;
        border-bottom: 2px solid #00ADB5 !important;
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background-color: rgba(0, 173, 181, 0.1) !important;
        color: #E0E0E0 !important;
        border: 1px solid #00ADB5 !important;
        padding: 1rem !important;
        border-radius: 8px !important;
    }
    
    .stError {
        background-color: rgba(255, 76, 76, 0.1) !important;
        border: 1px solid #FF4C4C !important;
        color: #FF4C4C !important;
    }
    
    /* Download button styling */
    .stDownloadButton>button {
        background-color: #2C3333 !important;
        color: #00ADB5 !important;
        border: 1px solid #00ADB5 !important;
        padding: 0.5rem 2rem !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton>button:hover {
        background-color: #00ADB5 !important;
        color: white !important;
    }
    
    /* Audio player styling */
    audio {
        width: 100% !important;
        border-radius: 8px !important;
        background-color: rgba(51, 51, 51, 0.6) !important;
        margin: 1rem 0 !important;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-color: #00ADB5 !important;
    }
    </style>
""", unsafe_allow_html=True)

def generate_pdf(text: str) -> bytes:
        
        """Generate PDF from transcription text"""
        # Create PDF using reportlab
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Split text into lines and write to PDF
        y = height - 50
        words = text.split()
        current_line = []
        
        for word in words:
            current_line.append(word)
            # Check if current line would be too long
            if c.stringWidth(' '.join(current_line), 'Helvetica', 12) > width - 100:
                # Remove last word and write line
                current_line.pop()
                line_text = ' '.join(current_line)
                if y < 50:
                    c.showPage()
                    y = height - 50
                c.drawString(50, y, line_text)
                y -= 15
                # Start new line with the last word
                current_line = [word]
        
        # Write last line
        if current_line:
            line_text = ' '.join(current_line)
            if y < 50:
                c.showPage()
                y = height - 50
            c.drawString(50, y, line_text)
        
        c.save()
        buffer.seek(0)
        
        # Create final PDF
        output_buffer = BytesIO()
        pdf_writer = PdfWriter()
        pdf_reader = PdfReader(buffer)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
        
        pdf_writer.write(output_buffer)
        output_buffer.seek(0)
        
        return output_buffer.getvalue()

def main():
        # Apply custom styling
    apply_custom_css()
    st.title("🎧 Audio to Text Conversion")
    st.markdown("Convert audio files into accurate text transcriptions with AI-powered processing.")

    # Sidebar settings
    st.sidebar.markdown("""
    ### 🎯 Features
    - upcomming Multiple language support
    - High accuracy transcription
    - Speaker detection
    - Noise reduction
    
    ### 📝 Supported Formats
    - WAV, MP3, M4A, FLAC
    - Max duration: 1 hour
    """)

    # File upload section
    uploaded_file = st.file_uploader("Upload your audio file", type=['wav', 'mp3', 'm4a', 'flac'])
    
    if uploaded_file:
        # Display audio player
        st.audio(uploaded_file)
        
        # Settings
        #col1, col2 = st.columns(2)
        #with col1:
            #language = st.selectbox("Select language", ["English", "Spanish", "French", "Auto-detect"])
        #with col2:
            #model_quality = st.select_slider(
                #"Model Quality",
                #options=["Fast", "Balanced", "Accurate"],
                #value="Balanced"
            #)
        
        # Process button
        if st.button("🎯 Transcribe Audio"):
            with st.spinner("Transcribing your audio..."):
                try:
                    # Initialize transcriber
                    transcriber = AudioTranscriber()
                    transcriber.load_model()
                    
                    # Save temporary file and transcribe
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        transcription = transcriber.transcribe_audio(tmp_file.name)
                    
                    # Display results
                    st.success("✅ Transcription completed!")
                    
                    # Results tabs
                    tab1, tab2 = st.tabs(["📝 Result", "⚙️ Export"])
                    
                    with tab1:
                        st.markdown("### Transcription")
                        st.markdown(transcription)
                    
                    with tab2:
                        st.markdown("### Export Options")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.download_button(
                                 "⬇️ Download as TXT",
                                transcription,
                                file_name="transcription.txt",
                                mime="text/plain"
                            )
                        with col2:
                            pdf_content = generate_pdf(transcription)
                            st.download_button(
                                 "📑 Download as PDF",
                                pdf_content,
                                file_name="transcription.pdf",
                                mime="application/pdf"
                            )
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()